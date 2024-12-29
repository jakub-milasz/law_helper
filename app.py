from flask import Flask, render_template, redirect, url_for, request,session
import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai
from urllib.parse import urlparse


html_elements = {
  "title": "Prawniczy pomocnik - prawo karne",
  "description": "Tutaj możesz wpisać wykroczenie",
  "placeholder": "Wpisz wykroczenie...",
  "header": "Artykuł pasujący do twojego przestępstwa"
}


with open("db.csv", "r", encoding="utf-8") as file:
  data = file.read()



main_prompt_template = """
Pytanie: Co w Polsce grozi za następujący czyn: {description}. Podaj odpowiedni artykuł i zacytuj jego treść.
Kontekst:
{data}
Sformatuj odpowiedź za pomocą znaczników HTML, to znaczy: Numer artykułu lub artykułów w nagłówku h3, treść artykułów w paragrafach p, w tym zdanie z odpowiedzią oraz numery artykułów wytłuszczone.
Jeżeli uznasz opis za nieprecyzyjny, napisz "Doprecyzuj" oraz dopisz, w jaki sposób należy doprecyzować opis.
Podaj pytanie pomocnicze w [].
Schemat: "Doprecyzuj: [pytania pomocnicze]"
<h3>Artykuł numer_artykułu</h3>
<p>...</p>
"""

additional_prompt_template = """
Doprecyzowany opis: {description}
"""


def generate_response(description, data, prompt):
  filled_prompt = prompt.format(description=description, data=data)
  response = chat_session.send_message(filled_prompt)
  return response


_ = load_dotenv(find_dotenv())
genai.configure(api_key=os.environ.get("GOOGLE_AI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
# chat_session = model.start_chat(
#     history=[
#     ]
# )


app = Flask(__name__)
app.secret_key = "hello"


@app.route('/', methods=['POST', 'GET'])
def index():
  global chat_session
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    return redirect(url_for('rules'))
  chat_session = model.start_chat(history=[])
  return render_template('index.html', elem=html_elements)

@app.route('/rules')
def rules():
  if "description" in session:
    description = session['description'] # get description from session
    referer = request.headers.get('Referer') # get previous page
    if referer:
      previous_page = urlparse(referer).path # get url path
    else:
      previous_page = None
    if previous_page == '/additional': # check if previous page was additional
      prompt = additional_prompt_template
    else:
      prompt = main_prompt_template
    found_article = generate_response(description, data, prompt)
    print(found_article.text)
    if ("Doprecyzuj" or "[") in found_article.text:
      i1 = found_article.text.index('[')
      i2 = found_article.text.index(']')
      cause = found_article.text[i1+1:i2]
      session['cause'] = cause # save cause in session
      return redirect(url_for('additional'))
    return render_template('rules.html', rules=found_article.text, elem=html_elements)
  
@app.route('/additional', methods=['POST', 'GET'])
def additional():
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    return redirect(url_for('rules'))
  return render_template('additional.html', cause = session['cause'])

if __name__ == '__main__':
  app.run(debug=True)
  
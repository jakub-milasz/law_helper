from flask import Flask, render_template, request, redirect, url_for, request,session, flash
import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai


# with open("db.csv", "r", encoding="utf-8") as file:
#   data = file.read()



prompt_template = """
Pytanie: Co w Polsce grzoi za następujący czyn: {description}. Podaj odpowiedni artykuł i przytocz jego treść.
Sformatuj odpowiedź za pomocą znaczników HTML, to znaczy: Numer artykułu lub artykułów w nagłówku h3, treść artykułów w paragrafach p, w tym zdanie z odpowiedzią wytłuszczone. Jeżeli uznasz opis za nieprecyzyjny, napisz "Doprecyzuj" oraz dopisz, w jaki sposób należy doprecyzować opis. Podaj pytanie pomocnicze w [].
<h3>Artykuł numer_artykułu</h3>
<p>...</p>
"""

def generate_response(description):
  filled_prompt = prompt_template.format(description=description)
  response = model.generate_content(filled_prompt)  
  return response


_ = load_dotenv(find_dotenv())
genai.configure(api_key=os.environ.get("GOOGLE_AI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


app = Flask(__name__)
app.secret_key = "hello"


@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    return redirect(url_for('rules'))
  return render_template('index.html')

@app.route('/rules')
def rules():
  if "description" in session:
    description = session['description']
    found_article = generate_response(description)
    i1 = found_article.text.index('[')
    i2 = found_article.text.index(']')
    cause = found_article.text[i1+1:i2]
    session['cause'] = cause
    if "Doprecyzuj" in found_article.text:
      return redirect(url_for('additional'))
    return render_template('rules.html', rules=found_article.text)
  
@app.route('/additional', methods=['POST', 'GET'])
def additional():
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    return redirect(url_for('rules'))
  return render_template('additional.html', cause = session['cause'])

if __name__ == '__main__':
  app.run(debug=True)
  
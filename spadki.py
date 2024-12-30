from flask import Blueprint, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai
from urllib.parse import urlparse

spadki = Blueprint('spadki', __name__, static_folder='static', template_folder='templates')
spadki.secret_key = "eluwina"

html_elements = {
  "title": "Prawniczy pomocnik - prawo spadkowe",
  "paragraph": "W tej sekcji pomożemy ci zrozumieć, jak działa dziedziczenie w Polsce. Opisz problem, a my spróbujemy go rozwiązać.",
  "description": "Opisz problem związany z prawem spadkowym",
  "placeholder": "Opis problemu...",
  "header": "Rozwiązanie",
  "action": "/spadki/",
}



with open("spadki.csv", "r", encoding="utf-8") as file:
  data = file.read()



main_prompt_template = """
Pytanie: Mam następujący problem związany z prawem spadkowym: {description}. Oblicz, w jakiej części dziedziczą spadkobiercy po wskazanej osobie.
Kontekst:
{data}
Jeżeli uznasz opis za nieprecyzyjny, napisz "Doprecyzuj" oraz dopisz, w jaki sposób należy doprecyzować opis. Numery artykułów wytłuszczone.
Podaj pytanie pomocnicze w [].
Schemat: "Doprecyzuj: [pytania pomocnicze]"
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





@spadki.route('/', methods=['POST', 'GET'])
def index():
  global chat_session
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    return redirect(url_for('spadki.rules'))
  chat_session = model.start_chat(history=[])
  return render_template('index.html', elem=html_elements)

@spadki.route('/rules')
def rules():
  if "description" in session:
    description = session['description'] # get description from session
    referer = request.headers.get('Referer') # get previous page
    if referer:
      previous_page = urlparse(referer).path # get url path
    else:
      previous_page = None
    if previous_page == '/spadki/additional': # check if previous page was additional
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
      return redirect(url_for('spadki.additional'))
    return render_template('rules.html', rules=found_article.text, elem=html_elements)
  
@spadki.route('/additional', methods=['POST', 'GET'])
def additional():
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    return redirect(url_for('spadki.rules'))
  return render_template('additional.html', cause = session['cause'], action = html_elements['action'])
  
from flask import Blueprint, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai
from urllib.parse import urlparse
import json

spadki = Blueprint('spadki', __name__, static_folder='static', template_folder='templates')
spadki.secret_key = "hi"

html_elements = {
  "title": "Prawniczy pomocnik - prawo spadkowe",
  "paragraph": "W tej sekcji pomożemy ci zrozumieć, jak działa dziedziczenie w Polsce. Opisz problem, a my spróbujemy go rozwiązać.",
  "description": "Opisz problem związany z prawem spadkowym",
  "placeholder": "Opis problemu...",
  "header": "Rozwiązanie",
  "action": "/spadki/",
}



with open("datasets/spadki.csv", "r", encoding="utf-8") as file:
  data = file.read()



main_prompt_template = """
Pytanie: Mam następujący problem związany z prawem spadkowym: {description}. Oblicz, w jakiej części dziedziczą spadkobiercy po wskazanej osobie.
Kontekst:
{data}
Zwróć plik JSON gotowy do wczytania za pomocą funkcji json.loads według schematu:
{{
  "type": "object",
  "properties": {{
      "status": {{
          "type": "string",
          "enum": ["doprecyzowanie", "przypisanie"]
      }},
      "add_question": {{
          "type": "string",
          "description": "Ponumerowane pytania oddzielone znacznikiem <br> jeśli status=doprecyzowanie"
      }},
      "article": {{
          "type": "string",
          "description": "Numer artykułu jeśli status=przypisanie"
      }},
      "solution": {{
          "type": "string",
          "description": "Rozwiązanie jeśli status=przypisanie"
      }},
      "summary": {{
          "type": "string",
          "description": "Krótkie podsumowanie w liczbach jeśli status=przypisanie"
      }},
    }},
    "required": ["status"]
}}
Nie dodawaj tekstu spoza formatu JSON.
"""

additional_prompt_template = """
Doprecyzowany opis: {description}
"""


def generate_response(description, data, prompt):
  filled_prompt = prompt.format(description=description, data=data)
  response = chat_session.send_message(filled_prompt)
  return response.text.replace("```","").replace("json","").strip()

_ = load_dotenv(find_dotenv())
genai.configure(api_key=os.environ.get("GOOGLE_AI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")



@spadki.route('/', methods=['POST', 'GET'])
def index():
  global chat_session
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    return redirect(url_for('spadki.solution'))
  chat_session = model.start_chat(history=[])
  return render_template('index.html', elem=html_elements)

@spadki.route('/solution')
def solution():
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
    found_article_json = json.loads(found_article)
    status = found_article_json.get("status", "N/A")
    # print(found_article)
    if status == "doprecyzowanie":
      cause = found_article_json.get("add_question", "N/A")
      session['cause'] = cause # save cause in session
      return redirect(url_for('spadki.additional'))
    article = found_article_json.get("article", "N/A")
    solution = found_article_json.get("solution", "N/A")
    summary = found_article_json.get("summary", "N/A")
    return render_template('solution.html', article=article, solution=solution, summary=summary, elem=html_elements)

@spadki.route('/additional', methods=['POST', 'GET'])
def additional():
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    return redirect(url_for('spadki.solution'))
  return render_template('additional.html', cause = session['cause'], action = html_elements['action'])
  
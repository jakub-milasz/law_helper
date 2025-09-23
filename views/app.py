from flask import Blueprint, jsonify, render_template, redirect, url_for, request,session
import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai
from urllib.parse import urlparse
from views.spadki import spadki
import json
import pandas as pd
import time

app = Blueprint('app', __name__, static_folder='static', template_folder='templates')
app.secret_key = "dodo"



html_elements = {
  "title": "Prawniczy pomocnik - prawo karne",
  "paragraph": "W tej sekcji możesz sprawdzić, jakie konsekwencje prawne grożą za popełnienie wykroczenia. Wpisz opis wykroczenia, a my znajdziemy odpowiedni artykuł kodeksu karnego.",
  "description": "Tutaj możesz wpisać wykroczenie",
  "placeholder": "Wpisz wykroczenie...",
  "header": "Artykuł pasujący do twojego przestępstwa",
  "action": "/karne/",
}

data = pd.read_csv("datasets/new_db.csv", sep=';', encoding="utf-8")


main_prompt_template = """
Pytanie: Co w Polsce grozi za następujący czyn: {description}. Podaj odpowiedni artykuł i zacytuj jego treść.
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
          "description": "Nagłówek artykułu jeśli status=przypisanie"
      }},
      "content": {{
          "type": "string",
          "description": "Treść artykułu jeśli status=przypisanie"
      }},
      "penalty": {{
          "type": "string",
          "description": "Sankcje jeśli status=przypisanie"
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
  selected_option = session.get('selected_option', 'No option selected')
  data = data[data['Kategoria'] == selected_option]
  filled_prompt = prompt.format(description=description, data=data)
  # print(filled_prompt)
  response = chat_session.send_message(filled_prompt)
  return response.text.replace("```","").replace("json","").strip()



def edit_content(content):
  for i in range(len(content)):
    if content[i+1] == '§':
      content = content.replace(content[i+1], '<br>§', 1)
  return content

_ = load_dotenv(find_dotenv())
genai.configure(api_key=os.environ.get("GOOGLE_AI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route('karne/send-option', methods=['POST'])
def receive_option():
  data = request.get_json()
  selected_option = data.get('option')
  session['selected_option'] = selected_option
  return jsonify({"status": "success"}), 200


@app.route('/', methods=['POST', 'GET'])
def index():
  global chat_session
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    return redirect(url_for('app.rules'))
  chat_session = model.start_chat(history=[])
  categories = data['Kategoria'].unique().tolist()
  return render_template('index.html', elem=html_elements, categories=categories)

@app.route('/rules')
def rules():
  if "description" in session:
    description = session['description'] # get description from session
    referer = request.headers.get('Referer') # get previous page
    if referer:
      previous_page = urlparse(referer).path # get url path
    else:
      previous_page = None
    if previous_page == '/karne/additional': # check if previous page was additional
      prompt = additional_prompt_template
    else:
      prompt = main_prompt_template
    found_article = generate_response(description, data, prompt)
    found_article_json = json.loads(found_article)
    status = found_article_json.get("status", "N/A")
    if status == "doprecyzowanie":
      cause = found_article_json.get("add_question", "N/A")
      session['cause'] = cause # save cause in session
      return redirect(url_for('app.additional'))
    article = found_article_json.get("article", "N/A")
    content = found_article_json.get("content", "N/A")
    penalty = found_article_json.get("penalty", "N/A")
    content = content.replace('\n', '<br>')
    return render_template('rules.html', article=article, content=content, penalty=penalty, elem=html_elements)

@app.route('/additional', methods=['POST', 'GET'])
def additional():
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    return redirect(url_for('app.rules'))
  return render_template('additional.html', cause = session['cause'], action = html_elements['action'])
  
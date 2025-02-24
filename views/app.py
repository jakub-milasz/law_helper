from flask import Blueprint, render_template, redirect, url_for, request,session
import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai
from urllib.parse import urlparse
from views.spadki import spadki
from functools import lru_cache
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


with open("datasets/db.csv", "r", encoding="utf-8") as file:
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


@app.route('/', methods=['POST', 'GET'])
def index():
  start_time = time.perf_counter()
  global chat_session
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    return redirect(url_for('app.rules'))
  chat_session = model.start_chat(history=[])
  end_time = time.perf_counter()
  execution_time = end_time - start_time
  print(f"Wynik index: czas wykonania: {execution_time:.6f} sek.")
  return render_template('index.html', elem=html_elements)

# tutaj do optymalizacji
@app.route('/rules')
def rules():
  start_time = time.perf_counter()

  description = session.get('description')
  if not description:
      return redirect(url_for('home'))  # Przykładowa obsługa braku opisu

  referer = request.headers.get('Referer', '')
  previous_page = urlparse(referer).path if referer else None
  prompt = additional_prompt_template if previous_page == '/karne/additional' else main_prompt_template

  found_article = generate_response(description, data, prompt)
  article_text = found_article.text

  if "Doprecyzuj" in article_text or "[" in article_text:
      try:
          cause = article_text.split("[", 1)[1].split("]", 1)[0]  # Szybsze wydobycie zawartości nawiasów
          session['cause'] = cause
          return redirect(url_for('app.additional'))
      except IndexError:
          pass  # Jeśli coś pójdzie nie tak, po prostu kontynuujemy

  execution_time = time.perf_counter() - start_time
  print(f"Wynik rules: czas wykonania: {execution_time:.6f} sek.")
  return render_template('rules.html', rules=article_text, elem=html_elements)
  
@app.route('/additional', methods=['POST', 'GET'])
def additional():
  start_time = time.perf_counter()
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    return redirect(url_for('app.rules'))
  end_time = time.perf_counter()
  execution_time = end_time - start_time
  print(f"Wynik additional: czas wykonania: {execution_time:.6f} sek.")
  return render_template('additional.html', cause = session['cause'], action = html_elements['action'])

if __name__ == '__main__':
  app.run(debug=True)
  
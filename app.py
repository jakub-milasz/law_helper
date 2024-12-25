from flask import Flask, render_template, request, redirect, url_for, request,session, flash
import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai


prompt_template = """
Pytanie: Co w Polsce grzoi za następujący czyn: {description}. Podaj odpowiedni artykuł i przytocz jego treść. Sformatuj za pomocą znaczników HTML, to znaczy: Numer artykułu lub artykułów w nagłówku h3, treść artykułów w paragrafach p, w tym zdanie z odpowiedzią wytłuszczone.
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
    # print(dataset['crime'])
    return redirect(url_for('rules'))
  return render_template('index.html')

@app.route('/rules')
def rules():
  if "description" in session:
    description = session['description']
    found_article = generate_response(description)
    return render_template('rules.html', rules=found_article.text)

if __name__ == '__main__':
  app.run(debug=True)
  
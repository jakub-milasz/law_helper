from flask import Flask, render_template, request, redirect, url_for, request,session, flash

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from stempel import StempelStemmer


app = Flask(__name__)
app.secret_key = "hello"

dataset = pd.read_csv('criminal.csv')
transformed = pd.read_csv('transformed.csv', sep=';')

def transform_text(text):
  text = text.lower()
  text = text.split()
  ss = StempelStemmer.default()
  text = [ss.stem(word) for word in text]
  text = ' '.join(text)
  return text

def fit_crime(my_crime, data):
  my_crime = transform_text(my_crime)
  tfidf_vectorizer = TfidfVectorizer()
  tfidf_matrix = tfidf_vectorizer.fit_transform(data)
  crime_vector = tfidf_vectorizer.transform([my_crime])
  similarity = cosine_similarity(crime_vector, tfidf_matrix)
  if similarity.max() < 0.05:
    return False
  best_match_index = similarity.argsort()[0][-1]
  print(transformed.iloc[best_match_index]['crime'])
  return dataset.iloc[best_match_index]['article_number'], dataset.iloc[best_match_index]['crime'], dataset.iloc[best_match_index]['penalty']



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
    found_article = fit_crime(description, transformed['crime'])
    print(found_article)
    return render_template('rules.html', rules=found_article, description=description)

if __name__ == '__main__':
  app.run(debug=True)
  
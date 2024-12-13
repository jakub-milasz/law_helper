from flask import Flask, render_template, request, redirect, url_for, request,session, flash

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from stempel import StempelStemmer


app = Flask(__name__)
app.secret_key = "hello"

dataset = pd.read_csv('database.csv', sep=';')

def fit_crime(my_crime, data):
  tfidf_vectorizer = TfidfVectorizer()
  tfidf_matrix = tfidf_vectorizer.fit_transform(data)
  crime_vector = tfidf_vectorizer.transform([my_crime])
  similarity = cosine_similarity(crime_vector, tfidf_matrix).flatten()
  best_match_index = similarity.argmax()
  return dataset.iloc[best_match_index]['crime'], dataset.iloc[best_match_index]['penalty']


@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    description = request.form['description']
    session['description'] = description
    print(dataset['crime'])
    return redirect(url_for('rules'))
  return render_template('index.html')

@app.route('/rules')
def rules():
  if "description" in session:
    description = session['description']
    found_article = fit_crime(description, dataset['crime'])
    return render_template('rules.html', rules=found_article, description=description)

if __name__ == '__main__':
  app.run(debug=True)
  
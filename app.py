from flask import Flask, render_template, request, redirect, url_for, request,session, flash

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)
app.secret_key = "hello"

dataset = pd.read_csv('criminal.csv')

def fit_crime(my_crime):
  tfidf_vectorizer = TfidfVectorizer()
  tfidf_matrix = tfidf_vectorizer.fit_transform(dataset['crime'])
  crime_vector = tfidf_vectorizer.transform([my_crime])
  similarity = cosine_similarity(crime_vector, tfidf_matrix)
  best_match_index = similarity.argsort()[0][-1]
  return dataset.iloc[best_match_index]['crime'], dataset.iloc[best_match_index]['penalty']



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
    found_article = fit_crime(description)
    if found_article:
      return render_template('rules.html', crime=found_article[0], penalty=found_article[1], description=description)
    else:
      return render_template('rules.html', rules="Nie znaleziono artykułu")

if __name__ == '__main__':
  app.run(debug=True)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pgadmin123@localhost/Codex'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class Criminal(db.Model):
#     __tablename__ = 'criminal'
#     id = db.Column("article_id", db.Integer, primary_key=True)
#     crime = db.Column("crime", db.String(400))
#     penalty = db.Column("penalty", db.String(400))
  
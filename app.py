from flask import Flask, render_template, request, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pgadmin123@localhost/Codex'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Criminal(db.Model):
    __tablename__ = 'criminal'
    id = db.Column("article_id", db.Integer, primary_key=True)
    crime = db.Column("crime", db.String(400))
    penalty = db.Column("penalty", db.String(400))
    
def clean_description(description):
    return description.strip().lower()


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
    found_article = Criminal.query.filter(Criminal.crime.ilike(f"%{description}%")).first()
    if found_article:
      return render_template('rules.html', crime=description, penalty=found_article.penalty)
    else:
      return render_template('rules.html', rules="Nie znaleziono artykułu")

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)


  # try:
#     conn = psycopg2.connect("postgresql://postgres:Jakubm123@localhost.Codex")
#     print("Połączono z bazą danych!")
#     conn.close()
# except Exception as e:
#     print(f"Nie udało się połączyć z bazą danych: {e}")
  
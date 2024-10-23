from flask import Flask, render_template, request, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Jakubm123@localhost/Codex'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Criminal(db.Model):
    __tablename__ = 'criminal'
    id = db.Column("article_id", db.Integer, primary_key=True)
    article = db.Column("article_description", db.String(1000))


@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    return redirect(url_for('rules'))
  return render_template('index.html')

@app.route('/rules')
def rules():
  rules = Criminal.query.all()
  return render_template('rules.html', rules=rules)

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
  
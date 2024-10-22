from flask import Flask, render_template, request, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import pandas


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
  if request.method == 'POST':
    return redirect(url_for('rules'))
  return render_template('index.html')

@app.route('/rules')
def rules():
  return render_template('rules.html')
if __name__ == '__main__':
  app.run(debug=True)
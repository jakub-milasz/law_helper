import os
from flask import Flask, render_template
from views.spadki import spadki
from views.karne import karne


current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = "hello"
app.register_blueprint(spadki, url_prefix='/spadki')
app.register_blueprint(karne, url_prefix='/karne')


@app.route('/', methods=['POST', 'GET'])
def home():
  return render_template('home.html')

if __name__ == '__main__':
  app.run(debug=True)  
from flask import Flask, render_template
from views.spadki import spadki
from views.karne import karne


app = Flask(__name__)
app.secret_key = "hello"
app.register_blueprint(spadki, url_prefix='/spadki')
app.register_blueprint(karne, url_prefix='/karne')


@app.route('/', methods=['POST', 'GET'])
def home():
  return render_template('home.html')

# if __name__ == '__main__':
#   app.run(debug=True)
  
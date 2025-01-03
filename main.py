from flask import Flask, render_template
from views.spadki import spadki
from views.app import app


main = Flask(__name__)
main.secret_key = "hello"
main.register_blueprint(spadki, url_prefix='/spadki')
main.register_blueprint(app, url_prefix='/karne')


@main.route('/', methods=['POST', 'GET'])
def home():
  return render_template('home.html')

if __name__ == '__main__':
  main.run(debug=True)
  
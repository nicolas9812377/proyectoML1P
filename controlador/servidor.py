from controlador import modulo_tweets as tw
from flask import Flask
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
  tweets = tw.obtenerTweets(5); 
  return json.dumps(tweets),{'Content-Type': 'application/json'}


def correr():
  app.run(host='0.0.0.0', port='3000')
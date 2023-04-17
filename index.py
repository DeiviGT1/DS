from flask import Flask, render_template, request, redirect, url_for
from webscrapping import WebScrapping

app = Flask(__name__)

@app.route('/')
def index(methods=['GET']):
  json_resultados = WebScrapping().resultados()
  
  return render_template('index.html')

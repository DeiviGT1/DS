from flask import Flask, render_template, request, redirect, url_for
from webscrapping import WebScrapping
import pandas as pd
import json

app = Flask(__name__, template_folder='./templates')

@app.route('/')
def index(methods=['GET']):
  resultados = pd.DataFrame(json.loads(open('./info/json_resultados_historicos.json').read())["Resultados"])
  df = pd.DataFrame(resultados.groupby(["rival", "ganador", "torneo"]).count()["fecha"]).sort_values(by="fecha", ascending=False).reset_index()
  df.rename(columns={"fecha": "partidos ganados"}, inplace=True)
  return render_template('index.html', df=df.to_dict())

if __name__ == '__main__':
  app.run(debug=True)
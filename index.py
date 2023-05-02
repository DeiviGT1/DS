from flask import Flask, render_template, request, redirect, url_for
from webscrapping import WebScrapping
import pandas as pd
import json
import operator

app = Flask(__name__, template_folder='./templates', static_folder='./static')

@app.route('/')
def index(methods=['GET']):
  data = json.loads(open('./info/json_resultados_historicos.json').read())["Resultados"]
  partidos_ganados ={}
  dict_=[]
  # return json.loads(open('./info/json_resultados_historicos.json').read())
  for i in data:
    ganador = i["ganador"]
    rival = i["rival"]
    if(ganador, rival) not in partidos_ganados:
      partidos_ganados[(ganador, rival)] = 1
    else:
      partidos_ganados[(ganador, rival)] += 1
  partidos_ganados = sorted(partidos_ganados.items(), key=operator.itemgetter(1), reverse=True)
  for i in partidos_ganados:
    dict_.append({"ganador": i[0][0], "rival": i[0][1], "partidos_ganados": i[1]})

  resultados = {"resultados"  : dict_}
  return render_template('index.html', resultados=resultados)
  

if __name__ == '__main__':
  app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
from webscrapping import WebScrapping
import pandas as pd
import json
import operator

app = Flask(__name__, template_folder='./templates')

@app.route('/')
def index(methods=['GET']):
  data = json.loads(open('./info/json_resultados_historicos.json').read())["Resultados"]
  partidos_ganados ={}
  for d in data:
    rival = d['rival']
    ganador = d['ganador']
    torneo = d['torneo']
    if ganador == rival:
        continue
    key = (rival, ganador, torneo)
    partidos_ganados[key] = partidos_ganados.get(key, 0) + 1

  return str(partidos_ganados)
  partidos_ganados = sorted(partidos_ganados.items(), key=operator.itemgetter(1), reverse=True)
  resultados = []
  
  for ((rival, ganador, torneo), num_partidos) in partidos_ganados:
      resultado = {
          'rival': rival,
          'ganador': ganador,
          'torneo': torneo,
          'partidos_ganados': num_partidos
      }
      resultados.append(resultado)


  return {"resultados": resultados}

if __name__ == '__main__':
  app.run(debug=True)
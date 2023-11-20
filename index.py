from flask import Flask, render_template, request, redirect, url_for
from webscrapping import WebScrapping
import pandas as pd
import jsonpickle
import time
import json
import operator

app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

lista_equipos = json.loads(open('./info/teams.json', encoding="utf8").read())

def resultados_inicial(ganador):
    if ganador == "Independiente Medellín":
        return {"partidos_ganados": 0,
                "partidos_perdidos": 1,
                "partidos_empatados": 0}
    elif ganador == "Empate":
        return {"partidos_ganados": 0,
                "partidos_perdidos": 0,
                "partidos_empatados": 1}
    else:
        return {"partidos_ganados": 1,
                "partidos_perdidos": 0,
                "partidos_empatados": 0}

@app.route('/')
def index(method=['GET']):
  
  data = json.loads(open('./info/json_resultados_historicos.json').read())["json_resultados_historicos"]
  partidos ={}
  dict_=[]
  for i in data:
    ganador = i["ganador"]
    rival = i["rival"]
    escudo = lista_equipos[rival]
    if rival not in partidos:
      partidos[rival] = {"escudo":escudo,
                         "resultados" : resultados_inicial(ganador),
                         "partidos_totales": sum(resultados_inicial(ganador).values())}
    else:
      partidos[rival]["resultados"]["partidos_ganados"] += resultados_inicial(ganador)["partidos_ganados"]
      partidos[rival]["resultados"]["partidos_perdidos"] += resultados_inicial(ganador)["partidos_perdidos"]
      partidos[rival]["resultados"]["partidos_empatados"] += resultados_inicial(ganador)["partidos_empatados"]
      partidos[rival]["partidos_totales"] += sum(resultados_inicial(ganador).values())
  
  version_number = int(time.time())
  resultados = {"resultados"  : partidos}


  return render_template('index.html', resultados=resultados, version = version_number)

if __name__ == '__main__':
  app.run(host='localhost', port=5000, debug=True)
from flask import Flask, render_template, request, redirect, url_for
from webscrapping import WebScrapping
import pandas as pd
import json
import operator

app = Flask(__name__, template_folder='./templates', static_folder='./static')

lista_equipos = {
  '9 de Octubre':'9-de-octubre.png',
  'Rionegro Águilas':'aguilas-doradas.png',
  'Alianza Petrolera':'alianza_petrolera.png',
  'América de Cali':'america.png',
  'Atlético Nacional':'atletico-nacional.png',
  'Boca Juniors':'boca-junior.png',
  'Boyacá Chicó':'boyaca-chico.png',
  'Bucaramanga':'bucaramaga.png',
  'Caracas FC':'caracas.png',
  'Cerro Porteño':'cerro-porteno.png',
  'Cortuluá':'cortulua.png',
  'Cúcuta Deportivo':'cucuta-deportivo.png',
  'Deportivo Cali':'deportivo-cali.png',
  'Independiente Medellín':'deportivo-independiente-medellin.png',
  'Deportivo Táchira':'deportivo-tachira.png',
  'Emelec':'emelec.png',
  'Envigado':'envigado.png',
  'La Equidad':'equidad.png',
  'Leones':'leones.png',
  'Fortaleza CEIF':'fortaleza.png',
  'Guaireña':'guairena.png',
  'Atlético Huila':'huila.png',
  'Internacional':'internacional.png',
  'Jaguares de Córdoba':'jaguares.png',
  'Atlético Junior':'junior.png',
  'Libertad':'libertad.png',
  'Melgar':'melgas.png',
  'Millonarios':'millonarios.png',
  'Once Caldas':'once-caldas.png',
  'Pachuca':'pachuca.png',
  'Palestino':'palestino.png',
  'Deportivo Pasto':'pasto.png',
  'Patriotas':'patriotas.png',
  'Peñarol':'penarol.png',
  'Deportivo Pereira':'pereira.png',
  'Deportes Quindío':'quindio.png',
  'Racing Club':'racing.png',
  'River Plate':'river-plate.png',
  'Santa Cruz':'santa-cruz.png',
  'Independiente Santa Fe':'santa-fe.png',
  'Sol de América':'sol-de-america.png',
  'Sportivo Luqueño':'sportivo-luqueno.png',
  'Tigres':'tigres.png',
  'Deportes Tolima':'tolima.png',
  'Atlético Tucumán':'tucuman.png',
  'Unión Magdalena':'union-magdalena.png',
  'Universidad Católica (Quito)':'universidad-catolica-quito.png',
  'Valledupar FC':'valledupar.png'
}

@app.route('/')
def index(methods=['GET']):
  data = json.loads(open('./info/json_resultados_historicos.json').read())["Resultados"]
  partidos_ganados ={}
  dict_=[]
  # return json.loads(open('./info/json_resultados_historicos.json').read())
  for i in data:
    ganador = i["ganador"]
    rival = i["rival"]
    escudo = lista_equipos[rival]
    if(ganador, rival) not in partidos_ganados:
      partidos_ganados[(ganador, rival, escudo)] = 1
    else:
      partidos_ganados[(ganador, rival, escudo)] += 1
  partidos_ganados = sorted(partidos_ganados.items(), key=operator.itemgetter(1), reverse=True)
  for i in partidos_ganados:
    dict_.append({"ganador": i[0][0], "rival": i[0][1], "partidos_ganados": i[1], "escudo": i[0][2]})

  resultados = {"resultados"  : dict_}
  return render_template('index.html', resultados=resultados)
  

if __name__ == '__main__':
  app.run(debug=True)
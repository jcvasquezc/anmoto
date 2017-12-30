import dash
import dash_core_components as dcc
import dash_html_components as html
import os

import plotly.graph_objs as go
import pandas as pd
import numpy as np

from functools import reduce
from utils import top_list, compute_prob, prob_list, compute_prob_city
import base64

app = dash.Dash(__name__)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


df=pd.read_csv('./data_motos.csv')
dfp=pd.read_csv('./pos_col.csv')

lat=[str(dfp["lat"][j]) for j in range(len(dfp["lat"]))]
lon=[str(dfp["lon"][j]) for j in range(len(dfp["lon"]))]
city_map=dfp["MUNICIPIO"]

image_filename1="./udea.png"
image_filename2="./logoGITA.png"
image_filename3="./logo.png"

encoded_image1=base64.b64encode(open(image_filename1, 'rb').read())
encoded_image2=base64.b64encode(open(image_filename2, 'rb').read())
encoded_image3=base64.b64encode(open(image_filename3, 'rb').read())

data=[str(df["Departamento"][j]) for j in range(len(df["Departamento"]))]
list_dep=np.unique(data)
data=[str(df["Municipio"][j]) for j in range(len(df["Municipio"]))]
list_city=np.unique(data)
data=[str(df["MARCA"][j]) for j in range(len(df["MARCA"]))]
list_brand=np.unique(data)
data=[str(df["COLOR"][j]) for j in range(len(df["COLOR"]))]
list_color=np.unique(data)
list_model=np.unique(df["MODELO"])
list_model=[list_model[k] for k in range(len(list_model)) if not np.isnan(list_model[k])]
data=[str(df["LINEA"][j]) for j in range(len(df["LINEA"]))]
list_type=np.unique(data)
list_barrio=np.unique(df["Barrio"])

datalinea=[str(df["LINEA"][j]) for j in range(len(df["LINEA"]))]
datacity=[str(df["Municipio"][j]) for j in range(len(df["Municipio"]))]
datamodel=[str(df["MODELO"][j]) for j in range(len(df["MODELO"]))]
datastate=[str(df["Departamento"][j]) for j in range(len(df["Departamento"]))]
databarrio=[str(df["Barrio"][j]) for j in range(len(df["Barrio"]))]



models=df['MODELO'].unique()
models.sort()

models=[models[j] for j in range(len(models)-1)]

list_moto=[df["MARCA"][j]+" "+datalinea[j] for j in range(len(df["MARCA"]))]

top10motos=top_list(list_moto, 10)

top10motos_menos=top_list(list_moto, 10, flag_order=0)

print(top10motos)

print(top10motos_menos)


top5city=top_list(df["Municipio"], 10)

print(top5city)


top5barrios=["","","","","","","","","",""]

prob_linea=compute_prob(list_moto, np.unique(list_moto), True)
#prob_model=compute_prob(datamodel, list_model, True)
prob_city=compute_prob(datacity, list_city, True)
prob_state=compute_prob(datastate, list_dep, True)
prob_barrio=compute_prob(databarrio, list_barrio, True)




list_type_model=[datalinea[j]+" "+str(df["MODELO"][j]) for j in range(len(df["MARCA"]))]
prob_linea_model=compute_prob(datalinea, list_type_model, False)

list_type_model_state=[df["Departamento"][j]+" "+datalinea[j]+" "+str(df["MODELO"][j]) for j in range(len(df["MARCA"]))]
prob_linea_model_state=compute_prob(datalinea, list_type_model_state, False)

list_type_state=[df["Departamento"][j]+" "+datalinea[j] for j in range(len(df["MARCA"]))]
prob_linea_state=compute_prob(datalinea, list_type_state, False)


list_type_model_city=[df["Municipio"][j]+" "+datalinea[j]+" "+str(df["MODELO"][j]) for j in range(len(df["MARCA"]))]
prob_linea_model_city=compute_prob(datalinea, list_type_model_city, False)

list_type_city=[df["Municipio"][j]+" "+datalinea[j] for j in range(len(df["MARCA"]))]
prob_linea_city=compute_prob(datalinea, list_type_city, False)

list_type_model_neigh=[df["Barrio"][j]+" "+datalinea[j]+" "+str(df["MODELO"][j]) for j in range(len(df["MARCA"]))]
prob_linea_model_barrio=compute_prob(datalinea, list_type_model_neigh, False)



probtop10more=prob_list(top10motos, np.unique(list_moto), prob_linea)
probtop10less=prob_list(top10motos_menos, np.unique(list_moto), prob_linea)
probtop10cities=prob_list(top5city, list_city, prob_city)

list_top10morestr=[]
list_top10lessstr=[]
list_top10citystr=[]



for k in range(10):
    list_top10morestr.append(top10motos[k]+': '+str(np.round(probtop10more[k],3)))
    list_top10lessstr.append(top10motos_menos[k]+': '+str(np.round(probtop10less[k],3)))
    list_top10citystr.append(top5city[k]+': '+str(np.round(probtop10cities[k],3)))


styles = {
    'column': {
        'display': 'inline-block',
        'width': '90%',
        'padding': 10,
        'boxSizing': 'boder-box',
        'minHeight': '350px',
        'columnCount': 4,
    },
    'pre': {'border': 'thin lightgrey solid'}
}



token='pk.eyJ1IjoiamN2YXNxdWV6YyIsImEiOiJjajhpOHJzYzEwd2lhMndteGE3dXdoZ2JwIn0.FXt2St8t89mIZ-L-UpCYkg'


mapbox_access_token = token

datamap = go.Data([
    go.Scattermapbox(
        lat=['4.6'],
        lon=['-74.0833333'],

        mode='markers',
        marker=go.Marker(
            size=8
        ),
        text=['Bogotá'],
    )
])

layoutmap = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=4.6,
            lon=-74.09
        ),
        domain=dict(
                x=[0,1],
                y=[0,1]
            ),
        pitch=0,
        style='light',
        zoom=3.5
    ),
)





app.layout = html.Div([
        #html.H1(children='ANMOTO'),
        html.Title("ANMOTO"),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image1.decode()), style={'height':'5%', 'width': '10%', 'display': 'inline-block'}),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()), style={'height':"10%", 'width': '10%', 'display': 'inline-block'}),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image3.decode()), style={'height':'5%', 'width': '10%', 'display': 'inline-block'}),
        html.Div(["Herramienta de análisis de hurto de motocicletas en Colombia"], style={"font-size":"180%", 'width': '60%', 'display': 'inline-block'}),

        html.Div([

        html.Div([
            html.Div([
            html.Div(["Marca"]),
            dcc.Dropdown(
                    id="brand",
            options=[{'label': list_brand[i], "value": list_brand[i]} for i in range(len(list_brand))],

            ),]),

            html.Div([
            html.Div(["Linea"]),
            dcc.Dropdown(id="type_",),
            ]),

            html.Div([
            html.Div(["Color"]),
            dcc.Dropdown(
                    id="color",
            options=[{'label': list_color[i], "value": list_color[i]} for i in range(len(list_color))],
            ),]),

            html.Div([
            html.Div(["Modelo"]),
            dcc.Dropdown(
                    id="model",
            options=[{'label': models[i], "value": models[i]} for i in range(len(models))],
            ),]),
        ]),

        html.Div([
            html.Div([
            html.Div(["Departamento donde se encuentra"]),
            dcc.Dropdown(
                    id="state",
            options=[{'label': list_dep[i], "value": list_dep[i]} for i in range(len(list_dep))],
            ),]),

            html.Div([
            html.Div(["Ciudad donde se encuentra"]),
            dcc.Dropdown(
                    id="city",),
            ])
        ]),

        ],  style={'columnCount': 2}),




     html.Div([
    dcc.Markdown("""
            La Probabilidad de que su moto sea robada es: '{}'

            La probabilidad de que su moto sea robada en '{}' es: '{}'

            La probabilidad de que su moto sea robada en '{}' es: '{}'
        """.replace('   ', '').format('0.0', ' ', '0.0', ' ', '0.0')),
        html.Pre(style=styles['pre']),
             ],id="prob"),




    html.Div([
         dcc.Graph(
             id='map',
             figure={'data': datamap,

                 'layout': layoutmap

             }
         ),], style={'height':'300%','width': '33%', 'padding': '0 20', 'display': 'inline-block'}),



    html.Div([
     dcc.Graph(
         id='hurto',
         figure={'data': [
                 go.Histogram(x=df["Hora"], nbinsx=50)],

             'layout': go.Layout(
                 xaxis={'title': 'Hora'},
                 yaxis={'title': 'Número de motos robadas'},
                 margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                 hovermode='closest'
             )

         }
     ),], style={'width': '33%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
    dcc.Graph(
         id='hurto2',
         figure={'data': [
                 go.Histogram(x=df["Dia"], nbinsx=7)],

             'layout': go.Layout(
                 xaxis={'title': 'Dia de la semana'},
                 yaxis={'title': 'Número de motos robadas'},
                 margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                 hovermode='closest'
             )

         }
     )

      ], style={'display': 'inline-block', 'width': '33%'}),



    html.Div([
        dcc.Markdown("""
            **Motos más robadas en Colombia**

            1. '{}'
            2. '{}'
            3. '{}'
            4. '{}'
            5. '{}'
            6. '{}'
            7. '{}'
            8. '{}'
            9. '{}'
            10. '{}' :
        """.replace('   ', '').format(list_top10morestr[0], list_top10morestr[1], list_top10morestr[2], list_top10morestr[3], list_top10morestr[4],
                                      list_top10morestr[5], list_top10morestr[6], list_top10morestr[7], list_top10morestr[8], list_top10morestr[9])),
        html.Pre(id='lista', style=styles['pre']),

        dcc.Markdown("""
            **Motos menos robadas en Colombia**

            1. '{}'
            2. '{}'
            3. '{}'
            4. '{}'
            5. '{}'
            6. '{}'
            7. '{}'
            8. '{}'
            9. '{}'
            10. '{}'
        """.replace('   ', '').format(list_top10lessstr[0], list_top10lessstr[1], list_top10lessstr[2], list_top10lessstr[3], list_top10lessstr[4],
                                      list_top10lessstr[5], list_top10lessstr[6], list_top10lessstr[7], list_top10lessstr[8], list_top10lessstr[9])),
        html.Pre(id='lista', style=styles['pre']),

        dcc.Markdown("""
            **Ciudades donde más motos roban**

            1. '{}'
            2. '{}'
            3. '{}'
            4. '{}'
            5. '{}'
            6. '{}'
            7. '{}'
            8. '{}'
            9. '{}'
            10. '{}'
        """.replace('   ', '').format(list_top10citystr[0], list_top10citystr[1], list_top10citystr[2], list_top10citystr[3], list_top10citystr[4],
                                      list_top10citystr[5], list_top10citystr[6], list_top10citystr[7], list_top10citystr[8], list_top10citystr[9])),
        html.Pre(id='lista', style=styles['pre']),


        html.Div([
        dcc.Markdown("""
            **Barrios donde más motos roban en '{}'**

            1. '{}'
            2. '{}'
            3. '{}'
            4. '{}'
            5. '{}'
            6. '{}'
            7. '{}'
            8. '{}'
            9. '{}'
            10. '{}'
        """.replace('   ', '').format(' ', top5barrios[0], top5barrios[1], top5barrios[2], top5barrios[3], top5barrios[4],top5barrios[5], top5barrios[6], top5barrios[7], top5barrios[8], top5barrios[9])),
        html.Pre(style=styles['pre']),
        ],id='listbarrio'),



    ], style=styles['column']),


html.Div(["Icons made by Freepik from Flaticon. Is licensed by Creative Commons BY 3.0"])

 ])


@app.callback(
     dash.dependencies.Output('city', 'options'),
     [dash.dependencies.Input('state', 'value'),
      ])
def update_drop(state):
    print("--------------------------------------------")
    print(state)
    pos_state=np.where(df["Departamento"]==state)[0]
    city_sel=np.unique(df["Municipio"][pos_state])
    print(city_sel)
    print(len(city_sel))
    return [{'label': city_sel[i], "value": city_sel[i]} for i in range(len(city_sel))]







@app.callback(
     dash.dependencies.Output('type_', 'options'),
     [dash.dependencies.Input('brand', 'value'),
      ])
def update_drop2(brand):
    print("--------------------------------------------")
    print(brand)
    pos_brand=np.where(df["MARCA"]==brand)[0]
    print("###########################################################")
    print(brand, pos_brand)
    print("##############################################################")
    type_sel=np.unique(df["LINEA"][pos_brand])
    print(type_sel)
    print(len(type_sel))
    return [{'label': str(type_sel[i]), "value": type_sel[i]} for i in range(len(type_sel))]


@app.callback(
     dash.dependencies.Output('model', 'options'),
     [dash.dependencies.Input('type_', 'value'),
      ])
def update_drop3(type_):
    print("---------------------------------------------------------------- MODELOS -----------------------------------------------------")
    print(type_)
    pos_brand=np.where(df["LINEA"]==type_)[0]
    print(pos_brand)
    type_sel=np.unique(df["MODELO"][pos_brand])
    type_sel=[type_sel[k] for k in range(len(type_sel)) if not np.isnan(type_sel[k])]
    print(type_sel)
    print(len(type_sel))
    return [{'label': type_sel[i], "value": type_sel[i]} for i in range(len(type_sel))]



@app.callback(
     dash.dependencies.Output('color', 'options'),
     [dash.dependencies.Input('brand', 'value'),
      ])
def update_drop4(brand):
    print("--------------------------------------------")
    print(brand)
    pos_brand=np.where(df["MARCA"]==brand)[0]
    type_sel=np.unique(df["COLOR"][pos_brand])
    print(type_sel)
    print(len(type_sel))
    return [{'label': type_sel[i], "value": type_sel[i]} for i in range(len(type_sel))]




@app.callback(
     dash.dependencies.Output('map', 'figure'),
     [dash.dependencies.Input('type_', 'value'),
      ])
def update_map(type_):

    prob_cities=compute_prob_city(type_, list_city, list_type_city, prob_linea_city)

    print(prob_cities)

    pos_prob=np.where(prob_cities>0)[0]

    city_list_map=list_city[pos_prob]

    latmap=[]
    lonmap=[]
    sizemap=[]
    textmap=[]
    for k in range(len(city_list_map)):
        pos_map=np.where(city_map==city_list_map[k])[0]
        if len(pos_map)>0:
            latmap.append(lat[pos_map[0]])
            lonmap.append(lon[pos_map[0]])
            sizemap.append(int(np.ceil((prob_cities[pos_prob[k]]*100)))+4)
            textmap.append(city_map[pos_map[0]]+'\n\r'+"Probabilidad="+str(np.round(prob_cities[pos_prob[k]],3)))




    datamap2 = go.Data([
        go.Scattermapbox(
            lat=latmap,
            lon=lonmap,

            mode='markers',
            marker=go.Marker(
                size=sizemap
            ),
            text=textmap,
        )
    ])
    #
    print(latmap)
    print(city_map)
    print(sizemap)
    print(datamap2)

    return {
        'data': datamap2,
            'layout': layoutmap
    }



@app.callback(
    dash.dependencies.Output('hurto', 'figure'),
    [dash.dependencies.Input('brand', 'value'),
     dash.dependencies.Input('color', 'value'),
     dash.dependencies.Input('model', 'value'),
     dash.dependencies.Input('state', 'value'),
     dash.dependencies.Input('city', 'value'),
     dash.dependencies.Input('type_', 'value'),
     ])
def update_graph(brand, color, model, state, city, type_):
     pos_state=np.where(df["Departamento"]==state)[0]
     pos_city=np.where(df["Municipio"]==city)[0]
     pos_brand=np.where(df["MARCA"]==brand)[0]
     #pos_color=np.where(df["COLOR"]==color)[0]
     pos_model=np.where(df["MODELO"]==model)[0]
     pos_type=np.where(df["LINEA"]==type_)[0]


     if len(pos_model)>0:
         intersect=reduce(np.intersect1d, (pos_state, pos_city, pos_brand, pos_model, pos_type))
     else:
         intersect=reduce(np.intersect1d, (pos_state, pos_city, pos_brand, pos_type))


     h=[df["Hora"][j][-2:]+" "+df["Hora"][j][0:2] for j in range(len(df["Hora"]))]
     hstate=[h[j] for j in intersect]
     hstate.sort()
     print(hstate)
     return {
         'data': [
                 go.Histogram(x=hstate, nbinsx=20)],

             'layout': go.Layout(
                 xaxis={'title': "Hora"},
                 yaxis={'title': 'Número de motos robadas'},
                 margin={'l': 40, 'b': 60, 't': 10, 'r': 10},
                 hovermode='closest'
             )
     }

@app.callback(
    dash.dependencies.Output('hurto2', 'figure'),
    [dash.dependencies.Input('brand', 'value'),
     dash.dependencies.Input('color', 'value'),
     dash.dependencies.Input('model', 'value'),
     dash.dependencies.Input('state', 'value'),
     dash.dependencies.Input('city', 'value'),
     dash.dependencies.Input('type_', 'value'),
     ])
def update_graph2(brand, color, model, state, city, type_):
     pos_state=np.where(df["Departamento"]==state)[0]
     pos_city=np.where(df["Municipio"]==city)[0]
     pos_brand=np.where(df["MARCA"]==brand)[0]
     #pos_color=np.where(df["COLOR"]==color)[0]
     pos_model=np.where(df["MODELO"]==model)[0]
     pos_type=np.where(df["LINEA"]==type_)[0]


     if len(pos_model)>0:
         intersect=reduce(np.intersect1d, (pos_state, pos_city, pos_brand, pos_model, pos_type))
     else:
         intersect=reduce(np.intersect1d, (pos_state, pos_city, pos_brand, pos_type))
     h=df["Dia"]

     order=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

     hstate=[h[j] for j in intersect]
     hstate2=sorted(hstate, key=lambda v: order.index(v))

     #hstate.sort()
     return {
         'data': [
                 go.Histogram(x=hstate2, nbinsx=7)],

             'layout': go.Layout(
                 xaxis={'title': "Dia"},
                 yaxis={'title': 'Número de motos robadas'},
                 margin={'l': 40, 'b': 60, 't': 10, 'r': 10},
                 hovermode='closest'
             )
     }




@app.callback(
        dash.dependencies.Output('prob', 'children'),
        [dash.dependencies.Input('type_', 'value'),
        dash.dependencies.Input('city', 'value'),
        dash.dependencies.Input('model', 'value'),
        dash.dependencies.Input('state', 'value'),
        ])
def upate_prob(type_, city, model, state):

    pos_state=np.where(df["Departamento"]==state)[0]
    pos_city=np.where(df["Municipio"]==city)[0]
    pos_model=np.where(df["MODELO"]==model)[0]
    pos_type=np.where(df["LINEA"]==type_)[0]


    print("*******************************************************")
    print(len(pos_type), len(pos_city), len(pos_state))
    pos_all=0
    if len(pos_type)==0 or len(pos_city)==0 or len(pos_state)==0:
        return [
                dcc.Markdown("""
                La Probabilidad de que su moto sea robada es: {}

                La probabilidad de que su moto sea robada en {} es {}

                La probabilidad de que su moto sea robada en {} es: {}
            """.replace('   ', '').format("0", "", "0", "", "0")),
            html.Pre(style=styles['pre']),
                 ]
    else:
        if not model==None:
            chosen_=str(type_)+" "+str(model)+".0"
            print(".........................................")
            print(chosen_)
            print(".........................................")
            for j in range(len(list_type_model)):
                if list_type_model[j]==chosen_:
                    pos_all=j
                    break
            prob_robbed1=prob_linea_model[pos_all]
        else:
            chosen_=type_
            for j in range(len(list_type)):
                if list_type[j]==chosen_:
                    pos_all=j
                    break
            prob_robbed1=prob_linea[pos_all]

        if not model==None:
            chosen_=city+" "+type_+" "+str(model)+".0"
            print(".........................................")
            print(chosen_)
            print(".........................................")
            for j in range(len(list_type_model_city)):
                if list_type_model_city[j]==chosen_:
                    pos_all=j
                    break
            prob_robbed3=prob_linea_model_city[pos_all]

        else:
            chosen_=city+" "+type_
            print(".........................................")
            print(chosen_)
            print(".........................................")
            for j in range(len(list_type_city)):
                if list_type_city[j]==chosen_:
                    pos_all=j
                    break
            prob_robbed3=prob_linea_city[pos_all]


        if not model==None:
            chosen_=state+" "+type_+" "+str(model)+".0"
            print(".........................................")
            print(chosen_)
            print(".........................................")
            for j in range(len(list_type_model_state)):
                if list_type_model_state[j]==chosen_:
                    pos_all=j
                    break
            prob_robbed2=prob_linea_model_state[pos_all]
        else:
            chosen_=state+" "+type_
            print(".........................................")
            print(chosen_)
            print(".........................................")
            for j in range(len(list_type_state)):
                if list_type_state[j]==chosen_:
                    pos_all=j
                    break
            prob_robbed2=prob_linea_state[pos_all]



        return [
                dcc.Markdown("""
                La Probabilidad de que su moto sea robada es: {}

                La probabilidad de que su moto sea robada en {} es {}

                La probabilidad de que su moto sea robada en {} es: {}
            """.replace('   ', '').format(str(np.round(prob_robbed1,3)), state, str(np.round(prob_robbed2,3)), city, str(np.round(prob_robbed3,3)))),
            html.Pre(style=styles['pre']),
                 ]



@app.callback(
    dash.dependencies.Output('listbarrio', 'children'),
    [dash.dependencies.Input('city', 'value'),
    ])
def update_barriolist(city):
    if city==None:
        return [dcc.Markdown("""
                    **Barrios donde más motos roban en '{}'**

                    1. '{}'
                    2. '{}'
                    3. '{}'
                    4. '{}'
                    5. '{}'
                    6. '{}'
                    7. '{}'
                    8. '{}'
                    9. '{}'
                    10. '{}'
                """.replace('   ', '').format(' ', ' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ', ' ')),
                ]


    else:

        pos_city=np.where(df["Municipio"]==city)[0]
        barrio_sel=np.unique(df["Barrio"][pos_city])
        top5barrios=top_list(barrio_sel,10)
        print(top5barrios)
        return [dcc.Markdown("""
                    **Barrios donde más motos roban en '{}'**

                    1. '{}'
                    2. '{}'
                    3. '{}'
                    4. '{}'
                    5. '{}'
                    6. '{}'
                    7. '{}'
                    8. '{}'
                    9. '{}'
                    10. '{}'
                """.replace('   ', '').format(city, top5barrios[0], top5barrios[1], top5barrios[2], top5barrios[3], top5barrios[4],top5barrios[5], top5barrios[6], top5barrios[7], top5barrios[8], top5barrios[9])),
                ]



if __name__ == '__main__':
    app.run_server(debug=True)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 18:35:49 2017

@author: J. C. Vasquez-Correa
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from functools import reduce
from utils import top_list, compute_prob
import base64

app = dash.Dash()



df=pd.read_csv('./data_motos.csv')
image_filename1="./udea.png"
image_filename2="./logoGITA.png"
encoded_image1=base64.b64encode(open(image_filename1, 'rb').read())
encoded_image2=base64.b64encode(open(image_filename2, 'rb').read())



list_dep=np.unique(df["Departamento"])
list_city=np.unique(df["Municipio"])
list_brand=np.unique(df["MARCA"])
list_color=np.unique(df["COLOR"])
list_model=np.unique(df["MODELO"])
list_type=np.unique(df["LINEA"])
list_barrio=np.unique(df["Barrio"])

models=df['MODELO'].unique()
models.sort()

models=[models[j] for j in range(len(models)-1)]

list_moto=[df["MARCA"][j]+" "+df["LINEA"][j] for j in range(len(df["MARCA"]))]

top5motos=top_list(list_moto, 5)

top5city=top_list(df["Municipio"], 5)

list_type_model=[df["LINEA"][j]+" "+str(df["MODELO"][j]) for j in range(len(df["MARCA"]))]
prob_linea_model=compute_prob(df["LINEA"], list_type_model)

list_type_model_state=[df["Departamento"][j]+" "+df["LINEA"][j]+" "+str(df["MODELO"][j]) for j in range(len(df["MARCA"]))]
prob_linea_model_state=compute_prob(df["LINEA"], list_type_model_state)

list_type_model_city=[df["Municipio"][j]+" "+df["LINEA"][j]+" "+str(df["MODELO"][j]) for j in range(len(df["MARCA"]))]
prob_linea_model_city=compute_prob(df["LINEA"], list_type_model_city)

list_type_model_neigh=[df["Barrio"][j]+" "+df["LINEA"][j]+" "+str(df["MODELO"][j]) for j in range(len(df["MARCA"]))]
prob_linea_model_barrio=compute_prob(df["LINEA"], list_type_model_neigh)




styles = {
    'column': {
        'display': 'inline-block',
        'width': '100%',
        'padding': 10,
        'boxSizing': 'boder-box',
        'minHeight': '600px', 
        'columnCount': 2,
    },
    'pre': {'border': 'thin lightgrey solid'}
}

app.layout = html.Div([
        html.Img(src='data:image/png;base64,{}'.format(encoded_image1.decode()), style={'width':150, 'height':100}),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()), style={'width':150, 'height':100}),
        html.Div(["Herramienta de diagnóstico y análisis de hurto de motocicletas en Colombia: DIANMOTO"], style={"font-size":"180%"}),
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
     ),], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
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
         
      ], style={'display': 'inline-block', 'width': '49%'}),
    html.Div([
        dcc.Markdown("""
            **Motos más robadas en Colombia**

            1. '{}'
            2. '{}'
            3. '{}'
            4. '{}'
            5. '{}'
        """.replace('   ', '').format(top5motos[0], top5motos[1], top5motos[2], top5motos[3], top5motos[4])),
        html.Pre(id='lista', style=styles['pre']),
    
        dcc.Markdown("""
            **Ciudades donde más motos roban**

            1. '{}'
            2. '{}'
            3. '{}'
            4. '{}'
            5. '{}'
        """.replace('   ', '').format(top5city[0], top5city[1], top5city[2], top5city[3], top5city[4])),
        html.Pre(id='lista', style=styles['pre']),   
    
    ], style=styles['column']),
#     dcc.Graph(
#         id='scatterPDTOD',
#         figure={
#             'data': [
#                 go.Scatter(
#                     x=df[i]['UPDRS'],
#                     y=df[i]['TOD'],
#                     text=df[i]['AGE'],
#                     mode='markers',
#                     opacity=0.7,
#                     marker={
#                         'size': 15,
#                         'line': {'width': 0.5, 'color': 'white'}
#                     },
#                     name=i
#                 ) for i in ["Czech", "Spanish", "German", "Portuguese"]
#             ],
#             'layout': go.Layout(
#                 xaxis={'type': 'log', 'title': 'UPDRS'},
#                 yaxis={'title': 'Time post diagnosis'},
#                 margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#                 legend={'x': 0, 'y': 1},
#                 hovermode='closest'
#             )
#         }
#     )])
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
    type_sel=np.unique(df["LINEA"][pos_brand])
    print(type_sel)
    print(len(type_sel))
    return [{'label': type_sel[i], "value": type_sel[i]} for i in range(len(type_sel))]
     

@app.callback(
     dash.dependencies.Output('model', 'options'),
     [dash.dependencies.Input('type_', 'value'),
      ])
def update_drop3(type_):
    print("--------------------------------------------")
    print(type_)
    pos_brand=np.where(df["LINEA"]==type_)[0]
    type_sel=np.unique(df["MODELO"][pos_brand])
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
     

     intersect=reduce(np.intersect1d, (pos_state, pos_city, pos_brand, pos_model, pos_type))
     
     h=[df["Hora"][j][-2:]+" "+df["Hora"][j][0:2] for j in range(len(df["Hora"]))]
     hstate=[h[j] for j in intersect]
     hstate.sort()
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
     

     intersect=reduce(np.intersect1d, (pos_state, pos_city, pos_brand, pos_model, pos_type))
     
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

    print("..............................................")
    print(model)
    print("..............................................")
    
    chosen_=type_+" "+str(model)+".0"
    print(".........................................")
    print(chosen_)
    print(".........................................")
    for j in range(len(list_type_model)):
        if list_type_model[j]==chosen_:
            pos_all=j
            break
    prob_robbed1=prob_linea_model[pos_all]
    
    chosen_=city+" "+type_+" "+str(model)+".0"
    print(".........................................")
    print(chosen_)
    print(".........................................")
    for j in range(len(list_type_model_city)):
        if list_type_model_city[j]==chosen_:
            pos_all=j
            break
    prob_robbed3=prob_linea_model_city[pos_all]    

    chosen_=state+" "+type_+" "+str(model)+".0"
    print(".........................................")
    print(chosen_)
    print(".........................................")
    for j in range(len(list_type_model_state)):
        if list_type_model_state[j]==chosen_:
            pos_all=j
            break
    prob_robbed2=prob_linea_model_state[pos_all]    
    

    
    
    return [        
            dcc.Markdown("""
            La Probabilidad de que su moto sea robada es: {}
            
            La probabilidad de que su moto sea robada en {} es {}
            
            La probabilidad de que su moto sea robada en {} es: {}
        """.replace('   ', '').format(str(np.round(prob_robbed1,3)), state, str(np.round(prob_robbed2,3)), city, str(np.round(prob_robbed3,3)))),
        html.Pre(style=styles['pre']),
             ]


if __name__ == '__main__':
    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"}) # to change fontstyle
    app.run_server()
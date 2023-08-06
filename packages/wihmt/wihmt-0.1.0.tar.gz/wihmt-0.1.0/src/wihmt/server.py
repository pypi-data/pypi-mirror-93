# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import datetime
import sys
import ofxtools
from ofxtools.Parser import OFXTree
import pytz
import os
import logging

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
occ = """
"""
ofx_file = None

try:
    occ = open("occ.save", "r").read()
    logging.debug("occ read")
except:
    pass

app = dash.Dash(__name__)

def update_with_occ(data, occ, amount=0, charges=()):
    occ_data = {}
    for line in occ.splitlines():
        if len(line.strip()) == 0:
            continue
        if line.startswith("#"):
            continue
        _d = line.split("|")
        if int(_d[0].strip()) not in occ_data:
            occ_data[int(_d[0].strip())] = [float(_d[1].strip()), ]
            # print("if", int(_d[0].strip()), occ_data[int(_d[0].strip())])
        else:
            occ_data[int(_d[0].strip())].append(float(_d[1].strip()))
            # print("else", int(_d[0].strip()), occ_data[int(_d[0].strip())])
    date = datetime.datetime.today()
    # print("occ_data", occ_data)
    for day in range(31):
        try:
            current_day = date.day
            amount += sum(occ_data[current_day])
        except KeyError:
            pass
        data["date"].append(date)
        data["amount"].append(amount)
        data["type"].append("futur")
        data["date"].append(date)
        data["amount"].append(amount - day*sum(charges)/30)
        data["type"].append("avec charges non fixes")
        date += datetime.timedelta(days=1)


def aggregate(data, c_amount=0):
    _d = {"date": [], "amount": [], "type": []}
    for cpt in range(len(data["date"])):
        if data["date"][cpt] not in _d["date"]:
            _d[data["date"][cpt]] = [data["amount"][cpt], ]
            _d["date"].append(data["date"][cpt])
        else:
            _d[data["date"][cpt]].append(data["amount"][cpt])
    data["date"] = []
    data["amount"] = []
    data["type"] = []
    del(data["name"])
    #_date = sorted(_d["date"])
    for cpt in _d["date"]:
        data["date"].append(cpt)
        c_amount -= sum(_d[cpt])
        data["amount"].append(c_amount)
        data["type"].append("réel")

def get_ofx(filename, occ="", charges=(), mois=3):
    data = {"date": [], "amount": [], "name": []}
    parser = OFXTree()
    max_date = datetime.datetime.today() - datetime.timedelta(days=mois*30)
    with open(filename, 'rb') as f:
        parser.parse(f)
        ofx = parser.convert()
        stmts = ofx.statements
        c_amount = float(stmts[0].ledgerbal.balamt)
        c_amount_init = float(stmts[0].ledgerbal.balamt)
        txs = stmts[0].transactions
        data["date"].append(datetime.datetime.today())
        data["amount"].append(c_amount_init)
        data["name"].append("")
        # print(datetime.datetime.today(), c_amount_init, "")
        for i in txs:
            #c_amount -= float(i.trnamt)
            if i.dtposted.replace(tzinfo=pytz.UTC) < max_date.replace(tzinfo=pytz.UTC): continue 
            data["date"].append(i.dtposted)
            data["amount"].append(float(i.trnamt))
            data["name"].append(i.name)
    aggregate(data, 2*c_amount)
    update_with_occ(data, occ, c_amount_init, charges)
    return px.line(data, x="date", y="amount", color="type")

@app.callback(
    Output('example-graph', 'figure'),
    Input('textarea', 'value'),
    Input('repas', 'value'),
    Input('voiture', 'value'),
    Input('divers', 'value'),
    Input('mois', 'value')
)
def get_from_occ(textarea, repas, voiture, divers, mois):
    open("occ.save", "w").write(textarea)
    return get_ofx(ofx_file, textarea, (int(repas), int(voiture), int(divers)), int(mois))

def run():
    fig = get_ofx(ofx_file)
    app.layout = html.Div(children=[
        html.H1(children='Banque CA'),

        dcc.Graph(
            id='example-graph',
            figure=fig
        ),
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    "Afficher", 
                    dcc.Input(id='mois', value='3', type='text'),
                    "mois", 
                ]),
                html.Div(children=[
                    "Charges alimentaires par mois :", 
                    dcc.Input(id='repas', value='1000', type='text')
                ]),
                html.Div(children=[
                    "Charges véhicule par mois :", 
                    dcc.Input(id='voiture', value='500', type='text')
                ]),
                html.Div(children=[
                    "Charges diverses par mois :", 
                    dcc.Input(id='divers', value='0', type='text')
                ]),
            ], 
            style={"float": "right", "width": "45%"}),
            html.Div(children=[
                "Charges fixes :", 
                dcc.Textarea(
                    id='textarea',
                    value=occ,
                    style={'width': '95%', 'height': 200},
                ),
            ],
            style={"overflow": "hidden", "width": "auto"}),
        ],
        style={"overflow": "hidden", "height": "auto"}
        )
    ])


def main(_ofx_file):
    global ofx_file
    ofx_file = _ofx_file
    logging.info("Starting the server...")
    run()
    app.run_server(debug=True)

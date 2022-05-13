import streamlit as st
import pickle
import pandas as pd
import json
import base64
import uuid
import re
import pandas as pd
import numpy as np

import importlib.util

# Modifica el avance y la columna de semestres totales según las condiciones especificadas
def Avance(df):
    notegresados = df[df.Avance != 'Egresado']
    notegresados['Avance'] = notegresados['Avance'].apply(pd.to_numeric, errors='coerce')
    df['Semestres Totales'] = df['Semestres Totales'].apply(pd.to_numeric, errors='coerce')
    df['Semestres Totales'] = df['Semestres Totales'].fillna(10)
    df['Semestres Totales'] = df['Semestres Totales'].astype(int)
    df['Avance'] = df['Avance'].fillna(7)
    df['Avance'].replace({'Egresado':13}, inplace=True)
    df['Avance'] = df['Avance'].apply(pd.to_numeric, errors='coerce')
    df = df[(df['Avance'] > 4)]
    vacante = np.where((df['Semestres Totales']-df['Avance'] > 1) & (df['Avance'] != 13), 'Practicante', 'Profesional')
    df.insert(5, 'Vacante', vacante)
    return df


#Cambiar las variables categoricas a numericas
def Num(df):
    colCategoricas = ['Operaciones-Calidad', 'MTTO-DIMA', 'Comercial-Planeamiento', 'DIGI-SC', 'Resto-Soft']
    dict_categorical = {np.nan:0, 'Do Not Recommend':0, 'Recommend':1, 'Highly Recommend':2}
    for col in colCategoricas:
        df.replace({col: dict_categorical},inplace=True)
        a = 1
    # df.replace({'Actividad Grupal.1': {np.nan : 4}})
    df.replace({'Actividad Grupal.1': {np.nan:0, 1:0, 2:0, 3:1, 4:1, 5:2, 6:2}},inplace=True)
    df['Actividad Grupal.1'] = df['Actividad Grupal.1'].apply(pd.to_numeric, errors='coerce')

    # df.replace({'Ingles' : {np.nan : df['Ingles'].mode()}})
    df.replace({'Ingles': {np.nan :1, 'B2 - High Intermediate':2, 'B1 - Low Intermediate':2,
        'A1 - Low Beginner':1, 'A2 - High Beginner':1, 'C2 - Mastery':2,
        'C1 - Advanced':2, 'False Beginner':1, 'Late hangup':1 }},inplace=True)

    return a,df
#limpieza de variables binarias
def Ortografia(df):
    colBinarias = ['Evaluados Si/No', 'Altamente Recomendado', 'Destacado', 'Ingresados Si/No']
    dict_binary = {np.nan:0, 'No':0, 'no':0, 'NO':0, 'nO':0, 'Sí':1, 'Si':1, 'SÍ':1, 'Lic. Química': 'Química', 'Lic. en Química': 'Química'}
    for col in colBinarias:
        df.replace({col: dict_binary}, inplace=True)
    return df

#Aplicar las condiciones para ver si es apto
def conditions(s):
  if (s['Altamente Recomendado'] == 19):
    return 2
  elif (s['Operaciones-Calidad']==2 or s['MTTO-DIMA']==2 or s['Comercial-Planeamiento']==2 or s['DIGI-SC']==2):
    return 2
  elif (s['Operaciones-Calidad']==1 or s['MTTO-DIMA']==1 or s['Comercial-Planeamiento']==1 or s['DIGI-SC']==1):
    return 1
  elif (s['Resto-Soft'] == 2):
    return 1
  elif (s['Operaciones-Calidad']==0 and s['MTTO-DIMA']==0 and s['Comercial-Planeamiento']==0 and s['DIGI-SC']==0):
    return 0
  elif (s['Actividad Grupal.1'] == 2):
    return 2
  elif (s['Actividad Grupal.1'] == 1):
    return 1
  elif (s['Actividad Grupal.1'] == 0):
    return 0
  elif (s['Ingles'] == 2):
    return 2
  elif (s['Ingles'] == 1):
    return 1

def Drop(df):
    df.drop_duplicates(subset ="ID Candidato",
                     keep = False, inplace = True)
    df = df.drop(['Embajador Ternium', 'Destacado AG', 'Inglés', 'Actividad Grupal', 'Multimodelo Pymetrics',
       'Encuadre de Ingreso', 'Dirección', 'Área', 'Status Académico',
       'Potencial Vigente', 'Información Real/No Real', 'Vacante Postulada',
       'Ingresó', 'VIPS', 'NIPS', 'Apto AG', 'Destacado Pym', 'Universidad'], axis=1)
    df = df.drop(['Fecha Acción', 'PEA', 'Año Acción', 'Periodo Acción', 'País',
       'Tipo de Acción ', 'Acción', 'ID Evento', 'Nombre Evento', 'Apto', 'Apto/No Apto',
       'Institución Acción', 'Referente Ternium', 'Postulados Si/No', 'Perfil Pymetrics',
       'ID Candidato', 'Género', 'Nacionalidad'], axis=1)

    return df


def download_button(object_to_download, download_filename, button_text):
    if isinstance(object_to_download, bytes):
        pass

    elif isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
    # Try JSON encode for everything else
    else:
        object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()
    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub("\d+", "", button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: .25rem .75rem;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = (
        custom_css
        + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br><br>'
    )
    # dl_link = f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}"><input type="button" kind="primary" value="{button_text}"></a><br></br>'

    st.markdown(dl_link, unsafe_allow_html=True)
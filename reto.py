import pickle
from select import select
from tkinter import CENTER
import streamlit as st
import pandas as pd
import numpy as np
import re
from download import download_button, Avance, Drop, Ortografia, Num, conditions
import matplotlib.pyplot as plt

#import plotly.graph_objs as go
st.sidebar.header("MENÚ")
selectbox = st.sidebar.selectbox("Elige una opción",
    ('Principal',"¿Quienes somos?", "Modelo utilizado","Prototipo funcional")
)

st.image(
    "https://media-exp1.licdn.com/dms/image/C4D1BAQFKxQ8tQ8o1MQ/company-background_10000/0/1641312013326?e=2147483647&v=beta&t=VHq8VRdai75HzBLlCxDu-WfVe4ho2vpI95NF5gcQhpg"
)
st.image(
    "data:image/png;base64,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"
, width  = 200)




#Subir archivo
if selectbox == 'Principal':
    st.write("""
        ## Reclutamiento de personal destacado 

        La ciencia de datos es una ciencia multidisciplinaria que ha permitido la toma de decisiones eficientes debido a la analítica predictiva que plantea, atendiendo las necesidades para optimizar diversos procesos con ayuda de técnicas y modelos matemáticos probabilísticos que intentan pronosticar una problemática.
        
        Al utilizar este campo para encontrar personal destacado en las bases de datos de la empresa en el área de Recursos Humanos de la empresa Ternium, será mucho más efectivo y eficiente el proceso para encontrar el candidato con el perfil más adecuado a las especificaciones del cargo y con los mismos valores de la empresa, así como optimizar los recursos que se invierten.

        """)
    st.image(
        "https://revistafortuna.com.mx/wp-content/uploads/2021/04/img_3701.jpg"
    )

if selectbox == "¿Quienes somos?":

    st.header("""
    Equipo CUI
    """)
    st.write("""
    #### Centro Unificado de Ingenieros
    Equipo de plan de optimización en el proceso de selección de personal destacado en la empresa Ternium por medio de analítica predictiva.
    """)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Eder Martínez")
        st.image("eder.jpeg",  width = 150)
        st.text('Científico de Datos, \nDesarrollador web')

    with col2:
        st.subheader("Grisel Porras")
        st.image("joaquin.jpeg", width = 150)
        st.text('Científico de Datos, \nProject manager')

    with col3:
        st.subheader("Giselle Sabbagh")
        st.image("gis.jpeg", width = 150)
        st.text('Científico de Datos, \nUX/UI designer')
    col4, col5,col6,col7 = st.columns(4)
    with col5:
        st.subheader("Joaquin Bravo")
        st.image("gris.jpeg", width = 150)
        st.text('Científico de Datos, \nIng. datos')

    with col6:
        st.subheader("David Rodríguez")
        st.image("david.jpeg", width = 150)
        st.text('Científico de Datos, \nCDO')

elif ( selectbox== 'Modelo utilizado') :

    st.write("""
    ### Modelo utilizado: Gradient Boosting
    El algoritmo de Gradient Boosting se basa en tomar un algoritmo débil como hipótesis, y se hacen una serie de ajustes para mejorar la fuerza de dicho algoritmo. Se podría decir que es un aprendizaje secuencial, puesto que se entrena un modelo con todo el conjunto de entrenamiento y los modelos posteriores se construyen ajustando valores de error residual.
    Este modelo es muy bueno para hacer clasificaciones donde se busca minimizar la pérdida o la diferencia entre el valor de clase real de los datos de entrenamiento y los datos predichos por el modelo. El proceso es muy similar al descenso de gradiente en una red neuronal.
    
    #### Hiperparámetros: 
    {learning_rate = 0.01, max_depth = 1, n_estimators = 250}
    
    Métrica optimizada: _precisión_
    """)
    

elif selectbox == 'Prototipo funcional':
#información general del archivo
    st.write("""
        Esta aplicación web busca asegurar la selección de personal sobresaliente y destacado que aplicaron para
        una vacante en la empresa Ternium. Se quiere que compartan las habilidades técnicas e interpersonales.
    """)
    file = st.file_uploader("Pick a file")
    if file is not None:
        file_container = st.expander("Check your uploaded .csv")
        df = pd.read_csv(file)
        file.seek(0)
        file_container.write(df)
        file_container.write(df.shape)
    else:
        st.info(
            f"""
                Upload a .csv file first. 
                """
        )
        st.stop()
    st.write("""
    ### Información general
    """)
    st.write('Dimensiones de la base de datos:',df.shape)
    st.write('Número de registros de la base de datos:',df.size)

    totalC = np.product(df.shape)

    st.write('Total de registros NaN:', df.isnull().sum().sum())
    mostrar_nan = st.expander("Registros por columna")
    mostrar_nan.write(df.isnull().sum())
    st.text("")

    #prediction = classifier.predict([[]])
    st.write("""
    #### Base de datos limpia

    """)


    df = Drop(df)
    A = []
    for i in range(len(df['Avance'])):
        A.append(i)
    df.insert(0,'ID',A)


    df = Avance(df)
    df = Ortografia(df)
    a,df = Num(df)

    df['Apto'] = df.apply(conditions, axis=1)
    df['Apto suma'] = df['Operaciones-Calidad'] + df['MTTO-DIMA'] + df['Comercial-Planeamiento'] + df['DIGI-SC'] + df['Actividad Grupal.1'] + df['Ingles']

    if a == 1:
        mostrar_limpio = st.expander("Check your .csv clean ")
        mostrar_limpio.write(df)
        CSVButton = download_button(
        df,
        "File.csv",
        "Download CSV clean")


    st.write("""
    #### Visualizaciones

    """)

    colu1, colu2 = st.columns(2)

    with colu1:
      fig, ax = plt.subplots()
      x_values =np.sort(df['Apto suma'].unique())
      y_values = df['Apto suma'].value_counts().tolist()
      plt.bar(x_values, y_values)          #El gráfico
      plt.title('Suma de aptitudes')      #El título
      ax = plt.subplot()                   #Axis
      ax.set_xticks(x_values)             #Eje x
      ax.set_xticklabels(x_values)        #Etiquetas del eje x
      ax.set_xlabel('Suma')  #Nombre del eje x
      ax.set_ylabel('Número de aplicantes')  #Nombre del eje y
      st.pyplot(fig, caption='Sunrise by the mountains')
    with colu2:
      fig1, ax1 = plt.subplots()
      x_values =['No apto','Apto','Destacado']
      y_values = df.Apto.value_counts().tolist()
      plt.bar(x_values, y_values)          #El gráfico
      plt.title('Aplicantes')      #El título
      ax1 = plt.subplot()                   #Axis
      ax1.set_xticks(x_values)             #Eje x
      ax1.set_xticklabels(x_values)        #Etiquetas del eje x
      ax1.set_xlabel('Aptitud')  #Nombre del eje x
      ax1.set_ylabel('Número de aplicantes')  #Nombre del eje y
      st.pyplot(fig1)



    option = st.selectbox(
    'Escoge la categoría',
    ('No aptos', 'Apto', 'Destacados'))
    coll1,coll2 = st.columns(2)
    if (option == 'No aptos'):
        a = df[df['Apto']==0]
        st.write('Aplicantes no aptos:', df['Apto'].value_counts()[0])
        with coll1:
            fig, ax = plt.subplots()
            x_values =np.sort(a['Avance'].unique())
            y_values =a['Avance'].value_counts().to_list()
            plt.bar(x_values, y_values)          #El gráfico
            plt.title('Avance de No aptos')      #El título
            ax = plt.subplot()                   #Axis
            ax.set_xticks(x_values)             #Eje x
            ax.set_xticklabels(x_values)        #Etiquetas del eje x
            ax.set_xlabel('Avance')  #Nombre del eje x
            ax.set_ylabel('Número aplicantes')  #Nombre del eje y
            st.pyplot(fig)



    elif(option == 'Destacados'):
        st.write('Aplicantes destacados:', df['Apto'].value_counts()[2])
        with coll1:
            fig, ax = plt.subplots()
            a = df[df['Apto']==2]
            x_values =np.sort(a['Avance'].unique())
            y_values =a['Avance'].value_counts().to_list()
            plt.bar(x_values, y_values)          #El gráfico
            plt.title('Avance de destacados')      #El título
            ax = plt.subplot()                   #Axis
            ax.set_xticks(x_values)             #Eje x
            ax.set_xticklabels(x_values)        #Etiquetas del eje x
            ax.set_xlabel('Avance')  #Nombre del eje x
            ax.set_ylabel('Número aplicantes')  #Nombre del eje y
            st.pyplot(fig)
    else:
        st.write('Aplicantes aptos:', df['Apto'].value_counts()[1])
        with coll1:
            fig, ax = plt.subplots()
            a = df[df['Apto']==1]
            x_values =np.sort(a['Avance'].unique())
            y_values =a['Avance'].value_counts().to_list()
            plt.bar(x_values, y_values)          #El gráfico
            plt.title('Avance de aptos')      #El título
            ax = plt.subplot()                   #Axis
            ax.set_xticks(x_values)             #Eje x
            ax.set_xticklabels(x_values)        #Etiquetas del eje x
            ax.set_xlabel('Avance')  #Nombre del eje x
            ax.set_ylabel('Número aplicantes')  #Nombre del eje y
            st.pyplot(fig)







    st.write("""
    #### Generación de un sistema para la predicción de personal destacado

    """)

    st.write("""
    Pruebas técnicas

    - Operaciones-Calidad
    - MTTO-DIMA
    - Comercial-Planteamiento
    - DIGI-SC
    """)

    st.write("""
    Pruebas de habilidades personales
    - Resto-Soft
    - Actividad Grupal.1
    """)

    target = 'Ingresados Si/No'
    X = df.drop(['Carrera/Titulación', 'Carrera Gestional', 'Especialidad', 'Vacante',
        'Avance', 'Semestres Totales', 'Evaluados Si/No', 'Altamente Recomendado', 'Correo electrónico', 'Correo institucional', 'Nombres',
       'Apellidos','ID',target ], axis = 1)


        #res = classifier.predict(([[features]]))
    #st.write(final)

    if st.button("Predict"): 
        nombre_archivo='regresorGBOver.pkl'
        archivo_entrada=open(nombre_archivo,'rb')
        classifier=pickle.load(archivo_entrada)
        
        final = pd.DataFrame()
        final['Resultado'] = []
        #final['Resultado'] = np.nan
        #res = classifier.predict(([[1,1,1,1,1,1,1,1,2,13]]))
        #res[0]
        for i in range(len(df)):
            A = []
            for j in range(len(X.columns)):
                A.append(X.iloc[i,j])
            res = classifier.predict(([A]))
            final.loc[i] = [res[0]]
        id_temp = df['ID'].to_list()
        final['ID Candidato'] = id_temp
        



        ingresados = df
        ingresados['Resultado'] = final['Resultado']

        ingresados = ingresados[ingresados['Resultado']==1]
        ingresados.drop('Resultado', inplace=True, axis=1)
        ingresados = ingresados.loc[ingresados['Apto suma'] >=4]


    
        st.write(final)
        st.write(final.size)
        ing = len(ingresados)
        noing = len(final['Resultado']-ing)
        col1, col2, col3 = st.columns(3)
        col1.metric("Posibles ingresados", ing, "")
        col2.metric("Posibles no ingresados", noing, "")
        tasa = str(round((ing/(ing+noing))*100,3))+'%'
        col3.metric("Tasa de ingresados", tasa, "")

        mostrar_final = st.expander("Checar csv de Ingresados ")
        mostrar_final.write(ingresados)

        CSVButton = download_button(
        ingresados,
        "Ingresados.csv",
        "Download resultados")



                

st.text("")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.text(" \n")
    st.image("logo.jpeg",width=50)

with c4:
    st.image("https://esemanal.mx/revista/wp-content/uploads/2019/06/Tec-Monterrey.jpg")

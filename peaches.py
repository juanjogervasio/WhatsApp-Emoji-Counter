# -*- coding: utf-8 -*-
"""
Contador de emoji - Grupo de WhatsApp 

Programa para llevar un conteo del emoji :peach: en el grupo.
El conteo es mensual, debe actualizarse el archivo .txt mes a mes, descargán-
dolo desde la aplicación WhatsApp.
"""

import os
import pandas as pd
import seaborn as sns
from whatstk import WhatsAppChat as wp
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

sns.set_style("darkgrid")

# Importo el emoji de peach, corona y cara triste
ubicacion_emojis = r"files"
emoji1 = pd.read_csv(ubicacion_emojis + r"/Emoji_peach.txt")
emoji2 = pd.read_csv(ubicacion_emojis + r"/Emoji_corona.txt")
emoji3 = pd.read_csv(ubicacion_emojis + r"/Emoji_sad.txt")
peach = emoji1.columns[0]
corona = emoji2.columns[0]
triste = emoji3.columns[0]

# Guardo ubicación de imágenes para gráficos:
winner = r"files/peach_corona.png"
loser = r"files/peach_sad.png"
big_peach = r"files/peach.png"

#Cargo el archivo descargado de WhatsApp
while True:
    descargado = input("Ingrese nombre completo del archivo descargado: ")
    try:   
        chat_wp = wp.from_source(descargado)
    except:
        print("Intente nuevamente. Revise la terminación de archivo.\n")
    else:
        break      
    
#Lo convierto a csv exportándolo a un nuevo archivo
chat_wp.df.to_csv("Nuevo_chat.csv", index = False)

# Importo el chat en .csv a un Dataframe de Pandas y lo elimino
with open("Nuevo_chat.csv", "r", encoding = "utf-8") as archivo:
    Chat = pd.read_csv(archivo)
os.remove("Nuevo_chat.csv")

#Transformo la columna de fecha a datetime
Chat.date = pd.to_datetime(Chat.date)

#Filtro sólo los mensajes con el emoji
Filtrado_emoji = Chat[Chat.message.str.contains(peach, na=False)]

#Filtro desde la fecha de inicio del conteo, que es el 12 de noviembre 2023
inicio = dt.date(2023,11,1)
Filtrado_emoji = Filtrado_emoji[Filtrado_emoji["date"].dt.date >= inicio]

#Creo una columna numérica para contar que ese día se envió un mensaje:
Filtrado_emoji.loc[:,"Conteo"] = 1

#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

#Voy a crear una lista que contenga los datos en intervalos de 30 días

fecha_inicial = Filtrado_emoji.date.iloc[0] #la primera fecha del archivo
fecha_final = Filtrado_emoji.date.tail(1).iloc[0] #la última fecha del archivo

#Cada elemento de la lista es un Dataframe de 30 días
Datos_mensual = []
while fecha_inicial < fecha_final:
    delta = dt.timedelta(days=30)
    condicion_mensual = (Filtrado_emoji.date >= fecha_inicial) & \
                        (Filtrado_emoji.date < fecha_inicial + delta) 
    temp = Filtrado_emoji[ condicion_mensual ]
    if len(temp) != 0:
        Datos_mensual.append(temp)  
    fecha_inicial += delta

#Ya podemos hacer estadísticas mes a mes.

#Voy a separar el correspondiente al último mes (el anterior al mes en curso):
ultimo = Datos_mensual[-2]
    
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

#Graficar la cantidad de emojis enviados cada 30 días

#Creamos el entorno de la figura, y defino las cantidades a graficar.
#Voy a incluir en la figura un gráfico por cada 30 días de datos.
meses = len(Datos_mensual)
ancho = 4
tamaño_y = (meses -1)//ancho + 1
fig, axs = plt.subplots(tamaño_y,ancho, figsize = (5*ancho,5*tamaño_y),
                        layout = "constrained", sharey=True)

#Los datos están en los elementos de Datos_mensual. 
#En la lista 'x' voy a poner los usuarios, en la lista 'y' voy a poner el conteo
#de cada mes. Y también voy a guardar las fechas de cada mes.
lista_x=[]
lista_y=[]
fechas=[]
for mes in Datos_mensual:
    datos = mes.groupby("username").message.count()
    datos_fechas = mes["date"].dt.date 
    lista_x.append(datos.index)
    lista_y.append(datos)
    fechas.append(datos_fechas)

#Vamos a graficar todo junto en la figura que defini antes.

for ax, x, y, fecha in zip(axs.flat, lista_x, lista_y, fechas):
    #ax.set_ylabel("Cacas")
    ax.set_title(str(fecha.min()) + " al " + str(fecha.max()))
    ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    
    
    #Primero unas líneas verticales estilo gráfico de barras
    ax.vlines(x, ymin=0, ymax=y, 
               linewidth = 1, linestyles = "dashed", colors="brown")
    
    #En la altura de cada línea, un emoji distinguiendo ganador y perdedor.
    #Primero voy a cargar las imagenes y despues voy a ubicarlas en la figura
    
    for x0, y0 in zip(x, y):
        if y0 == y.max():
            temp = AnnotationBbox(OffsetImage(plt.imread(winner), zoom=0.05),
                                (x0, y0), frameon=False)
            ax.add_artist(temp)
        elif y0 == y.min():
            temp = AnnotationBbox(OffsetImage(plt.imread(loser), zoom=0.038),
                                (x0, y0), frameon=False)
            ax.add_artist(temp)
        else :
            temp = AnnotationBbox(OffsetImage(plt.imread(big_peach), zoom=0.035),
                                (x0, y0), frameon=False)
            ax.add_artist(temp)
        ax.annotate(f"{y0}", (x0, y0), 
                     textcoords = "offset points", xytext=(0,20), ha = "center")
            
    #Detalles del gráfico
    max_y = max(i.max() for i in lista_y)        
    ax.set_ylim(0, max_y + 4)
    ax.grid(True, axis="y")
#fig.tight_layout()
fig.suptitle("Histórico", fontsize = 25, fontweight = "semibold")
#plt.subplots_adjust(wspace=0.2, 
#                    hspace=0.2)
plt.savefig("historico.png", dpi=300)
#plt.show()

#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

#Generar un mensaje para publicar resultados del último mes.

#Hagamos un mensaje en el que en cada línea imprimimos:
    #1) Fecha inicial
    #2) Fecha final
    #3) Cantidad ordenada de mayor a menor.
  
#Genero el conteo de mensajes de cada usuario:
ultimo_conteo = ultimo.groupby("username").message.count()

#Empiezo por 3). Voy a ordenar la Series de mayor a menor y a armar una lista,
#donde cada elemento sea el texto a imprimir en el mensaje, uno por cada user:

mensaje = []    
for user in ultimo_conteo.sort_values(ascending=False).index:
    temp = user + ": "
    for i in np.arange(ultimo_conteo[user]):
        temp += peach
    if ultimo_conteo[user] == ultimo_conteo.max():
        texto = temp + " " + corona + " " + str(ultimo_conteo[user]) + " " + corona
    elif ultimo_conteo[user] == ultimo_conteo.min():
        texto = temp + " " + str(ultimo_conteo[user]) + " " + triste
    else:
        texto = temp + " " + str(ultimo_conteo[user])
    mensaje.append(texto)
        
#Y ahora ya tengo el mensaje, lo guardo en un archivo .txt:
with open("mensaje.txt", "w", encoding = "utf-8") as archivo:
    print("*CONTADOR*", file = archivo)
    print("*" + str(ultimo.date.min()) + " - " + str(ultimo.date.max()) + "*", 
          file=archivo)
    for texto in mensaje:
        print("*" + texto + "*", file = archivo)

#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------

#Graficar la evolucion diaria del último mes

# Suma acumulada: voy a crear una pivot table que haga el conteo por día, 
# aprovechando la columna Conteo. Será de la forma:
#       username1 | username2 | ...
#   dia1
#   dia2

# Voy a crear una columna para la fecha, en formato dia/mes; si no hay registros
# ese día, completo con 0:
inicio = ultimo.date.min()
fin = ultimo.date.max()

# Reinicio el index para acceder a cada registro de la tabla:
ultimo.reset_index(drop=True, inplace=True)

i=0
while i <= ultimo.index.max():
    registro = ultimo.loc[i, "date"] # Accedo al registro en la ubicación i
    dia_siguiente = inicio + dt.timedelta(days=1)
    if (registro.day == inicio.day) and (registro.month == inicio.month):
        ultimo.loc[i, "fecha"] = registro.strftime("%d/%m")
    elif (registro.day == dia_siguiente.day) and (registro.month == dia_siguiente.month):
        inicio = dia_siguiente
        continue
    elif dia_siguiente < fin:
        for user in ultimo.username.unique():
            ultimo.loc[ultimo.index.max() + 1] = [dia_siguiente, user, np.nan, 0, dia_siguiente.strftime("%d/%m") ]
        inicio += dt.timedelta(days=1)
        continue
    i+=1

# Cambio la columna datetime para quedarme sólo con la fecha
ultimo["date"] = ultimo.date.dt.date
ultimo.reset_index(drop=True, inplace=True)
acumulado = pd.pivot_table(data=ultimo, index="date", columns="username",
                           values="Conteo", aggfunc="sum")

# Completo los días sin peaches con 0
acumulado = acumulado.fillna(0)

# Hago la suma cumulativa de cada columna
acumulado = acumulado.cumsum()

# Grafico los resultados
fig, ax = plt.subplots(figsize = (12,8), layout = "constrained")
for user in acumulado.columns:
    sns.lineplot(data=acumulado,
                    x="date",
                    y=user,
                    label=user,
                    marker="o",
                    ax=ax)
    
#Identificando ganador y perdedor: calculo el valor máximo de cada usuario
maximos = acumulado.max()

#Y ubico las imagenes winner y loser en los puntos correspondientes al más 
#alto o más bajo

x0 = acumulado.index.max() + dt.timedelta(days=1)
for i in acumulado.columns:
    y0 = maximos[i] #el valor máximo de cada usuario
    if y0 == maximos.max():
        temp = AnnotationBbox(OffsetImage(plt.imread(winner), zoom=0.05),
                            (x0, y0) ,frameon=False)
        ax.add_artist(temp)
    elif y0 == maximos.min():
        temp = AnnotationBbox(OffsetImage(plt.imread(loser), zoom=0.04),
                            (x0, y0), frameon=False)
        ax.add_artist(temp)       

    
#Detalles de los ejes y labels del gráfico
ax.legend(loc='best', shadow=True, fontsize='large')
ax.grid(True, axis="both")
ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
ax.set_ylabel("Acumulado 30 días")
ax.set_xlabel("Día")
ax.set_xticks(acumulado.index, labels=[i.strftime("%d/%m") for i in acumulado.index])
ax.set_title("Último conteo", fontweight = "semibold")
plt.xticks(rotation=45)
#plt.show()
plt.savefig("ultimo.png", dpi=300)    

input("Listo! Presione Enter para salir\n")
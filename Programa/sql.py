
from pickle import FALSE
import pandas as pd
from datetime import datetime
import numpy as np

def agregarExcel(original, agregar):
    df = pd.read_excel(original)
    df2 = pd.read_excel(agregar)

    productos = df2['Titulo'].to_list()
    precios = df2['Precio'].to_list()
    print(len(productos))
    ultimo_valor = len(df['Titulo'].to_list())
    col = len(df.axes[1])
    nuevaFecha = datetime.today().strftime('%d-%m-%Y')


    df[nuevaFecha] = np.nan

    for i in range(len(productos)):

        valor_nuevo = df.index[df['Titulo'] == productos[i]].tolist()

        if len(valor_nuevo) == 1:
            df.at[valor_nuevo, nuevaFecha] = (precios[i])
        else:
            df.at[ultimo_valor, 'Titulo'] = productos[i]
            df.at[ultimo_valor, nuevaFecha] = (precios[i])

    df.to_excel("chan.xlsx")
    

def agregarCategoria(original, agregar):
    df = pd.read_excel(original)
    df2 = pd.read_excel(agregar)

    productos = df2['Titulo'].to_list()
    precios = df2['Categoria'].to_list()
    print(len(productos))
    nuevaFecha = datetime.today().strftime('%d-%m-%Y')


    df[nuevaFecha] = np.nan

    for i in range(len(productos)):

        valor_nuevo = df.index[df['Titulo'] == productos[i]].tolist()
        if len(valor_nuevo) == 1:
            df.at[valor_nuevo, 'Categoria'] = precios[i]
        else:
            pass            

    df.to_excel("chan.xlsx",index=False)
    

df= pd.read_excel("chan.xlsx")

print(df.dtypes)

#agregarCategoria("chan.xlsx","categorico.xlsx")
agregarExcel("chan.xlsx", "Archivos/" +datetime.today().strftime('%d-%m-%Y')+".xlsx")
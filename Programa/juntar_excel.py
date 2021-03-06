
import pandas as pd
from datetime import datetime
from pip import main
import numpy as np
import main
import drive

def agregarExcel(original, agregar):
    df = pd.read_excel(original)
    df2 = pd.read_excel(agregar)

    productos = df2['Titulo'].to_list()
    precios = df2['Precio'].to_list()
    ultimo_valor = len(df['Titulo'].to_list())
    nuevaFecha = fecha


    df[nuevaFecha] = np.nan

    for i in range(len(productos)):

        valor_nuevo = df.index[df['Titulo'] == productos[i]].tolist()

        if len(valor_nuevo) == 1:
            df.at[valor_nuevo, nuevaFecha] = (precios[i])
        else:
            df.at[ultimo_valor, 'Titulo'] = productos[i]
            df.at[ultimo_valor, nuevaFecha] = (precios[i])

    df.to_excel("Precios historicos.xlsx")
    

def agregarCategoria(original, agregar):
    df = pd.read_excel(original)
    df2 = pd.read_excel(agregar)

    productos = df2['Titulo'].to_list()
    precios = df2['Categoria'].to_list()
    
    nuevaFecha = agregar


    df[nuevaFecha] = np.nan

    for i in range(len(productos)):

        valor_nuevo = df.index[df['Titulo'] == productos[i]].tolist()
        if len(valor_nuevo) == 1:
            df.at[valor_nuevo, 'Categoria'] = precios[i]
        else:
            pass            

    df.to_excel("Precios historicos.xlsx",index=False)
    

#agregarCategoria("chan.xlsx","categoria_productos.xlsx")
fecha =  datetime.today().strftime('%d-%m-%Y')
main.ejecutar()


agregarExcel("Precios historicos.xlsx", "Archivos/" + fecha +".xlsx")

drive.actualizar()
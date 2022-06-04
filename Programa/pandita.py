from math import radians
from traceback import print_tb
import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_excel("chan.xlsx")


df['Aumento'] = df[datetime.today().strftime('%d-%m-%Y')]/df['07-05-2022']

df = df[df[datetime.today().strftime('%d-%m-%Y')].notna()]


copy = df.sort_values(by=['Categoria','Titulo'])

copy.to_excel("ordenado.xlsx",index=False)

categorias = copy.groupby(["Categoria"])
print(categorias.Aumento.mean() )

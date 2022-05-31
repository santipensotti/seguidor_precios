
from traceback import print_tb
from bs4 import BeautifulSoup as soup 
from urllib.request import Request, urlopen
import re
import pandas as pd
import concurrent.futures
from datetime import datetime

begin_time = datetime.now()

numero = 0
lista = []
def main(numero):
    pag_url = f"https://www.cotodigital3.com.ar/sitios/cdigi/browse?Nf=product.endDate%7CGTEQ+1.651536E12%7C%7Cproduct.startDate%7CLTEQ+1.651536E12&No={numero}&Nr=AND%28product.language%3Aespa%C3%B1ol%2Cproduct.sDisp_200%3A1004%2COR%28product.siteId%3ACotoDigital%29%29&Nrpp=72"
    req = Request(pag_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    pag_soup = soup(webpage,"html.parser")

    hello = pag_soup.find_all("div","descrip_full")
    precio = pag_soup.find_all("span","atg_store_newPrice")
    a = 0
    b = 0

    
    for i in precio:
        a = a + 1
        if i.parent.parent.find("div","info_discount"):
                s = [str(s) for s in re.findall(r'-?\d+.?\d+\,?\d*',i.contents[2])  ]  
                diccionario = {
                    'Titulo' :hello[b].text,
                    'Precio' :str(s[0])
                }
                lista.append(diccionario)            
                b = b + 1

        else:
            pass

    

def cantidad():
    pag_url = f"https://www.cotodigital3.com.ar/sitios/cdigi/browse?Nf=product.endDate%7CGTEQ+1.651536E12%7C%7Cproduct.startDate%7CLTEQ+1.651536E12&No={numero}&Nr=AND%28product.language%3Aespa%C3%B1ol%2Cproduct.sDisp_200%3A1004%2COR%28product.siteId%3ACotoDigital%29%29&Nrpp=72"
    req = Request(pag_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    pag_soup = soup(webpage,"html.parser")
    cantidad_productos = pag_soup.find(id ="resultsCount").text
    return cantidad_productos


cantidad_paginas = cantidad()
url = []
for i in range(0, int(cantidad_paginas),72):
    url.append(i)


with concurrent.futures.ThreadPoolExecutor() as executor:
    #Ejecuto varios procesos a la vez asi se reduce el tiempo de ejecucion
    executor.map(main, url)


df = pd.DataFrame(lista)
print(df.head()) 


df.to_excel(datetime.today().strftime('%d-%m-%Y')+".xlsx",index=False)
print(datetime.now() - begin_time)

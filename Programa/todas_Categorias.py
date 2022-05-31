from encodings import utf_8
from traceback import print_tb
from bs4 import BeautifulSoup as soup 
from urllib.request import Request, urlopen
import re
import pandas as pd
import concurrent.futures
from datetime import datetime
from requests.utils import requote_uri



def main():
    pag_url= "https://www.cotodigital3.com.ar/sitios/cdigi/browse"
    req = Request(pag_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    pag_soup = soup(webpage,"html.parser")
    todas = []
    categorias = pag_soup.find('ul',{'class','atg_store_facetOptions'})
    diccionario = {}
    b = 1
    for i in categorias:
        if b %2 == 0 :
            nombres =i.text.strip()
            nombres = ''.join([i for i in nombres if not i.isdigit()]).encode('utf-8')
            diccionario ={
                'Categoria' : nombres[:-3],
                'Link' : "https://www.cotodigital3.com.ar"+ str(i.a.get('href'))
            }
            todas.append(diccionario)

        b = b +1
    return todas

sub_categoria = []

def cantidad():
    pag_url = f"https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-cereales/_/N-ukd5id"
    req = Request(pag_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    pag_soup = soup(webpage,"html.parser")
    cantidad_productos = pag_soup.find(id ="resultsCount").text
    return cantidad_productos


def category(link,catPadre):
    pag_url= requote_uri(link)
    req = Request(pag_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    pag_soup = soup(webpage,"html.parser")
    categorias = pag_soup.find('ul',{'class','atg_store_facetOptions'})
    diccionario = {}

    b = 1
    for i in categorias:
        cantidad_productos = pag_soup.find(id ="resultsCount").text

        if b %2 == 0 :
            nombres =''.join([i for i in i.text.strip() if not i.isdigit()])
            link = "https://www.cotodigital3.com.ar"+ str(i.a.get('href'))

            diccionario ={
                'Categoria' : catPadre.decode("utf-8") ,
                'Subcategoria' : nombres[:-3],
                'Link' :link ,
                'Cantidad Productos' : cantidad_productos
            }
            sub_categoria.append(diccionario)
            recorrerSubCat(link,nombres[:-3])
        b = b +1
    
categorias_principales = main()
def recorrer_cat_prin():
    for i in categorias_principales:
        category(i['Link'], i['Categoria'])

    df = pd.DataFrame(sub_categoria)
    df.to_excel("CATEGORIASTODAS.xlsx")

productos_y_categoria = []

def buscarProductos(link, categoria):
    pag_url= requote_uri(link)
    req = Request(pag_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    pag_soup = soup(webpage,"html.parser")
    hello = pag_soup.find_all("div","descrip_full")

    products = pag_soup.find_all('div',{'class':'descrip_full'})
    diccionario = {}
    precio = pag_soup.find_all("span","atg_store_newPrice")
    b = 0

    for i in precio:
        
        if i.parent.parent.find("div","info_discount"):
            s = [str(s) for s in re.findall(r'-?\d+.?\d+\,?\d*',i.contents[2])  ]  
            diccionario = {
                'Titulo' :hello[b].text,
                'Precio' :str(s[0]),
                'Categoria' : categoria
            }
            b = b +1    
            productos_y_categoria.append(diccionario)


def recorrerSubCat(link, categoria):
    print('Recorriendo')
    if categoria is not None :
        categorias = categoria
    else:
        categorias = ""
    pag_url= requote_uri(link)
    req = Request(pag_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    pag_soup = soup(webpage,"html.parser")
    cantidad_productos = pag_soup.find(id ="resultsCount").text
    link_siguiente = pag_soup.find('a', {'title' : 'Ir a página 2'})
    buscarProductos(link, categorias)
    if link_siguiente is not None :
        link_siguiente = "https://www.cotodigital3.com.ar" + link_siguiente['href']

        buscarProductos(link_siguiente[:-2] + cantidad_productos, categorias)

    
recorrer_cat_prin()
print(len(productos_y_categoria))

dfs = pd.DataFrame(productos_y_categoria)
dfs.to_excel("categorico.xlsx")
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
import sys 
import pickle 
# Librerias propias
from tools.html.saveDocuments import saveHTML
import datetime
import procesaHTML
import procesaHTML2

def cargaSitio(page,filepath):
    """ En una pagina dada, se carga hasta el final y se baja.
    valores:.
    page: String que tiene la URL a bajar.
    tituloSite: String, solo referencia para el nombre del sitio.
    usuario: String, para abrir y guardar cookies."""

    ### INICIALIZANDO VALORES ###
    # Path donde guardara el sitio una vez cargado.
    #guardaInfo = '_files/' + 'vuelos' + tituloSite + '.html'
    guardaInfo = filepath
    # Pagina para hacer el scraping
    paginaUsuarios = page
    userAgent="Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"
    # Inicio el navegador          
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (userAgent)
    service_args = ['--proxy=localhost:8080']
    driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=service_args)
    # Inicio el navegador
    # Cargo la pagina
    driver.get(paginaUsuarios)
    time.sleep(20)
    ### SALVO LA PAGINA ### 
    saveHTML(driver.page_source, guardaInfo)
    driver.close()

def makeURL(fecha,dias,iterador):
    """ Metodo que se encarga de construir la url para buscar los vuelos.
    Recibe tres parametros
    `fecha` =  de tipo (string) sera la fecha inicial de partida de viaje. 
    `dias` =  de tipo (int) son la cantidad de dias que se desea ir de viaje
    `iterador` = de tipo (int) el incremental para ir cambiando la fecha
    inicial. """
    # baseURL, en este caso ya construyo ciudad orig/dst pero en el futuro se
    # puede modificar. 
    baseURL="http://www.despegar.com.ar/shop/flights/results/roundtrip/EZE/RIO/"
    otros="/1/0/0?from=SB"
    # Seteo la fecha inicial
    format="%Y-%m-%d"
    fInicial=datetime.datetime.strptime(fecha,format)

    one_day = datetime.timedelta(days=1) # necesario para el delta de la fech
    fIda= fInicial + one_day * iterador
    # Seteo la fecha de regreso
    fVuelta=fIda + one_day * dias
    #return (baseURL + str(fIda) + "/" + str(fVuelta) + otros)
    return (baseURL + fIda.strftime(format) + "/" + fVuelta.strftime(format) + otros)

#cargaSitio("http://www.despegar.com.ar/shop/flights/results/roundtrip/EZE/RIO/2017-02-13/2017-02-24/1/0/0?from=SB","Despegar","Empty") 

def flying(fecha, dias, x):
    url=makeURL(fecha,dias,x)
    filepath='_files/vuelos-despegar_' + str(x)+ str(dias) + '.html'
    #print(url)
    print(filepath)
    cargaSitio(url,filepath)
    #procesaHTML.procesaHTML(filepath, url)
    procesaHTML2.procesaHTML(filepath, url)
    time.sleep(10)


dias = 12
fecha="2017-02-10"
for x in range(0, 6):
    flying(fecha, dias, x*7)
    flying(fecha, dias - 1, x*7)
    flying(fecha, dias + 1, x*7)
    for y in range(1,3):
        flying(fecha, dias, (x*7)+y)
        flying(fecha, dias -1, (x*7)+y)
        flying(fecha, dias + 1, (x*7)+y)



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

def cargaSitio(page,tituloSite,usuario):
    """ En una pagina dada, se carga hasta el final y se baja.
    valores:.
    page: String que tiene la URL a bajar.
    tituloSite: String, solo referencia para el nombre del sitio.
    usuario: String, para abrir y guardar cookies."""

    ### INICIALIZANDO VALORES ###
    # Path donde guardara el sitio una vez cargado.
    guardaInfo = '_files/' + 'vuelos' + tituloSite + '.html'
    # Pagina para hacer el scraping
    paginaUsuarios = page
    userAgent="Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"
    # Inicio el navegador          
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (userAgent)
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    # Inicio el navegador
    # Cargo la pagina
    driver.get(paginaUsuarios)
    time.sleep(20)
    ### SALVO LA PAGINA ### 
    saveHTML(driver.page_source, guardaInfo)
    driver.close()

def makeURL(aaaa,mm,dd,dias):
    baseURL="http://www.despegar.com.ar/shop/flights/results/roundtrip/EZE/RIO/" 
    otros="/1/0/0?from=SB"
    fIda= datetime.date(aaaa,mm,dd) 
    one_day = datetime.timedelta(days=1)
    fVuelta=fIda + one_day * dias
    return (baseURL + str(fIda) + "/" + str(fVuelta) + otros)

#cargaSitio("http://www.despegar.com.ar/shop/flights/results/roundtrip/EZE/RIO/2017-02-13/2017-02-24/1/0/0?from=SB","Despegar","Empty") 
dia = 15
for salida in 1,2,3,4: 
    dia = dia + salida
    url=makeURL(2017,2,dia,12)
    fecha= str(datetime.date(2017,2,dia))
    filepath='_files/vuelos-despegar_' + fecha + '.html'
    print(url)
    print(filepath)

#makeURL(2017,2,20,12)


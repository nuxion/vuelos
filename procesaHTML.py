"""
    procesaHTML toma un archivo html, y aisla los usuarios
    para finalmente guardarlo en algun formato, db, csv, etc.
"""
# Librerias
import lxml.html
import re
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen 


def procesaHTML(pathHTML):
    """ Metodo que recibe el path de un html y extrae nombre de la persona.
    y url del perfil en facebook, devuelve un diccionario o lista.
    Valores `pathHTML`: String, path a nivel filesyste de donde esta el archivo html."""
    #archivo= lxml.html.parse(pathHTML)
    ## @ hace referencia a atributos de una clase, en este caso div
    #precios= archivo.xpath('//span[@class="amount price-amount"]/text()') 
    ##nombres = archivo.xpath('//div[@class="_gll"]//div[@class="_5d-5"]/text()')
    ##print(type(precios))
    #f=open(pathHTML,'r')
    datos = open("_files/vuelosDespegar.html",'r').read() 
    soup = BeautifulSoup(datos,"html.parser")
    #tablaprecios = soup.find_all('div',{'class':''})
    #tablaprecios = soup.find_all('trip-route')
    infoyprecios = soup.find_all('div',{'class':'cluster-content flights-cluster'})
    #print(infoyprecios)
    for  tabla in infoyprecios:
        tipo=tabla.find('span', {'class':'route-info-item route-info-item-type type'})

        precio=tabla.find('span', {'class':'amount price-amount'}).getText()

        enPesos=float(precio)
        #if enPesos < 9.5:
        #    print (enPesos)
        tripRoute = tabla.find_all('trip-route')
        for x,trip in enumerate(tripRoute):
            #tipo=trip.find('span', {'class':'route-info-item route-info-item-type type'}).getText()
            headInfo=trip.find('span', {'class':'route-info'}).getText()
            headFormated=(headInfo.replace("\n", " "))
            print(headFormated)
            sale=trip.find('span',{'class':'hour'}).getText()
            duracion=trip.find('span',{'class':'best-duration'}).getText()
            duracion=duracion.replace("\n", " ")
            print("Sale a las: " + sale + "hs") 
            print("Duracion: " + duracion + "hs") 
            print ("-------------------------")
        print ("Valor del vuelo final: $" + precio)
        print("==========================")
procesaHTML("file:///_files/vuelosDespegar.html")

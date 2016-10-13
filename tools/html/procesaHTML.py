"""
    procesaHTML toma un archivo html, y aisla los usuarios
    para finalmente guardarlo en algun formato, db, csv, etc.
"""
# Librerias
import lxml.html
import re
import csv

# Variables generales y temporales
htmlpath="/home/nuxion/Projects/caradelibro/_files/usuariosdosorillas.html"
#htmlpath="/home/nuxion/Projects/caradelibro/_files/usuariosdosorillas.html" 
csvfile="/home/nuxion/Projects/caradelibro/_files/usuariosdosorillas.csv"

def toCSV(lista,pathcsv):
    """
    Metodo que  guarda en un csv los valores de una lista.
    --------
    Parametros:
        `lista` es un List de pyhton.
        `pathcsv` ruta y nombre de archivo donde guardara el csv."""
    with open(pathcsv, "w") as f:
        # Seteo formato de archivo
        writer = csv.writer(f, delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL,lineterminator='\n') 
        # escribo la primer fila que seria el titulo de cada columna
        writer.writerow(['name', 'ID', 'usuario', 'uri'])
        writer.writerows(lista)
        # Se reemplaza el for, se puede escribir directamente la lista
        # info de:
            # http://stackoverflow.com/questions/14037540/writing-a-python-list-of-lists-to-a-csv-file
        #for item in lista:
        #   writer.writerow([item[0], item[1], item[2]])

def cleanURL(urltext):
    """
    Metodo que mediante RE limpia la url para quedarse con el  nombre de usuario.
    En caso de que sea un numero: profile.php simplemente deja un ID en el campo.
    Parametros: `urltext` recibe el path del html con el que debe trabajara.
    Devuelve un valor tu STRING con el string para agregar en la lista.
    """

    # Precompilo expresiones regulares a usar
    ifProfile=re.compile('profile\.php')
    nombreUsuario=re.compile('(?<=com\/)(.*)(?=\?ref)')
    idUsuario= re.compile('[0-9]+')
    #print (urltext)
    # Es necesario chequear con ifProfile que no sea un ID. 
    if ifProfile.search(urltext) is None:
        m=nombreUsuario.search(urltext)
        toTheList=m.group(0)
        #print(m)
    else:
        # Deprecado, da error porque el join no puede hacerse
        # sobre numeros
        m=idUsuario.search(urltext)
        # Como el ID es un numero lo paso a string:
        #letras=str(m.group(0))
        toTheList=int(m.group(0))

        #toTheList='ID'
        #toTheList=letras
    return toTheList
    #return m.group(0)

def procesaHTML(pathHTML):
    """ Metodo que recibe el path de un html y extrae nombre de la persona.
    y url del perfil en facebook, devuelve un diccionario o lista.
    Valores `pathHTML`: String, path a nivel filesyste de donde esta el archivo html."""

    archivo= lxml.html.parse(pathHTML)
    # @ hace referencia a atributos de una clase, en este caso div
    profiles= archivo.xpath('//div[@class="_gll"]//a/@href')
    nombres = archivo.xpath('//div[@class="_gll"]//div[@class="_5d-5"]/text()')
    # list of things
    lot = []
    # Utilizo zip para recorrer dos listas a la vez.
    for x, z in zip(nombres, profiles):
        # Defino una lista temporal 
        tempLOT=[]
        # Agrego los dos elementos en la lista
        tempLOT.append(x) # Primero el nombre del usuario
        # Luego necesito limpiar la url(z), e identificar si tengo el ID
        # o el nombre de usuario
        urlLimpia=cleanURL(z)
        #print (type(urlLimpia))#debug
        # tal vez se podria optimizar si hacer una funcion aparte para limpiar
        # url
        if type(urlLimpia)==int:
            urlLimpia=str(urlLimpia)
            tempLOT.append(urlLimpia)
            tempLOT.append("name")
        else:
            tempLOT.append("ID")
            tempLOT.append(urlLimpia)
        #Deprecado: ahora me interesa obtener y guardar los dos valores
        #tempLOT.append(cleanURL(z)) # me quedo con el nombre o id de usuario
        tempLOT.append(z)
        # Agrego la lista temporal a lista final
        lot.append(tempLOT)
    # A modo prueba separo en ;
    # tomado de
    # http://stackoverflow.com/questions/44778/how-would-you-make-a-comma-separated-string-from-a-list
    #for x in lot:
    #    myString = ";".join(x)
    #    print (myString) 
    return lot

#### MAIN ####
# Esta funcion devuelve una lista con los usuarios ya procesados
lista=procesaHTML(htmlpath)
toCSV(lista,csvfile)

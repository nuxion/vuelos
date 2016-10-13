import sys

def saveHTML(page,nombreArch):
    """ Metodo que salva en archivo el sitio cargado.
    params:  string, nombrepatharchivo
    """
    page_text = (page).encode('utf-8') 
    textFile = open(nombreArch, 'wb')
    textFile.write(page_text)
    textFile.close()

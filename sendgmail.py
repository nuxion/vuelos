import smtplib  
#from configparser import ConfigParser 
import configparser

def cargarCuenta(): 
    config = configparser.ConfigParser()
    config.read('config.properties')
    sender = config.get('SMTP', 'smtp.username')
    password = config.get('SMTP', 'smtp.password')
    listaTO=config.get('senders','senders.lista') 
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = listaTO
    msg['Subject'] = "VUELOS DESPEGAR" 
    body="Se encontrddo"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, listaTO, text)
    server.quit()

#cargarCuenta() 
def sendMail(texto): 
    config = configparser.ConfigParser()
    config.read('config.properties')
    sender = config.get('SMTP', 'smtp.username')
    password = config.get('SMTP', 'smtp.password')
    listaTO=config.get('senders','senders.lista')

    TO = listaTO
    SUBJECT = 'Vuelos en Despegar'
    TEXT = texto

    # Gmail Sign In
    gmail_sender = sender
    gmail_passwd = password
#
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                     'From: %s' % gmail_sender,
                     'Subject: %s' % SUBJECT,
                     '', TEXT])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print ('error sending mail')

    server.quit() 

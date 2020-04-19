# -*- coding: utf-8 -*-
from scrapy import Selector
import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pickle
import os
import time


def contentAsDataframe(data):
   
    # =============================================================================
    # leggo contenuto pagina HTML
    # =============================================================================
    html = requests.get(data['url']).content    
    
    # =============================================================================
    # estrazione informazioni 
    # =============================================================================    
    sel = Selector( text = html )
    
    # =============================================================================
    # DIV
    # =============================================================================
    divList = sel.xpath(data['div'])

    # =============================================================================
    # CONTENUTI
    # =============================================================================
    contenuti = divList.xpath(data['contenuti']).extract()
    contenuti = [i.strip() for i in contenuti]
    
    # per sicurezza, rendo univoci i valori trovati
    contenuti = list(set(contenuti))
    
    # =============================================================================
    # TITOLI
    # =============================================================================
    titoli = []
    
    if(data['titoli'] != 'false'):
        titoli = divList.xpath(data['titoli']).extract()
        titoli = [t.strip() for t in titoli]
    else:
        for c in contenuti:
            temp = c.split(' ')
            temp = temp[:data['nWords']]
            temp = ' '.join(temp)
            titoli.append(temp)
    
    # =============================================================================
    # LINK
    # =============================================================================
    link = []
    if(data['link'] != 'false'):
        link = divList.xpath(data['link']).extract()
    else:
        for c in contenuti:
            link.append(data['url'])
    
    # rendo univoci
    link = list(set(link))
    
    # =============================================================================
    # DATAFRAME
    # =============================================================================
    df = pd.DataFrame()
    df['titolo'] = titoli
    df['contenuto'] = contenuti
    df['link'] = link        

    return df

def sendMail(data, esito):
# =============================================================================
#     import smtplib
#     from email.mime.multipart import MIMEMultipart
#     from email.mime.text import MIMEText
# =============================================================================

    msg = MIMEMultipart()
    msg['Subject'] = 'Alert'
    msg['From'] = data['mailFrom']
    msg['To'] = ', '.join(data['mailTo'])       
    body = "***PAGINA CAMBIATA***\n\n" + esito + "\n\n" + data['url']
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.federicocattai.it', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
                  
    #Next, log in to the server
    server.login("info@federicocattai.it", "roygbiv76")
    
    #Send the mail        
    server.sendmail(data['mailFrom'], data['mailTo'], msg.as_string())
    server.quit()
    
def sendHTMLmail(data, esito):
        
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Alert ' + data['fileName']
    msg['From'] = data['mailFrom']
    msg['To'] = ', '.join(data['mailTo'])
    
    # Create the body of the message (a plain-text and an HTML version).
    text = 'mail generata automaticamente'
    

    # carico html da file template
    t = open("_App/_mailTemplate.html", "r")
    html = t.read()
    t.close()

    html = html.replace("#link#", data['url'])   
    html = html.replace("#result#", esito)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    
    server = smtplib.SMTP('smtp.federicocattai.it', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
                
    #Next, log in to the server
    server.login("info@federicocattai.it", "roygbiv76")

    #Send the mail        
    server.sendmail(data['mailFrom'], data['mailTo'], msg.as_string())
    server.quit()

    return True

def process(data):
    # =============================================================================
    # scraping
    # ottengo un pandas df
    # =============================================================================
    tbl = contentAsDataframe(data)
    
    
    # =============================================================================
    # htmlOut
    # ricostruisco dal pandas un html formattato
    # =============================================================================
    htmlOut = ''
    for index, row in tbl.iterrows():
            htmlOut += '<a href="'+row['link']+'">'+row['titolo']+'</a>'
            htmlOut += '<p>'+row['contenuto']+'</p>'
            htmlOut += '<br>'
    
    # =============================================================================
    # carico file di confronto
    # =============================================================================
    filePath = data['appPath'] + '/_Results/' + data['fileName'] + '.zzz'
    
    # se esiste, leggo risultato precedente
    if os.path.exists(filePath):
        f = open(filePath, 'rb')
        y = pickle.load(f)
        f.close()
    else:
        y = pd.DataFrame()
        
        
    # =============================================================================
    # confronto
    # =============================================================================
    esito = tbl.to_string() == y.to_string()
    
    # =============================================================================
    # output
    # =============================================================================
    timestamp = time.strftime("%d/%m/%Y %H:%M:%S")
    
    if esito:
        print(timestamp + ' ' +  data['fileName'] + ': nessun cambiamento')
    
    else:
        
        if y.shape[0]>0:
            print('***PAGINA CAMBIATA***')
            
            # MAIL
            sendHTMLmail(data, htmlOut)
    
        # =============================================================================
        #     # salvo il nuovo risultato
        # =============================================================================
        if os.path.exists(filePath):
            os.remove(filePath)
        
        f = open(filePath, 'ab')
        pickle.dump(tbl, f, protocol=2)
        f.close()

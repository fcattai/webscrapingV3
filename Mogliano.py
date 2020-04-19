# -*- coding: utf-8 -*-

# =============================================================================
# load
# =============================================================================
import _App.libreria as lib
from os.path import dirname

# =============================================================================
# config data
# =============================================================================
configData = {
        'appPath': dirname(__file__),
        'url':'http://www.comune.mogliano-veneto.tv.it/index.php/concorsi.html',
        'div': '//table[@id="greytable"]/tbody/tr/td',
        'titoli': 'false',
        
        # il numero di parole da prendere al contenuto per creare il tiutolo mancante
        'nWords': 5,
        'contenuti': './p[2]/strong/text()',
        'link': 'false',
        
        # nome del file da usare per il monitoraggio
        'fileName': 'Mogliano',
        
        # indirizzo di invio mail
        'mailFrom': 'info@federicocattai.it',
        
        #destinatari mail, va inserito come LIST!
        # 'mailTo': ["federico.cattai@gmail.com", "maria_andrea_peruch@hotmail.com"],
        'mailTo': ["federico.cattai@gmail.com"]
        }

lib.process(configData)
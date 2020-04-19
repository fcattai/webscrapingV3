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
#        'appPath': dirname(__file__),
        'appPath': '/Volumes/Data/OneDrive/Python/WebScrapingV2',
        'url':'https://mirano.trasparenza-valutazione-merito.it/web/trasparenza/papca-g/-/papca/igrid/46319/41272',
        'div': '//tr[contains(@class, "master-detail-list-line")]',
        'titoli': 'false',
        
        # il numero di parole da prendere al contenuto per creare il tiutolo mancante
        'nWords': 5,
        'contenuti': './td[contains(@class, "oggetto text")]/text()',
        'link': './td[@class="actions"]/a[1]/@href',
        
        # nome del file da usare per il monitoraggio
        'fileName': 'Mirano',
        
        # indirizzo di invio mail
        'mailFrom': 'info@federicocattai.it',
        
        #destinatari mail, va inserito come LIST!
        # 'mailTo': ["federico.cattai@gmail.com", "maria_andrea_peruch@hotmail.com"],
        'mailTo': ["federico.cattai@gmail.com"]
        }

lib.process(configData)

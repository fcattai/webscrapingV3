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
        'url':'https://www.aziendazero.concorsieavvisi.it/index.cfm?action=trasparenza.concorso&id=159',
#        'div': '//tr[contains(@class, "master-detail-list-line")]',
        
        'div': '//div[@class="allegus"]//a[@class="spostatut"]',
        
        'titoli': 'false',
        
        # il numero di parole da prendere al contenuto per creare il titolo mancante
        'nWords': 1,
#        'contenuti': './td[contains(@class, "oggetto text")]/text()',
        'contenuti': '//div[@class="allegus"]//a[@class="spostatut"]/text()',
        'link': '//div[@class="allegus"]//a[@class="spostatut"]/@href',
        
        # nome del file da usare per il monitoraggio
        'fileName': 'Azero',
        
        # indirizzo di invio mail
        'mailFrom': 'info@federicocattai.it',
        
        #destinatari mail, va inserito come LIST!
        # 'mailTo': ["federico.cattai@gmail.com", "maria_andrea_peruch@hotmail.com"],
        'mailTo': ["federico.cattai@gmail.com"]
        }

lib.process(configData)

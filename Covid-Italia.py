''' 
    FRANCESCO GERRATANA WWW.NEXTECHNICS.COM 2020
    Scraping with python maps arcgis COVID-19 Italia.
'''
import urllib 
import requests
import json
import csv
from operator import itemgetter
from tabulate import _table_formats, tabulate
import sys
import os
import subprocess

def covidscrapy(urls,features,attr,colums):
    response = urllib.request.urlopen(urls)
    data = json.loads(response.read())
    my_list = []
    
    for each in data[features]:
        r1 = each[attr][colums[0]]#['denominazione_regione']
        r2 = each[attr][colums[1]]#['totale_casi']
        r3 = each[attr][colums[2]]#['totale_positivi']
        r4 = each[attr][colums[3]]#['terapia_intensiva']
        r5 = each[attr][colums[4]]#['deceduti']
        r6 = each[attr][colums[5]]#['dimessi_guariti']
        r7 = each[attr][colums[6]]#['tamponi']

        my_list.append((r1,r2,r3,r4,r5,r6,r7))
        
    return sorted(my_list, key=itemgetter(1),reverse=True)

url = r"https://services6.arcgis.com/L1SotImj1AAZY1eK/arcgis/rest/services/dpc_regioni__covid_19_new2/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&=totale_casi"                                

db = covidscrapy(url, 
                'features',
                'attributes',
               ['denominazione_regione', \
                'totale_casi', \
                'totale_positivi', \
                'terapia_intensiva', \
                'deceduti', \
                'dimessi_guariti', \
                'tamponi'])

header = ["REGIONE","TOT CASI","TOT POSITIVI","TOT TER.INTENSIVA","TOT DECEDUTI","TOT GUARITI","TOT TAMPONI"]
print(tabulate(db,header,tablefmt="grid"))

with open("file.txt", "w") as output:
    output.write(str(tabulate(db,header,tablefmt="grid")))

subprocess.call(["cmd", "/k", "start", "", "file.txt"], stderr=subprocess.STDOUT) 






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
import pandas as pd
from pandas import DataFrame
from matplotlib import pyplot as plt


def covidscrapy(urls,colums):
    response = urllib.request.urlopen(urls)
    data = json.loads(response.read())
    my_list = []

    for each in data:
            r1  = each[colums[0]]#['denominazione_regione']
            r2  = each[colums[1]]#['totale_positivi']
            r3  = each[colums[2]]#['terapia_intensiva']
            r4  = each[colums[3]]#['totale_ospedalizzati']
            r5  = each[colums[4]]#['isolamento_domiciliare']
            r6  = each[colums[5]]#['totale_positivi']
            r7  = each[colums[6]]#['variazione_totale_positivi']
            r8  = each[colums[7]]#['nuovi_positivi']
            r9  = each[colums[8]]#['dimessi_guariti']
            r10 = each[colums[9]]#['deceduti']
            r11 = each[colums[10]]#['casi_da_sospetto_diagnostico']
            r12 = each[colums[11]]#['casi_da_screening']
            r13 = each[colums[12]]#['totale_casi']
            r14 = each[colums[13]]#['tamponi'] 
            r15 = each[colums[14]]#['casi_testati']

            my_list.append((r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,))
 
    return sorted(my_list, key=itemgetter(1),reverse=True)

url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json"

db = covidscrapy(url,\
               ['denominazione_regione', \
                'totale_positivi', \
                'terapia_intensiva', \
                'totale_ospedalizzati', \
                'isolamento_domiciliare', \
                'totale_positivi', \
                'variazione_totale_positivi', \
                'nuovi_positivi', \
                'dimessi_guariti', \
                'deceduti', \
                'casi_da_sospetto_diagnostico', \
                'casi_da_screening', \
                'totale_casi', \
                'tamponi', \
                'casi_testati'])

header = ['REGIONE',\
          'TOT POSITIVI',\
          'TOT T.INTENSIVA',\
          'TOT OSPEDALIZZATI',\
          'TOT I.DOMICILIARE',\
          'TOT POSITIVI',\
          'VAR TOT POSITIVI',\
          'TOT POSITIVI',\
          'TOT GUARITI',\
          'TOT DECEDUTI',\
          'TOT SOSPETTO DIAGNOSTICO',\
          'TOT DA SCREENING',\
          'TOT CASI',\
          'TOT TAMPONI',\
          'TOT TESTATI']		  
		  
	  
print(tabulate(db,header,tablefmt="grid"))


with open("file.txt", "w") as output:
    output.write(str(tabulate(db,header,tablefmt="grid")))

subprocess.call(["cmd", "/k", "start", "", "file.txt"], stderr=subprocess.STDOUT)


df = pd.read_json (url)
df = DataFrame(df,columns=['denominazione_regione','totale_positivi'])
df.sort_values(by=['totale_positivi'], inplace=True)

# Start charts params

rd = df.plot(x ='denominazione_regione',
             y='totale_positivi',
             kind = 'barh',
             legend = False,
             figsize=(12,8),
             title="SITUAZIONE COVID PER REGIONE",
             cmap='RdBu_r')
rd.set_xlabel("TOT POSITIVI")
rd.set_ylabel("REGIONI")
rd.xaxis.labelpad = 15
rd.yaxis.labelpad = 10

rects = rd.patches

for rect in rects:
	
    # Vertical alignment positive values
	
    ha = 'left'
	
    # Get X and Y rects.
	
    x_value = rect.get_width()
    y_value = rect.get_y() + rect.get_height() / 2

    # Define label val format.

    label = "{0:,}".format(x_value)

    # Create annotation
    plt.annotate(
            label,                      
            (x_value, y_value),         # Place label at end of the bar
            xytext=(1, 0),              # Space between label and rect
            textcoords="offset points", # The coordinate system that xytext is given in.
            va='center',                # Vertically center label
            ha=ha,                      # Horizontally align label differently for positive and negative values.
            fontsize=6,                 # Font size
            rotation=45)                # Rotate label

plt.legend(["N° Abitanti"], loc ="lower right")
plt.savefig("COVID-19 Italia",dpi=250,bbox_inches='tight',pad_inches=0.5) # Save to png 
plt.show()



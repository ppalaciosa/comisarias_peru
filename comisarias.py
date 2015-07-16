#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib2
from bs4 import BeautifulSoup
import json

url = "https://www.mininter.gob.pe/serviciosMAPA-DIRECTORIO-DE-COMISARIAS"

request = urllib2.Request(url)
request.add_header('Accept-Encoding', 'utf-8')

# 'r' has UTF-8 charset header,
# and HTML body which is UTF-8 encoded
r = urllib2.urlopen(request)

soup = BeautifulSoup(r.read().decode('utf-8'))
container = soup.find(id="accordion")

# Lista vacia sobre la cual trabajaremos
x={}
        
# Limpiando la data con lo que nos interesa. 
# Esto se repite en cada categoria
regiones = container.find_all(["h3", "div"], recursive=False)
for item_reg in regiones:
    k = regiones.index(item_reg)
    
    # Nombre de region
    if k % 2 == 0:
        region = regiones[k].text
        x[region] = {}

    # Contenido de region
    provincias = item_reg.find_all(["h3", "div"], recursive=False)
    for item_prov in provincias:
        l = provincias.index(item_prov)

        #Nombre de Provincia
        if l % 2 == 0:
            provincia = provincias[l].text
            x[region][provincia] = {}

        #Contenido de provincia
        distritos = item_prov.find_all(["h3", "div"], recursive=False)
        for item_dist in distritos:
            m = distritos.index(item_dist)
            
            #Nombre de distrito
            if m % 2 == 0:
                distrito = distritos[m].text
                x[region][provincia][distrito] = []

            #Contenido de distrito - COMISARIAS
            comisarias = item_dist.find_all("div", {"class": "content"})
            for item_comi in comisarias:
                n = comisarias.index(item_comi)
                comisaria = item_comi.contents[1].text
                direccion = item_comi.contents[3].text
                telefono = item_comi.contents[5].text
                

                x[region][provincia][distrito].append({"Comisaría": comisaria, 
                                                       "Dirección": direccion, 
                                                       "Teléfono": telefono})


# Abriendo archivo para escritura
out_file = open("comisarias.json","w")
# Grabando con indentado 4
json.dump(x,out_file, indent=4)      
# Cerrando el archivo
out_file.close()

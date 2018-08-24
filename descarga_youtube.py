#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  descarga_youtube
#  
#  Copyright 2018 gnusyscamus <gnusyscamus@gnusyscamus-SVE14113ELW>

from pytube import YouTube
import base64
import time 
import urllib, urllib2
from lxml import etree
from StringIO import StringIO
from bs4 import BeautifulSoup as BS
import base64
import json

def buscarTitulo(titulo):
    titulo=titulo.split(" ")
    t='+'.join(titulo)
    l_encontrados=[]
    query="https://www.youtube.com/results?search_query="+t
    print query
    req=urllib2.Request(query,headers={'User-agent':'Mozila/5.0'})
    f = urllib2.urlopen(req)
    html = f.read()
    soup= BS(html) 
    soup.prettify('latin-1')[1:1000]
    links=soup.findAll("a",{"class":"yt-uix-tile-link"})
    for l in links:
        if "list"  not in l['href'] and "watch"  in l['href']:
            l_encontrados.append("https://www.youtube.com"+l['href'])
          
    return l_encontrados[:5]
    
    

def main(args):
    lista=open("play_list.txt","rw+")
    lista_descarga=[] #Lista final con los enlaces de descarga 

    lista_sugerencias=[]
    for url in lista:
    #agregar header 
        print "url"+url
        if "watch" not in url: # no es un video si no una busqueda
            print "buscando.."
            lista_busqueda=buscarTitulo(url)
            lista_descarga.extend(lista_busqueda)
        else:
            lista_descarga.append(url)#agregar los enlances que estan en el archivo de texto
            req=urllib2.Request(url,headers={'User-agent':'Mozila/5.0'})
            f = urllib2.urlopen(req)
            #time.sleep(10);
            html = f.read()
            soup= BS(html) 
            soup.prettify('latin-1')[1:1000]
            relacionados=soup.find(id="content")
            #relacionados=rela.findAll("li",{"class":"video-list-item"})
            links=relacionados.findAll("a",{"class":"yt-uix-sessionlink"})
            for link in links[:3]:
                if "/watch?v" in str(link['href']):
                    lista_descarga.append("https://www.youtube.com"+str(link['href']))

    playlist = {}
    
    print "Inicia Descarga"
    print lista_descarga
    for k, v in playlist.items():
        try:
            #object creation using YouTube which was imported in the beginning
            #print base64.b64decode(v)
            yt = YouTube("https://www.youtube.com/watch?v=wbS0u77qPP4")
            #yt = YouTube(base64.b64decode(v))
            #video = yt.get('mp4', '720p')
       
        except:
            print("Connection Error") #to handle exception
        
        #filters out all the files with "mp4" extension
        vids= yt.streams.filter(subtype='mp4',progressive=True).all()
        vids[0].download(None,k)
        print "se descargo "+k

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

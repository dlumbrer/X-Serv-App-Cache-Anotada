#!/usr/bin/python

import webapp
import urllib

cache = {}
cab1 = {}

class escrituraApp(webapp.webApp):

    def parse(self, request):
        rec = request.split()[1][1:]
	cabeceras = request.split("\r\n")[1:] #La primera (0) es la peticion
	print "--------------------------------------------------" + str(cabeceras)
	cab1[rec] = cabeceras;  
        return rec


    def process(self, rec):
        urloriginal = "http://" + rec
	
	partes = rec.split("/")
	
	if partes[0] != "cache" and partes[0] != "cab1":
	    try:
		f = urllib.urlopen(urloriginal)
		html = f.read()
		
		#Guardar en cache
		cache[rec] = html
		
		pos1 = html.find("<body")
		#posicionAbsoluta = html.find(">", pos1) OTRA FORMA
		pos2 = html[pos1:].find(">")
		posicionAbsoluta = pos1+pos2+1
		
		html1 = html[:posicionAbsoluta]
		html2 = html[posicionAbsoluta:]
		
		html = html1 + "<p>HOLA " + "<a href='" + urloriginal + "'>Original</a>" + "\r" + "<a href='http://localhost:1234/" + rec + "'>Recarga</a>" + "\r" + "<a href='http://localhost:1234/cache/" + rec + "'>Cache</a>" + "\r" + "<a href='http://localhost:1234/cab1/" + rec + "'>Cab1</a>" + "</p>" + html2
		return ("200 OK", html)
	    except IOError:
		return ("404 Not Found", "Error: Imposible conectar")
		
	elif partes[0] == "cache":
	    try:
		html = cache[partes[1]]
		return ("200 OK", html)
	    except KeyError:
		return ("404 Not Found", "Error: No hay cache almacenada para este sitio")
	elif partes[0] == "cab1":
	    try:
		html = str(cab1[partes[1]])
		return ("200 OK", html)
	    except KeyError:
		return ("404 Not Found", "Error: No hay cabeceras almacenadas para este sitio")
            

if __name__ == "__main__":
    servaleat = escrituraApp("localhost", 1234)

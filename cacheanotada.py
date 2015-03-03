#!/usr/bin/python

import webapp
import urllib

cache = {}

class escrituraApp(webapp.webApp):

    def parse(self, request):
        rec = request.split()[1][1:]  
        return rec


    def process(self, rec):
        urloriginal = "http://" + rec
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
            
            html = html1 + "<p>HOLA " + "<a href='" + urloriginal + "'>Original</a>" + "\r" + "<a href='http://localhost:1234/" + rec + "'>Recarga</a>" + "\r" + "<a href='http://localhost:1234/cache/" + rec + "'>Cache</a>" + "</p>" + html2
            return ("200 OK", html)
        except IOError:
            return ("404 Not Found", "Error: Imposible conectar")
            

if __name__ == "__main__":
    servaleat = escrituraApp("localhost", 1234)

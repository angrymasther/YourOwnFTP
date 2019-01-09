import socket
import sys
import os
import time

help = """
    =====FUNCIONES DEL CLIENTE=======
    -local-ls: Muestra los archivos de este ordenador
    -local-cd: Cambia de directorio en este ordenador
    -exit : Cierra la conexion con el servidor
    -help: Muestra este mensaje
    =====FUNCIONES DEL SERVIDOR======
    -ls : Muestra los archivos almacenados en esta carpeta
    -cd <carpeta>: Cambia de directorio
    -read <archivo>: Lee el archivo especificado
    -load <archivo>: Carga un archivo al servidor
    -mkdir <nombre>: Crea una carpeta
    -download <archivo>: Descarga un archivo
"""
socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
try:
    socket.connect(("localhost" , 8081))
except:
    print "El servidor no esta disponible"
    exit()
print "conectado al servidor"
print help
while 1:
    mensaje = raw_input(">")
    if mensaje[0:4] == "read":
        socket.send(mensaje)
        archivo = socket.recv(2048)
        print archivo
    if mensaje[0:2] == "ls":
        socket.send(mensaje)
        lista = socket.recv(2048)
        print lista
    if mensaje[0:2] == "cd":
        socket.send(mensaje)
        respuesta = socket.recv(1024)
        if respuesta == "ERROR":
            print "No se puede acceder al directorio"
        else:
            print respuesta

    if mensaje[0:4] == "load":
        nombre_archivo = mensaje[5:len(mensaje)]
        if nombre_archivo not in os.listdir("."):
            print "archivo no encontrado en el directorio de ejecucion"
        else:
            socket.send(mensaje)
            archivo = open(nombre_archivo, "r")
            texto = archivo.read()
            socket.send(texto)
    if mensaje[0:4] == "exit":
        socket.send("exit")
        time.sleep(1)
        exit()
    if mensaje[0:5] == "mkdir":
        socket.send(mensaje)
        mensaje_servidor = socket.recv(1024)
        print mensaje_servidor
    if mensaje[0:5] == "clear":
        print "\n"*100
    if mensaje[0:8] == "local-ls":
        lista = ""
        for x in os.listdir("."):
            lista += x + "\n"
        print lista
    if mensaje[0:8] == "local-cd":
        os.chdir(mensaje[9:len(mensaje)])
    if mensaje[0:8] == "download":
        socket.send(mensaje)
        contenido = socket.recv(10000)
        if contenido != "No hay archivo":
            archivo = open(mensaje[10:len(mensaje)],"w")
            archivo.write(contenido)
            archivo.close()

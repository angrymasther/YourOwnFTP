import socket
import os
import sys
import time
import threading

direccion_maxima = sys.argv[1]

def funcion_servidor(socket):
    direccion_actual = sys.argv[1]

    while 1:
        instruccion = socket.recv(1024) #read <a>,load <a>, ls
        if instruccion[0:4] == "read":
            nombre_archivo = direccion_actual + instruccion[5:len(instruccion)]
            time.sleep(1)
            socket.send(read(nombre_archivo))
            print "archivo envieado"
        if instruccion[0:2] == "ls":
            time.sleep(1)
            socket.send(ls(direccion_actual))
        if instruccion[0:2] == "cd":
            time.sleep(1)
            try:
                os.chdir(direccion_actual + instruccion[3:len(instruccion)])
                direccion_actual += instruccion[3:len(instruccion)] + "\\"
                socket.send(os.getcwd())
            except:
                socket.send("ERROR")

        if instruccion[0:4] == "load":
            nombre = direccion_actual + instruccion[5:len(instruccion)]
            contenido = socket.recv(2048)
            print load(nombre,contenido)
        if instruccion[0:4] == "exit":
            socket.close()
            return 0
        if instruccion[0:5] == "mkdir":
            time.sleep(1)
            nombre_carpeta = instruccion[6:len(instruccion)]
            try:
                os.mkdir(direccion_actual + nombre_carpeta)
                socket.send("carpeta creada")
            except:
                socket.send("error al crear la carpeta")
                direccion_actual = direccion_actual + "\\"

        if instruccion[0:8] == "download":
            time.sleep(1)
            socket.send(read(instruccion[10:len(instruccion)]))

def read(nombre):
    try:
        archivo = open(nombre , "r")
        return archivo.read()
    except IOError:
        return "archivo no encontrado"
def ls(direccion_actual):
    lista = ""
    print os.listdir(direccion_actual)
    for x in os.listdir(direccion_actual):
        lista += x + "\n"
    if lista == "":
        lista = "Vacio"
    return lista

def load(nombre, contenido):
    archivo = open(nombre , "w")
    archivo.write(contenido)
    return "archivo escrito"

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("localhost",8081)) #Sustituir "localhost" por socket.gethostname()
socket.listen(60)
print "Servidor funcionando"
while True:
    socket_cliente, direccion_cliente = socket.accept()
    print direccion_cliente
    t = threading.Thread(target=funcion_servidor , args=(socket_cliente,))
    t.start()

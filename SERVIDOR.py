import socket
import os
import sys
import time
import threading

direccion_maxima = sys.argv[1]

def getNow():
    now = str(time.localtime(time.time())[2]) + "/" + str(time.localtime(time.time())[1]) + "/" +str(time.localtime(time.time())[0])+" "+ str(time.localtime(time.time())[3]) + ":" + str(time.localtime(time.time())[4]) + ":" +str(time.localtime(time.time())[5])
    return now
def funcion_servidor(socket, cliente):
    direccion_actual = sys.argv[1]
    IP = cliente[0]
    while 1:
        instruccion = socket.recv(1024) #read <a>,load <a>, ls
        if instruccion[0:4] == "read":
            if direccion_actual in instruccion[5:len(instruccion)]:
                nombre_archivo = instruccion[5:len(instruccion)]
                if read(nombre_archivo[1]) == "":
                    time.sleep(1)
                    socket.send(5)
                    time.sleep(3)
                    socket.send("vacio")
                    print getNow() + "enviado contenido (vacio) de " + nombre_archivo + " a " + IP
                else:
                    nombre_archivo = instruccion[5:len(instruccion)]
                    socket.send(read(nombre_archivo)[0])
                    time.sleep(3)
                    socket.send(read(nombre_archivo)[1])
                    print getNow() + "!enviado contenido de " + nombre_archivo + " a " + IP
            else:
                nombre_archivo = direccion_actual + instruccion[5:len(instruccion)]
                if read(archivo)[1] == "":
                    socket.send(5)
                    time.sleep(1)
                    socket.send("vacio")
                    print getNow() + "enviado contenido (vacio) de " + nombre_archivo + " a " + IP
                else:
                    time.sleep(1)
                    socket.send(read(nombre_archivo)[0])
                    time.sleep(1)
                    socket.send(read(nombre_archivo)[1])
                    print getNow() + "enviado contenido de " + nombre_archivo + " a " + IP

        if instruccion[0:2] == "ls":
            time.sleep(1)
            socket.send(ls(direccion_actual))
            print getNow() + "enviado listado de archivo de " + direccion_actual + " a " + IP
        if instruccion[0:2] == "cd":
            time.sleep(1)
            try:
                os.chdir(direccion_actual + instruccion[3:len(instruccion)])
                direccion_actual += instruccion[3:len(instruccion)] + "/" #Cambiar "/" por "\\" en WINDOWS
                socket.send(os.getcwd())
                print getNow() + IP + "accedio a" + os.getcwd()
            except:
                socket.send("ERROR")
                print getNow() + IP + "No pudo acceder a" + os.getcwd()

        if instruccion[0:4] == "load":
            nombre = direccion_actual + instruccion[5:len(instruccion)]
            contenido = socket.recv(2048)
            load(nombre,contenido)
            print getNow() + IP + "subio "+nombre
        if instruccion[0:4] == "exit":
            socket.close()
            print getNow() +" "+ IP + " salio"
            return 0
        if instruccion[0:4] == "walk":
            time.sleep(1)
            socket.send(walk())
            print getNow()+" "+IP+" pidio un walk"

        if instruccion[0:5] == "mkdir":
            time.sleep(1)
            nombre_carpeta = instruccion[6:len(instruccion)]
            try:
                os.mkdir(direccion_actual + nombre_carpeta)
                socket.send("carpeta creada")
                print getNow() +" "+ IP + "creo la carpeta "+direccion_actual + nombre_carpeta
            except:
                socket.send("error al crear la carpeta")
                print getNow() + " " + IP + "no puedo crear la carpeta"+direccion_actual + nombre_carpeta
                direccion_actual = direccion_actual + "/"#Cambiar "/" por "\\" en windows

        if instruccion[0:8] == "download":
            time.sleep(1)
            if os.path.isfile(instruccion[10:len(instruccion)]):
                socket.send(read(nombre_archivo)[0])
                time.sleep(1)
                socket.send(read(instruccion[10:len(instruccion)])[1])
                print getNow() + " " + "IP descargo " + instruccion[10:len(instruccion)]
            else:
                socket.send(20)
                time.sleep(1)
                socket.send("No hay archivo")
def walk():
    lista = ""
    for path, dirs, archivos in os.walk(direccion_maxima):
        for archivo in archivos:
            lista += "," + path + "/" + archivo
    lista = lista[1:len(lista)]
    for x in lista:
        x = x[len(direccion_maxima):len(x)]
        print "     "+x
    if lista == "":
        return "vc"
    return lista
def read(nombre):
    try:
        archivo = open(nombre , "r")
        return len(archivo.read())
    except IOError:
        return (len("archivo no encontrado"),"archivo no encontrado")
def ls(direccion_actual):
    lista = ""
    print os.listdir(direccion_actual)
    for x in os.listdir(direccion_actual):
        if os.path.isdir(x):
            lista += "\"d(" + x + ")\","
        else:
            lista += "\"" + x + "\","
    if lista == "":
        lista = "Vacio"
    else:
        lista += ""
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
    t = threading.Thread(target=funcion_servidor , args=(socket_cliente,direccion_cliente))
    t.start()

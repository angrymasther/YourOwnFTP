import os
import sys
import socket
import time

servidor = sys.argv[1]
direccion_cliente = sys.argv[2]
socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
bucle = 1
def getNow():
    now = str(time.localtime(time.time())[2]) + "/" + str(time.localtime(time.time())[1]) + "/" +str(time.localtime(time.time())[0])+" "+ str(time.localtime(time.time())[3]) + ":" + str(time.localtime(time.time())[4]) + ":" +str(time.localtime(time.time())[5])
    return now
while bucle == 1:
    try:
        socket.connect((servidor,8081))
        print getNow()+" conectado al servidor"
        bucle = 0
    except:
        print getNow()+" imposible conectarse al servidor"
        time.sleep(60)

socket.send("walk")
print getNow()+" send walk"
mensaje = socket.recv(1024)
if mensaje == "vc":
    print getNow()+" Nube vacia"
    exit()

print getNow()+" recv " + mensaje
lista = mensaje.split(",")
for x in lista:
    if x != "":
        x = x[2:len(x)]
        socket.send("read " + x)
        print getNow()+" read " + x
        contenido = socket.recv(1024)
        print getNow()+"recv " + contenido
        o = open(direccion_cliente+x,"w")
        print direccion_cliente + "/"+x+"!!!"
        archivo = open(direccion_cliente + "/" +x , "w")
        print getNow()+" creado archivo  " + direccion_cliente+ "/"+x
        archivo.write(contenido)
        archivo.close()

socket.send("exit")
print "(equipo -> servidor) exit"
exit()

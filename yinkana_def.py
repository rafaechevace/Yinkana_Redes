#!/usr/bin/python3
"""YINKANA"""
#Rafael Echevarria Acena
#Se ha codificado en nano de linux ya que he tenido problemas al copiar los simbolos
#del hito 2 fuera de nano, no los reconocia.
#Se han hecho algunas abreviaturas en ciertos metodos que generaban 'linea demasiado larga'
#Pylint 10/10

#Definicion de librerias usadas
import sys
import array
import logging
import socket
import threading
import _thread
import hashlib
import struct
import base64
import queue
import urllib.request

#___FUNCIONES UTILIZADAS EN LOS DISTINTOS RETOS___

    #Funciones generales:
def encontrar_identificador(statement: bytes)-> bytes:
    """Funcion para encontrar el identificador en un enunciado"""
    for linea in statement.split(b"\n"): #Dividir el enunciado en lineas
        if b"identifier:" in linea: #Buscar la linea que contiene el identificador
            return linea.split(b":")[-1] #Extraer el identificador
    return None

def obtener_instrucciones(socket_read)-> str:
    """Funcion para obtener las instrucciones de un socket"""
    datos =b""  #Variable para almacenar los datos recibidos
    while True: #Bucle para recibir los datos
        datos_recibidos= socket_read.recv(2048) #Recibir datos para conexiones tcp
        if not datos_recibidos: #Si no hay datos recibidos, salir del bucle
            break
        datos += datos_recibidos #Almacenar los datos recibidos
    return datos

def encontrar_puerto_libre(socket_read:socket)-> int:
    '''Encuentra puertos libres en un rango'''
    for port in range(5000, 6000):  # Rango de puertos a probar
        try:
            # Intenta enlazar el socket al puerto
            socket_read.bind(("", port))
            return port  # Si se enlaza con   xito, retorna el puerto
        except OSError:
            continue  # Si hay un error, prueba con el siguiente puerto
    raise OSError("No se encontro un puerto libre en el rango especificado")

    #Hito 2
def obtener_instrucciones_corazon(socket_read)-> bytes:
    """Funcion para obtener las instrucciones del socket del hito 2"""   
    datos =b""  #Variable para almacenar los datos recibidos
    datos_recibidos=b""
    #Simbolo que queremos encontrar para parar de recibir datos
    simbolo_parar="╭(◉)╮".encode("utf-8")
    while True:
        datos_recibidos= socket_read.recv(2048) #Recibir datos en conexiones tcp
        datos+=datos_recibidos #Actualizar los datos recibidos
        if not datos_recibidos:
            break  #Si no hay datos recibidos, salir del bucle
        if simbolo_parar in datos: #Si se encuentra el simbolo de parada, parar de recibir datos
            datos=datos.split(simbolo_parar)[0]  #Extraer los datos hasta el simbolo de parada
            break
    return datos


def obtener_corazones(socket_read)-> str:
    """Funcion para comparar los simbolos del hito 2"""
    lista=[] #Lista para almacenar los corazones
    datos=obtener_instrucciones_corazon(socket_read) #Obtener los datos del socket
    cont=contar_corazones(datos) #Contar los corazones
    print(cont)
    for _ in range(cont): #A  adir corazones a la lista
        lista.append("[❤]")
    return lista

def contar_corazones(datos: bytes)-> int:
    """Funcion para contar los corazones de una lista"""
    corazon="[❤]".encode("utf-8")
    cont=datos.count(corazon) #Contar los corazones en los datos
    return cont

#Hito 3
def obtener_texto_reducido(socket_read) -> str:
    """Funcion para obtener el texto reducido del socket del hito 3"""
    datos = b"" # Variable para almacenar los datos recibidos
    palabras = [] # Lista para almacenar las palabras
    n = None # Variable para almacenar el número de palabras
    parar=False
    indice=0
    while True:
        datos_recibidos = socket_read.recv(4096) # Recibir datos en conexiones tcp
        if not datos_recibidos:
            break
        datos += datos_recibidos

        # Convertir bytes a string
        datos_str = datos.decode()
        print(datos_str)
        # Dividir el string en palabras
        nuevas_palabras = datos_str.split()

        if n is None:
            for palabra in nuevas_palabras: # Buscar el número de palabras
                if palabra.isdigit(): # Si la palabra es un número, almacenar el número
                    n = int(palabra) # Convertir el número a entero
                    break

        if n is not None:
            for palabra in nuevas_palabras[indice:]:  # Recorrer las palabras
                if not palabra.isdigit(): # Si la palabra no es un número, añadirla a la lista
                    if len(palabras) <n: # Si n es mas grande añadir la palabra
                        palabras.append(palabra)
                    else:
                        parar=True
                        break
                indice += 1

        if parar:
            break

    return ' '.join(palabras) # Unir las palabras en un string

def obtener_iniciales_en_mayusculas(texto):
    """Función para obtener las iniciales de las palabras en mayúsculas"""
    palabras=texto.split() # Dividir el texto en palabras
    # Extraer las iniciales de las palabras y convertirlas a mayusculas
    iniciales = ' '.join([palabra[0].upper() for palabra in palabras])
    return iniciales

    #Hito 4
def obtener_archivo(socket_read):
    """Funcion para obtener el archivo del socket del hito 4"""
    tamano = ''
    while True:
        caracter = socket_read.recv(1).decode('ascii') # Leer un caracter del socket
        if caracter == ':': # Si el caracter es ':', salir del bucle
            break
        tamano += caracter # Almacenar el tamaño del archivo

    # Convertir el tama  o a entero
    tamano = int(tamano)

    # Leer los datos del socket hasta el tama  o especificado
    datos = b""
    while len(datos) < tamano: # Leer los datos del socket hasta que se alcance tamano
        datos_recibidos = socket_read.recv(2048) # Recibir datos en conexiones tcp
        if not datos_recibidos:
            break
        datos += datos_recibidos # Almacenar los datos recibidos

    return datos

    #Hito 5
    #Metodo para calcular el checksum de arco:esi uclm
def cksum(pkt):
    """Funcion para crear el checksum de un paquete proporcionado por ARCO:ESI UCLM"""
    if len(pkt) % 2 == 1:
        pkt += b'\0'
    s = sum(array.array('H', pkt))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    s = ~s

    if sys.byteorder == 'little':
        s = ((s >> 8) & 0xff) | s << 8

    return s & 0xffff

    #Hito 6
def obtener_identificador(mensaje_bytes):
    """Funcion para obtener el identificador de un mensaje del servidor del hito 6"""
    mensaje = mensaje_bytes.decode() # Convertir el mensaje a string
    inicio = mensaje.find("identifier:") + len("identifier:")   # Encontrar el inicio
    fin = mensaje.find("%0A", inicio)   # Encontrar el final
    identificador = mensaje[inicio:fin]  # Extraer el identificador
    return identificador

def get(s: socket.socket, m:bytes, sv: tuple[str,int], q: queue.Queue)->None:
    """Funcion para procesar las peticiones GET"""
    #Se han abreviado las variables para evitar linea demasiado larga
    f = m.split(b" ")[1]
    f_str=f.decode()
    print(f_str)
    if b"identifier:" in f:
        id_bytes=obtener_identificador(f)
        q.put(id_bytes.encode())
    else:
        with urllib.request.urlopen(f"http://{sv[0]}:{sv[1]}/rfc{f_str}") as r:
            if r.status == 200:
                s.sendall(b"HTTP/1.1 200 OK\r\n\r\n" + r.read())
            else:
                s.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    s.close()

def recibir_mensaje(socket_cliente:socket.socket, servidor : tuple[str,int])->bytes:
    """Funcion para recibir mensajes del servidor del hito 6"""
    q = queue.Queue() #He obtenido varios problemas por el uso de concurrencia hasta que utilize
    #esta libreria, similar a la que utilizamos en pctr pero para python.
    while True:
        socket_aceptado,_=socket_cliente.accept()
        mensaje=socket_aceptado.recv(2048)
        print(mensaje)
        if mensaje[:3] == b"GET":  # Si el mensaje es una peticion GET,
            #crear un hilo para procesar la peticion
            thread= threading.Thread(target=get, args=(socket_aceptado,mensaje,servidor, q))
            thread.start()
            thread.join()   # Esperar a que el hilo termine
            if not q.empty():
                identificador = q.get() # Extraer el identificador de la cola
                return identificador
        else:
            return mensaje

def procesar_mensajes(server: tuple[str,int], identifier:bytes, puerto:bytes )->None:
    """Funcion para procesar los mensajes del servidor del hito 6"""
    mensaje:bytes=identifier+ b" " +puerto
    socket_cliente=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cliente.connect(server)
    print(mensaje)
    socket_cliente.sendall(mensaje)
    while True:
        mensaje_cliente= socket_cliente.recv(2048)
        if not mensaje_cliente:
            break

#___FUNCIONES DE LOS HITOS___
    #Hito 0
def hito0(usuario:str, server_address: str)-> str:
    """Funcion para ejecutar el hito 0"""
    logging.info("Iniciando Reto 0....") #Mensaje de inicio
    socket_hito0=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Creacion del socket
    socket_hito0.connect((server_address, 2000)) #Conexion al servidor
    socket_hito0.recv(1024) #Recibir mensaje de bienvenida
    socket_hito0.sendall(usuario.encode()) #Enviar usuario al servidor
    enunciado= obtener_instrucciones(socket_hito0) #Obtener enunciado
    logging.info(enunciado.decode()) #Mostrar enunciado
    socket_hito0.close() #Cerrar conexion
    return encontrar_identificador(enunciado) #Devolver el identificador

    #Hito 1
def hito1(identifier: bytes) -> bytes:
    """Funcion para ejecutar el hito 1"""
    socket_hito1=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creacion del socket
    puerto=encontrar_puerto_libre(socket_hito1) #Encontrar puerto libre
    direccion_servidor = ('rick', 4000) #Direccion del servidor
    mensaje : bytes = f"{puerto} ".encode() + identifier #Mensaje a enviar

    socket_hito1.sendto(mensaje, direccion_servidor) #Enviar mensaje al servidor
    msg, sender = socket_hito1.recvfrom(2048) #Recibir mensaje del servidor
    logging.info("Hito1: \n%s", msg.decode()) #Mostrar mensaje recibido

    if msg == b"upper-code?": #Si el mensaje recibido es "upper-code?",
        #enviar el identificador en mayusculas
        logging.info("Hito1: sending %s to %s", identifier.upper(), sender) #Mostrar mensaje
        socket_hito1.sendto(identifier.upper(), sender) #Enviar identificador en mayusculas
        enunciado, sender= socket_hito1.recvfrom(2048) #Recibir enunciado
        logging.info("Hito1: %s", enunciado.decode()) #Mostrar enunciado

        return encontrar_identificador(enunciado) #Devolver el identificador

    logging.error("Error al recibir enunciado") #Comprobacion porque me daba error
    return identifier    #Devolver el identificador

    #Hito 2
def hito2(identifier: bytes, server_address: str) -> bytes:
    """Funcion para ejecutar el hito 2"""
    socket_hito2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creacion del socket
    socket_hito2.connect((server_address, 3006)) #Conexion al servidor

    lista=obtener_corazones(socket_hito2) #Obtener los corazones
    reply = f"{identifier.decode()} {''.join(lista)} --" #Respuesta a enviar
    socket_hito2.sendall(reply.encode())    #Enviar respuesta al servidor

    enunciado = obtener_instrucciones(socket_hito2) #Obtener enunciado
    logging.info(enunciado.decode()) #Mostrar enunciado
    socket_hito2.close() #Cerrar conexion
    return encontrar_identificador(enunciado) #Devolver el identificador

    #Hito 3
def hito3(identifier: bytes, server_address: str)-> bytes:
    """Funcion para ejecutar el hito 3"""
    socket_hito3= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creacion del socket
    socket_hito3.connect((server_address, 3005)) #Conexion al servidor

    socket_hito3.sendall(identifier) #Enviar identificador al servidor
    mensaje=obtener_texto_reducido(socket_hito3)#Obtener texto reducido

    print(mensaje) #Mostrar texto reducido
    msg= obtener_iniciales_en_mayusculas(mensaje) #Obtener iniciales en mayusculas
    print(msg) #Mostrar iniciales en mayusculas

    socket_hito3.sendall(msg.encode()) #Enviar iniciales al servidor
    enunciado= obtener_instrucciones(socket_hito3) #Obtener enunciado
    logging.info(enunciado.decode()) #Mostrar enunciado
    socket_hito3.close() #Cerrar conexion
    return encontrar_identificador(enunciado) #Devolver el identificador


    #Hito 4
def hito4(identifier: bytes, server_address:str)-> bytes:
    """Funcion para ejecutar el hito 4"""
    socket_hito4= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creacion del socket
    socket_hito4.connect((server_address, 9003)) #Conexion al servidor
    socket_hito4.sendall(identifier) #Enviar identificador al servidor
    mensaje=obtener_archivo(socket_hito4) #Obtener archivo

    print(mensaje) #Mostrar archivo
    sha1=hashlib.sha1() #Calcular sha1
    sha1.update(mensaje) #Actualizar sha1
    suma_sha1=sha1.digest() #Obtener suma sha1

    socket_hito4.sendall(suma_sha1) #Enviar suma sha1 al servidor
    mensaje2=obtener_instrucciones(socket_hito4) #Obtener enunciado
    print(mensaje2.decode()) #Mostrar enunciado
    socket_hito4.close() #Cerrar conexion
    return encontrar_identificador(mensaje2) #Devolver el identificador

    #Hito 5
def hito5(identifier: bytes, server_address:str)-> bytes:
    """Funcion para ejecutar el hito 5"""
    socket_hito5=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creacion del socket
    direcion=(server_address,6000) #Direccion del servidor
    payload=base64.b64encode(identifier) #Codificar el identificador en base64

    header=struct.pack('!3sBHHH',b'WYP',0,0,0,1) #Empaquetar la cabecera
    #probé varios numeros de secuenciay me daba error, con el uno no.
    message=header+payload #Empaquetar el mensaje
    checksum=cksum(message) #Calcular el checksum
    header=struct.pack('!3sBHHH',b'WYP',0,0,checksum,1) #Empaquetar la cabecera con el checksum
    message2=header+payload #Empaquetar el mensaje con el checksum

    socket_hito5.sendto(message2,direcion) #Enviar mensaje al servidor
    paquete, _= socket_hito5.recvfrom(2048) #Recibir paquete del servidor

    lp = len(paquete) - 10 #10 es la longitud de la cabecera
    #Uso lp para evitar longitud de liena demasiado larga en la siguiente
    _, _, _, checksum, _, paquete = struct.unpack(f'!3sBHHH{lp}s', paquete)
    #Desempaquetar el paquete
    payload_decoded = base64.b64decode(paquete) #Decodificar el payload
    print(payload_decoded) #Mostrar payload
    return encontrar_identificador(payload_decoded) #Devolver el identificador

    #Hito 6
def hito6(identifier:bytes)-> bytes:
    """Funcion para ejecutar el hito 6"""
    socket_hito6=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creacion del socket
    puerto_libre=encontrar_puerto_libre(socket_hito6) #Encontrar puerto libre
    socket_hito6.listen(5) #Escuchar conexiones
    server=("rick",8003) #Direccion del servidor
    servidor=("web",81) #Direccion del servidor
    puerto = str(puerto_libre).encode('utf-8')  # Convertir el puerto a bytes
    #Procesar mensajes de forma concurrente
    _thread.start_new_thread(procesar_mensajes,(server, identifier, puerto))
    mensaje= recibir_mensaje(socket_hito6, servidor) #Mensaje recibido
    socket_hito6.close() #Cerrar conexion
    return mensaje

def hito7(mensaje:bytes)->bytes:
    """Funcion para ejecutar el hito 7"""
    socket_hito7=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Creacion del socket
    socket_hito7.connect(("rick", 33333)) #Conexion al servidor
    socket_hito7.sendall(mensaje) #Enviar mensaje al servidor
    final=socket_hito7.recv(2046) #Recibir mensaje del servidor
    socket_hito7.close() #Cerrar conexion
    return final

    #FUNCION PRINCIPAL
    #He elegido este formato porque fue el que se nos enseño en el primer laboratorio
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format= '') #Configuracion del log
    USER= 'full_moth' #Usuario
    SERVER_ADDRESS = 'rick' #Direccion del servidor
    try:
        hito0_id=hito0(USER, SERVER_ADDRESS) #Ejecutar el hito 0
        logging.info("[IDENTIFICADOR HITO 0]: %s", hito0_id.decode()) #Mostrar el ident del hito 0
        hito1_id=hito1(hito0_id)  #Ejecutar el hito 1
        logging.info("[IDENTIFICADOR HITO 1]: %s", hito1_id.decode()) #Mostrar el ident del hito 1
        hito2_id=hito2(hito1_id, SERVER_ADDRESS) #Ejecutar el hito 2
        logging.info("[IDENTIFICADOR HITO 2]: %s", hito2_id.decode()) #Mostrar el ident del hito 2
        hito3_id=hito3(hito2_id, SERVER_ADDRESS) #Ejecutar el hito 3
        logging.info("[IDENTIFICADOR HITO 3]: %s", hito3_id)    #Mostrar el ident del hito 3
        hito4_id=hito4(hito3_id, SERVER_ADDRESS) #Ejecutar el hito 4
        logging.info("[IDENTIFICADOR HITO 4]: %s", hito4_id)    #Mostrar el ident del hito 4
        hito5_id=hito5(hito4_id,SERVER_ADDRESS) #Ejecutar el hito 5
        logging.info("[IDENTIFICADOR HITO 5]: %s", hito5_id)   #Mostrar el ident del hito 5
        hito6_id=hito6(hito5_id) #Ejecutar el hito 6
        logging.info("[IDENTIFICADOR HITO 6]: %s", hito6_id)    #Mostrar el ident del hito 6
        hito7_id=hito7(hito6_id)
        logging.info("[IDENTIFICADOR HITO 7]: %s", hito7_id)
    except KeyboardInterrupt: #Capturar excepcion de interrupcion
        logging.warning("Ejecucion interrumpida CTrl+C") #Mostrar mensaje de interrupcion

#End-of-file (EOF)

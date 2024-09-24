# Yinkana_Redes
    Implementación de múltiples hitos, cada uno con sus propios desafíos y lógica de red.
    Uso de sockets TCP y UDP para comunicación entre cliente y servidor.
    Manejo de hilos para procesar mensajes de manera concurrente.
    Gestión de archivos, checksum, y otros tipos de procesamiento de datos.
    Logueo detallado de cada operación.
    Cumple con las normas de calidad de Pylint con una puntuación de 10/10.
    
##Requisitos

    Python 3.x
    Módulos estándar de Python:
        sys, socket, threading, _thread, hashlib, queue, logging, struct, array, base64, urllib

##Funciones Principales

1. Hito 0: hito0(usuario: str, server_address: str) -> str

    Conecta al servidor en el puerto 2000, envía el nombre del usuario y recibe un enunciado con un identificador que debe procesarse.

3. Hito 1: hito1(identifier: bytes) -> bytes

    Usa el protocolo UDP para enviar un mensaje al servidor y recibir una respuesta. Si el servidor solicita el identificador en mayúsculas, el cliente responde con el identificador transformado.

5. Hito 2: hito2(identifier: bytes, server_address: str) -> bytes
 
      Conecta con el servidor, recibe un mensaje codificado con corazones ([❤]), y procesa los símbolos para enviar una respuesta correcta.

7. Hito 3: hito3(identifier: bytes, server_address: str) -> bytes

    Envía un identificador y recibe un mensaje que se reduce a sus iniciales en mayúsculas. Luego envía este resultado de vuelta al servidor.

9. Hito 4: hito4(identifier: bytes, server_address: str) -> bytes
 
   Recibe un archivo binario del servidor, calcula su SHA-1 y lo envía de vuelta.

11. Hito 5: hito5(identifier: bytes, server_address: str) -> bytes
  
  Utiliza un protocolo empaquetado y codifica el identificador en base64 para interactuar con el servidor a través de UDP. El mensaje se empaqueta con un checksum personalizado.

13. Hito 6: hito6(identifier: bytes) -> bytes
  
  Establece un puerto libre, recibe y procesa mensajes HTTP GET en paralelo con un servidor, utilizando hilos para procesar cada petición.

15. Hito 7: hito7(mensaje: bytes) -> bytes
  
  Establece una conexión con el servidor en el puerto 33333, envía el mensaje final, y recibe la respuesta final.

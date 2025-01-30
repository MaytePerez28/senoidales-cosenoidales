import time
import math
from Adafruit_IO import MQTTClient
 
ADAFRUIT_IO_USERNAME = "MaytePerez28"
ADAFRUIT_IO_KEY = "aio_Wftt26W7MTWAPTSOD4gMCeWPgWHG"
 
FEED_SENO = "senoidal"
FEED_COSENO = "cosenoidal"
 
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
 
def connected(client):
    print("Conectado a Adafruit IO")
 
def disconnected(client):
    print("Desconectado de Adafruit IO. Intentando reconectar...")
    reconnect(client)
 
def message(client, feed_id, payload):
    print(f"Mensaje recibido en {feed_id}: {payload}")
 
def reconnect(client):
    """ Intenta reconectar en caso de desconexión """
    while True:
        try:
            client.connect()
            client.loop_background()
            print("Reconexion exitosa")
            break
        except Exception as e:
            print(f"Error en reconexión: {e}")
            time.sleep(5)
 
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
 
client.connect()
client.loop_background()
 
i = 0
while True:
    x = (i % 100) / 100 * 2 * math.pi
    sen_val = round(math.sin(x), 4)
    cos_val = round(math.cos(x), 4)
 
    try:
        client.publish(FEED_SENO, sen_val)
        client.publish(FEED_COSENO, cos_val)
        print(f"Enviado -> Seno: {sen_val}, Coseno: {cos_val}")
    except Exception as e:
        print(f"Error al enviar datos: {e}")
        reconnect(client)
 
    i += 1
    time.sleep(6)

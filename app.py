import paho.mqtt.client as mqtt
import time
import random

BROKER = "mosquitto"
PORT = 1883
TOPIC = "sensors/temperature"

client = mqtt.Client()

def connect_with_retry():
    while True:
        try:
            print(f"Verbinden met de broker ({BROKER})...")
            client.connect(BROKER, PORT, 60)
            print("Verbonden!")
            break
        except Exception as e:
            print(f"Kon nog niet verbinden: {e}. Opnieuw proberen in 5 seconden...")
            time.sleep(5)

connect_with_retry()

while True:
    try:
        # GEBRUIK UNIFORM VOOR FLOATS (randdouble bestaat niet)
        waarde = random.uniform(29478.3108065056, 59478.3108065056)
        
        client.publish(TOPIC, waarde)
        print(f"Verzonden: {waarde:.2f} naar {TOPIC}")
        time.sleep(5)
    except Exception as e:
        print(f"Fout tijdens verzenden: {e}")
        time.sleep(2)

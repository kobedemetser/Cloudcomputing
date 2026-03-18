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
            print("Verbinden met de broker...")
            client.connect(BROKER, PORT, 60)
            print("Verbonden!")
            break
        except Exception as e:
            print(f"Kon nog niet verbinden: {e}. Opnieuw proberen in 5 seconden...")
            time.sleep(5)

connect_with_retry()

while True:
    # Simuleer een waarde
    waarde = random.randint(20, 30)
    client.publish(TOPIC, waarde)
    print(f"Verzonden: {waarde} naar {TOPIC}")
    time.sleep(5)

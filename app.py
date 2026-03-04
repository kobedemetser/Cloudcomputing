import paho.mqtt.client as mqtt
import time
import random


BROKER = "mosquitto"
PORT = 1883
TOPIC = "sensors/temp"

client = mqtt.Client()

print("Verbinden met de broker...")
client.connect(BROKER, PORT, 60)

while True:
    # Simuleer een waarde
    waarde = random.randint(-10, 50)
    client.publish(TOPIC, waarde)
    print(f"Verzonden: {waarde} naar {TOPIC}")
    time.sleep(5)

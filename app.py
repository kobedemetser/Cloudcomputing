import paho.mqtt.client as mqtt
import time
import random
import json

BROKER = "mosquitto"
PORT = 1883
TOPIC_JOYSTICK = "sensor/joystick"
TOPIC_BUTTONS = "sensor/buttons"

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
        # Publish payloads in the same format as the Node-RED validators.
        joystick_payload = {
            "x": random.randint(-100, 100),
            "y": random.randint(-100, 100),
        }
        buttons_payload = {
            "btn1": random.randint(0, 1),
            "btn2": random.randint(0, 1),
        }

        client.publish(TOPIC_JOYSTICK, json.dumps(joystick_payload))
        client.publish(TOPIC_BUTTONS, json.dumps(buttons_payload))
        print(f"Verzonden joystick naar {TOPIC_JOYSTICK}: {joystick_payload}")
        print(f"Verzonden buttons naar {TOPIC_BUTTONS}: {buttons_payload}")
        time.sleep(5)
    except Exception as e:
        print(f"Fout tijdens verzenden: {e}")
        time.sleep(2)

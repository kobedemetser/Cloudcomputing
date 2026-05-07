import paho.mqtt.client as mqtt
import time
import random
import json

BROKER = "mosquitto"
PORT = 1883
TOPIC_CRYPTO = "sensor/crypto"

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

# Startprijzen
btc_price = 55000.0
eth_price = 3200.0

while True:
    try:
        # Simuleer kleine prijsfluctuaties (volatility)
        btc_price += round(random.uniform(-15.0, 15.0), 2)
        eth_price += round(random.uniform(-5.0, 5.0), 2)

        crypto_payload = {
            "symbol_btc": "BTCEUR",
            "price_btc": round(btc_price, 2),
            "symbol_eth": "ETHEUR",
            "price_eth": round(eth_price, 2)
        }

        client.publish(TOPIC_CRYPTO, json.dumps(crypto_payload))
        print(f"Verzonden naar {TOPIC_CRYPTO}: {crypto_payload}")
        
        time.sleep(5)
    except Exception as e:
        print(f"Fout tijdens verzenden: {e}")
        time.sleep(2)
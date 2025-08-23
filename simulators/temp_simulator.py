# This simulates a temperature sensor
import json
import time
import random
import paho.mqtt.client as mqtt
from datetime import datetime

class TempSensor:
    def __init__(self):
        self.client = mqtt.Client(client_id="temp_sensor_001")
        self.client.on_connect = self.on_connect

        self.device_id = "kitchen_temp_sensor"
        self.name = "Kitchen Temperature"

    def on_connect(self, client, userdata, flags, rc):
        print(f"🌡️ {self.name} connected to MQTT broker")

        # Announce this sensor exists
        discovery = {
            "name": self.name,
            "state_topic": f"home/sensor/{self.device_id}/temperature",
            "unit_of_measurement": "°C",
            "device_class": "temperature",
            "device": {
                "identifiers": [self.device_id],
                "name": self.name,
                "manufacturer": "Demo Corp",
                "model": "TempSense Pro"
            }
        }

        client.publish(
            f"homeassistant/sensor/{self.device_id}/config",
            json.dumps(discovery),
            retain=True
        )

    def send_temperature(self):
        # Send a random temperature reading
        temp = round(random.uniform(18.0, 26.0), 1)  # Random temp between 18-26°C

        data = {
            "temperature": temp,
            "timestamp": datetime.now().isoformat(),
            "battery": random.randint(75, 100)
        }

        self.client.publish(
            f"home/sensor/{self.device_id}/temperature",
            json.dumps(data)
        )
        print(f"🌡️ Temperature: {temp}°C")

    def run(self):
        time.sleep(3)
        self.client.connect("mosquitto", 1883, 60)
        self.client.loop_start()

        # Send temperature every 30 seconds
        while True:
            self.send_temperature()
            time.sleep(30)

if __name__ == "__main__":
    sensor = TempSensor()
    sensor.run()

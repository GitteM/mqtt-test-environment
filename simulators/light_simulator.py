# This simulates a smart light bulb
import json
import time
import paho.mqtt.client as mqtt
from datetime import datetime

class SmartLight:
    def __init__(self):
        self.client = mqtt.Client(client_id="light_sensor_001")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Light settings
        self.device_id = "living_room_light"
        self.name = "Living Room Light"
        self.is_on = False
        self.brightness = 100

    def on_connect(self, client, userdata, flags, rc):
        print(f"💡 {self.name} connected to MQTT broker")

        # Tell the world about this device (discovery)
        discovery = {
            "name": self.name,
            "command_topic": f"home/light/{self.device_id}/set",
            "state_topic": f"home/light/{self.device_id}/state",
            "brightness": True,
            "device": {
                "identifiers": [self.device_id],
                "name": self.name,
                "manufacturer": "Demo Corp",
                "model": "DemoLight Pro"
            }
        }

        client.publish(
            f"homeassistant/light/{self.device_id}/config",
            json.dumps(discovery),
            retain=True
        )

        # Listen for commands
        client.subscribe(f"home/light/{self.device_id}/set")

        # Report current state
        self.report_state()

    def on_message(self, client, userdata, msg):
        # Handle commands like "turn on" or "set brightness"
        try:
            command = json.loads(msg.payload.decode())
            if "state" in command:
                self.is_on = command["state"].upper() == "ON"
            if "brightness" in command:
                self.brightness = command["brightness"]

            print(f"💡 Light command received: {command}")
            self.report_state()
        except:
            pass

    def report_state(self):
        # Tell everyone the current state of the light
        state = {
            "state": "ON" if self.is_on else "OFF",
            "brightness": self.brightness,
            "timestamp": datetime.now().isoformat()
        }

        self.client.publish(
            f"home/light/{self.device_id}/state",
            json.dumps(state)
        )
        print(f"💡 Light state: {state}")

    def run(self):
        # Connect to the MQTT broker and keep running
        time.sleep(3)
        self.client.connect("mosquitto", 1883, 60)
        self.client.loop_forever()

if __name__ == "__main__":
    light = SmartLight()
    light.run()

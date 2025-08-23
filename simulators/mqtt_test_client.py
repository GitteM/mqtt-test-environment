#!/usr/bin/env python3
"""
MQTT Test Client - Subscribe to all topics and print messages
Useful for debugging and seeing what your simulators are publishing
"""

import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime

class MQTTTestClient:
    def __init__(self, broker_host="mosquitto", broker_port=1883):
        self.client = mqtt.Client(client_id="mqtt_monitor")
        self.broker_host = broker_host
        self.broker_port = broker_port

        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("✅ Connected to MQTT Broker!")
            # Subscribe to all topics for testing
            client.subscribe("home/+/+/+")  # home/light/device_id/state
            client.subscribe("homeassistant/+/+/+")  # homeassistant discovery
            print("📡 Subscribed to all sensor and device topics")
        else:
            print(f"❌ Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        timestamp = datetime.now().strftime("%H:%M:%S")

        try:
            # Try to parse as JSON for pretty printing
            data = json.loads(payload)
            print(f"📨 [{timestamp}] [{topic}] {json.dumps(data, indent=2)}")
        except json.JSONDecodeError:
            # If not JSON, just print as string
            print(f"📨 [{timestamp}] [{topic}] {payload}")

    def on_disconnect(self, client, userdata, rc):
        print("🔌 Disconnected from MQTT Broker")

    def run(self):
        print(f"🚀 Starting MQTT Test Client...")
        print(f"🔗 Connecting to {self.broker_host}:{self.broker_port}")

        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_forever()
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    client = MQTTTestClient()
    client.run()

# MQTT Test Environment

A complete Docker-based MQTT testing environment for developing and testing IoT device discovery applications. This containerized setup provides a local MQTT broker with simulated smart home devices that publish Home Assistant-compatible discovery messages, allowing you to test device discovery functionality without physical hardware.

## Project Overview

This environment simulates a realistic smart home MQTT setup with:
- **Mosquitto MQTT Broker** - Central message hub (ports 1883/9001)
- **Temperature Sensor Simulator** - Publishes readings every 30 seconds
- **Smart Light Simulator** - Controllable via MQTT commands
- **MQTT Test Client** - Monitors all traffic for debugging

All devices publish Home Assistant discovery messages to `homeassistant/+/+/config` topics and maintain state on `home/+/+/+` topics, providing a realistic testing scenario for MQTT device discovery applications.

## Use Cases

- **App Development**: Test MQTT device discovery without physical devices
- **Learning MQTT**: Understand Home Assistant auto-discovery protocols
- **Integration Testing**: Validate MQTT client implementations
- **Debugging**: Monitor live MQTT traffic and message formats

## Prerequisites

Before running the project, ensure you have the required tools installed:

### 1. Install Docker Desktop

**macOS:**
```bash
# Download and install from https://docker.com/products/docker-desktop
# Or using Homebrew:
brew install --cask docker
```

**Verify Docker installation:**
```bash
docker --version
docker-compose --version
```

### 2. Install Mosquitto MQTT Tools (Optional but Recommended)

For testing and debugging MQTT connections:

**macOS:**
```bash
brew install mosquitto
```

**Verify Mosquitto tools:**
```bash
mosquitto_pub --help
mosquitto_sub --help
```

### 3. Configure Mosquitto Service (Important!)

If you have Mosquitto running as a system service, it will conflict with the Docker broker on port 1883:

**Check if Mosquitto is running:**
```bash
# Check what's using port 1883
lsof -i :1883

# Check running processes
ps aux | grep mosquitto
```

**Stop Mosquitto service if running:**
```bash
# On macOS (with Homebrew)
brew services stop mosquitto

# Or kill all mosquitto processes
pkill mosquitto
```

**Start Mosquitto service (if needed later):**
```bash
brew services start mosquitto
```

### 4. Verify Docker is Running

Ensure Docker Desktop is running before proceeding:

```bash
# Check Docker status
docker info

# Test Docker functionality
docker run hello-world
```

**Troubleshooting:**
- If `docker info` fails, start Docker Desktop application
- If port 1883 is in use, stop any existing MQTT brokers
- On first run, Docker will download images (eclipse-mosquitto, python:3.9-slim)

## Quick Setup (Using bash script)

1. **Make script executable:**
   ```bash
   chmod +x setup.sh
   ```

2. **Start the environment:**
   ```bash
   ./setup.sh start
   ```

3. **View live MQTT messages:**
   ```bash
   ./setup.sh logs
   ```
   *This will wait for connections to establish, then show live messages*

4. **Send a test message:**
   ```bash
   ./setup.sh test
   ```

5. **Stop when done:**
   ```bash
   ./setup.sh stop
   ```

**Manual Method (if script doesn't work):**
```bash
# 1. Clean stop
docker-compose down

# 2. Start fresh
docker-compose up -d

# 3. Wait for connections (important!)
sleep 10

# 4. View messages manually
docker exec mqtt-test-client python /app/mqtt_test_client.py
```

**Note:** Always wait for connections to establish before checking logs. The simulators need time to connect to the MQTT broker.

## What You'll See

When the environment is running, you'll observe:

### Discovery Messages (Published once on startup)
```json
// homeassistant/light/living_room_light/config
{
  "name": "Living Room Light",
  "command_topic": "home/light/living_room_light/set",
  "state_topic": "home/light/living_room_light/state",
  "brightness": true,
  "device": {
    "identifiers": ["living_room_light"],
    "name": "Living Room Light",
    "manufacturer": "Demo Corp",
    "model": "DemoLight Pro"
  }
}

// homeassistant/sensor/kitchen_temp_sensor/config
{
  "name": "Kitchen Temperature",
  "state_topic": "home/sensor/kitchen_temp_sensor/temperature",
  "unit_of_measurement": "°C",
  "device_class": "temperature",
  "device": {
    "identifiers": ["kitchen_temp_sensor"],
    "name": "Kitchen Temperature",
    "manufacturer": "Demo Corp",
    "model": "TempSense Pro"
  }
}
```

### State Messages (Published regularly)
```json
// home/sensor/kitchen_temp_sensor/temperature (every 30 seconds)
{
  "temperature": 22.5,
  "timestamp": "2025-08-23T10:01:56.490196",
  "battery": 98
}

// home/light/living_room_light/state (on startup and command changes)
{
  "state": "OFF",
  "brightness": 100,
  "timestamp": "2025-08-23T10:01:56.490196"
}
```

## Project Structure

```
mqtt-test-environment/
├── docker-compose.yml         # Container orchestration
├── mosquitto.conf             # MQTT broker configuration
├── setup.sh                   # Management script
├── Dockerfile                 # Python environment for simulators
└── simulators/
    ├── temp_simulator.py      # Temperature sensor simulation
    ├── light_simulator.py     # Smart light simulation
    └── mqtt_test_client.py    # Message monitoring client
```

## Integration with Your App

Your MQTT device discovery application should:

1. **Connect** to `localhost:1883`
2. **Subscribe** to `homeassistant/+/+/config` for device discovery
3. **Parse** discovery JSON to create device objects
4. **Subscribe** to device state topics for real-time updates
5. **Publish** commands to device command topics for control

This setup provides realistic Home Assistant-compatible MQTT traffic for thorough testing.

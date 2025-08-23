#!/bin/bash

# MQTT Test Environment Management Script

case "$1" in
  "start")
    echo "🚀 Starting MQTT Test Environment..."
    docker-compose up --build -d
    echo ""
    echo "✅ Environment started!"
    echo "📱 Your mobile app should connect to: localhost:1883"
    echo "🌐 WebSocket clients can connect to: localhost:9001"
    echo ""
    echo "📊 To see live messages: ./setup.sh logs"
    ;;

  "stop")
    echo "🛑 Stopping MQTT Test Environment..."
    docker-compose down
    echo "✅ Environment stopped!"
    ;;

  "restart")
    echo "🔄 Restarting MQTT Test Environment..."
    docker-compose down
    docker-compose up --build -d
    echo "✅ Environment restarted!"
    ;;

  "logs")
    echo "📊 Live MQTT messages (Ctrl+C to exit):"
    echo "⏳ Waiting for connections to establish..."
    sleep 5
    if docker ps --format "table {{.Names}}" | grep -q mqtt-test-client; then
      docker exec mqtt-test-client python /app/mqtt_test_client.py
    else
      echo "❌ mqtt-test-client container not running. Try: ./setup.sh start"
    fi
    ;;

  "status")
    echo "📋 Container Status:"
    docker-compose ps
    echo ""
    echo "🔍 Quick Connection Test:"
    echo "Run this in another terminal: mosquitto_pub -h localhost -t test/topic -m 'Hello MQTT'"
    ;;

  "test")
    echo "🧪 Testing MQTT connection..."
    if command -v mosquitto_pub &> /dev/null; then
      mosquitto_pub -h localhost -t test/mobile-app -m '{"message":"Hello from setup script","timestamp":"'$(date -Iseconds)'"}'
      echo "✅ Test message sent! Check your logs with: ./setup.sh logs"
    else
      echo "⚠️  mosquitto_pub not found. Install with: brew install mosquitto"
    fi
    ;;

  "clean")
    echo "🧹 Cleaning up Docker resources..."
    docker-compose down
    docker system prune -f
    echo "✅ Cleanup complete!"
    ;;

  *)
    echo "🔧 MQTT Test Environment Manager"
    echo ""
    echo "Usage: ./setup.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start    - Start all containers"
    echo "  stop     - Stop all containers"
    echo "  restart  - Restart all containers"
    echo "  logs     - View live MQTT messages"
    echo "  status   - Show container status"
    echo "  test     - Send a test message"
    echo "  clean    - Clean up Docker resources"
    echo ""
    echo "📱 Mobile App Connection:"
    echo "  Host: localhost (or your computer's IP)"
    echo "  Port: 1883"
    echo ""
    ;;
esac

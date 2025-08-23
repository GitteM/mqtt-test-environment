FROM python:3.9-slim

# Install required Python packages first
RUN pip install paho-mqtt==1.6.1

# Set working directory
WORKDIR /app

# Copy simulator scripts
COPY simulators/ ./

# Make sure we're in the right directory and list files for debugging
RUN ls -la /app

# Default command
CMD ["python", "/app/temp_simulator.py"]

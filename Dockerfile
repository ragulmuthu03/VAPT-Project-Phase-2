# Use a base image with Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN apt-get update && apt-get install -y xvfb \
    && pip install --no-cache-dir -r requirements.txt

# Start a virtual display for PyQt5 UI
RUN Xvfb :99 -screen 0 1024x768x24 &

# Set environment variables
ENV DISPLAY=:99.0

# Define the entry point (CLI or UI)
CMD ["python3", "tidconsole.py"]

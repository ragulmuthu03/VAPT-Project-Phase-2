# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the application
EXPOSE 8080

# Set environment variables if needed
ENV DISPLAY=:99

# Run the UI application (change entry point if needed)
CMD ["python3", "tidconsole.py"]

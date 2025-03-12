# Use an official lightweight Python image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install all required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port (if needed for future API integrations)
EXPOSE 5000

# Command to run the CLI version
CMD ["python3", "tidconsole.py"]

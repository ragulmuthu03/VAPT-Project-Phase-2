# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the CLI tool
CMD ["python3", "tidconsole.py", "--help"]

# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install necessary packages for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

COPY static/ ./static/

# Expose the port
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
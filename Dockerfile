# Use Python 3.9 as base image
FROM --platform=$BUILDPLATFORM public.ecr.aws/docker/library/python:3.9-slim AS builder


# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Remove any existing .pyc files and pycache directories
RUN find . -type f -name "*.pyc" -delete && \
    find . -type d -name "__pycache__" -delete

# Create a non-root user
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose the port your application runs on
EXPOSE 5000

# Default command (can be overridden in docker-compose)
CMD ["python", "app.py"]
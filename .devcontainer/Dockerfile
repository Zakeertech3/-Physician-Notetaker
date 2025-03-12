# Use the official Python 3.9 slim image as the base
FROM python:3.9-slim

# Install system dependencies if needed
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /workspace


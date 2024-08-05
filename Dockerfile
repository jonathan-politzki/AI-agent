# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script to the container
COPY hello_world.py .

# Run the Python script when the container launches
CMD ["python", "hello_world.py"]
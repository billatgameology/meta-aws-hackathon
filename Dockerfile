# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir flask

# Expose the port that the Flask app will run on
EXPOSE 80

# Define the command to run your app
CMD ["python", "app.py"]

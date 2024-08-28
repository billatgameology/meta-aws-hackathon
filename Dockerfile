# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir flask

# Expose the port that the Flask app will run on
EXPOSE 8080

# Define the command to run your app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]

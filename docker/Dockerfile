# Use the official Python image as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY app/ ./app
COPY config/ ./config
COPY models/ ./models
COPY utils/ ./utils
COPY logs/ ./logs

# Expose the port the app runs on
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app/main.py"]
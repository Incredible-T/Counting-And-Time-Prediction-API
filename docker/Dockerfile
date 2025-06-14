# Use the official Python image as a parent image
FROM python:3.12-slim

# Update package lists and install security updates
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --timeout=1000 -r requirements.txt

# Create a non-root user
RUN useradd -m appuser

# Copy the rest of the application code into the container
COPY app/ ./app
COPY config/ ./config
COPY docker/ ./docker
COPY logs/ ./logs

# Expose the port the app runs on
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
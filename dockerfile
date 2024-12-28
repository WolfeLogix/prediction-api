# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Remove the requirements file
RUN rm requirements.txt

# Update and install additional requirements
RUN apt-get update && apt-get upgrade -y && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Use a non-root user
RUN useradd -m appuser

# Copy the application code and change ownership
COPY --chown=appuser:appuser ./app /app

# Change ownership of the working directory
RUN chown -R appuser:appuser /app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Expose the port
EXPOSE 8080

# Switch to the non-root user
USER appuser

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
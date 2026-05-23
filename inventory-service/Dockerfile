# Start from an official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (for faster rebuilds)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service code
COPY main.py .

# Tell Docker which port this service uses
EXPOSE 8001

# Command to start the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
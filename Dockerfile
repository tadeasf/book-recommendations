# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.lock .
RUN mv requirements.lock requirements.txt
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose the port
EXPOSE 6969

# Run the application with uvicorn
CMD ["uvicorn", "src.book_recommendations.main:app", "--host", "0.0.0.0", "--port", "6969", "--reload"]

# Use multi-stage build for smaller final image
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first
COPY requirements.lock .
COPY pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.lock

# Copy the rest of the application
COPY . .

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Set environment variables for Cloud Run
ENV PORT=8080
ENV HOST=0.0.0.0

# Run migrations and start the application
CMD alembic upgrade head && uvicorn src.book_recommendations.main:app --host $HOST --port $PORT

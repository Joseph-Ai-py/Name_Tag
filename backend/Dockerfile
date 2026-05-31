FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libglib2.0-0 \
    libgobject-2.0-0 \
    libpangoft2-1.0-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Create logs directory
RUN mkdir -p /logs

# Expose port
EXPOSE 8000

# Set Python path
ENV PYTHONPATH=/app:${PYTHONPATH}

# Run FastAPI with unbuffered output
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

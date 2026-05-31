FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (WeasyPrint 요구사항 및 한글 폰트 추가)
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libjpeg-dev \
    libopenjp2-7-dev \
    libffi-dev \
    fonts-nanum \
    libcairo2 \
    libjpeg62-turbo \
    libgdk-pixbuf-2.0-0 \
    libgobject-2.0-0 \
    libpangocairo-1.0-0 \
    libpixman-1-0 \
    libpng16-16 \
    libssl3 \
    libxml2 \
    libxslt1.1 \
    libzstd1 \
    shared-mime-info \
    fonts-dejavu-core \
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

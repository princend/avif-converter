FROM python:3.9-slim

# Install system dependencies required for image processing
RUN apt-get update && apt-get install -y \
    libavif-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Use standard requirements without limiting versions for Python 3.9
RUN echo "Flask\nPillow\npillow-avif-plugin\ngunicorn" > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Use Gunicorn for production
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]

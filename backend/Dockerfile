FROM python:3.12-slim-bookworm

WORKDIR /app

# Set production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Install minimal dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app ./app

# Expose default Cloud Run port
EXPOSE 8080

# Run FastAPI with uvicorn
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}

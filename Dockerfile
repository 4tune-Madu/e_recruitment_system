# Use official Python image
FROM python:3.11-slim-bullseye

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    libjpeg-dev \
    zlib1g-dev \
    libxml2 \
    libxslt1.1 \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (ignore errors)
RUN python manage.py collectstatic --noinput || true

# Expose port 8000
EXPOSE 8000

# Run app with Gunicorn
CMD ["gunicorn", "recruitment.wsgi:application", "--bind", "0.0.0.0:8000"]
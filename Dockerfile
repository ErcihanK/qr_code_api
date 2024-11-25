# Use an official lightweight Python image.
# 3.12-slim variant is chosen for a balance between size and utility.
FROM python:3.12-slim

# Set environment variables:
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
# PYTHONFAULTHANDLER: Enables the fault handler for segfaults
# PIP_NO_CACHE_DIR: Disables the pip cache for smaller image size
# PIP_DEFAULT_TIMEOUT: Avoids hanging during install
# PIP_DISABLE_PIP_VERSION_CHECK: Suppresses the "new version" message
# POETRY_VERSION: Specifies the version of poetry to install
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements, to cache them in Docker layer
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . .

# Create QR codes directory
RUN mkdir -p qr_codes && chmod 777 qr_codes

# Run the application as a non-root user for security
RUN useradd -m myuser
USER myuser

# Tell Docker about the port we'll run on.
EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
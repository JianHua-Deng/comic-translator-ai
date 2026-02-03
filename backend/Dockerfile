# Start with a clean, official Python 3.11 image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ca-certificates \
    libgl1 \
    libglib2.0-0 \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*


# Define a build argument with a default value of "true"
ARG USE_CUDA=true

# Conditional installation logic
# If USE_CUDA is true, install from the CUDA 12.6 wheel (GPU) (You might need to modify the the torch version link below based on your GPU)
# If USE_CUDA is false, install from the CPU wheel (Smaller image size)
RUN if [ "$USE_CUDA" = "true" ]; then \
        echo "Building with CUDA Support (GPU)..." && \
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128; \
    else \
        echo "Building with CPU Support Only..." && \
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu; \
    fi
# --- CONFIGURATION END ---

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install remaining dependencies
# (Ensure torch/torchvision are commented out in requirements.txt)
RUN pip install -r /app/requirements.txt

# Copy application code
COPY . /app

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

ENV PORT=8000
EXPOSE 8000

# Run uvicorn
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
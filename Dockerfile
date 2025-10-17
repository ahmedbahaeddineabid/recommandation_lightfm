FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=4

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    gfortran \
    pkg-config \
    python3-dev \
    git \
    curl \
    libopenblas-dev \
    liblapack-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel cython
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --no-binary=:all: lightfm \
    && pip install --no-cache-dir streamlit

# Copy app code
COPY . /app

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit (change "streamlit_app.py" to your file)
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

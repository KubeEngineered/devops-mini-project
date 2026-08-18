# ==========================================
# STAGE 1: Build & Install Dependencies
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies into a local prefix directory or virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# STAGE 2: Lightweight Runtime
# ==========================================
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user for security best practices
RUN useradd -ms /bin/bash pyuser
USER pyuser

# Copy installed python packages from the builder stage
COPY --from=builder --chown=pyuser:pyuser /root/.local /home/pyuser/.local

# Copy application source code
COPY --chown=pyuser:pyuser app.py .

# Ensure local user binaries are in PATH
ENV PATH=/home/pyuser/.local/bin:$PATH

# Run the python script
CMD ["python", "app.py"]

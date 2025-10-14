FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project metadata required for installation
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Copy and install smithery shim to PATH
COPY smithery /usr/local/bin/smithery
RUN chmod +x /usr/local/bin/smithery

# Expose port (if needed)
EXPOSE 3000

# Run the application - prefer direct Python invocation
CMD ["python", "main.py"]
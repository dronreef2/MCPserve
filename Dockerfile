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

# Expose port (if needed)
EXPOSE 3000

# Run the application
CMD ["sh", "-c", "python main.py"]
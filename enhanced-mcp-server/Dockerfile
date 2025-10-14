FROM python:3.12-bookworm AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
ENV PATH="/root/.local/bin:$PATH"
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Production stage
FROM python:3.12-bookworm AS runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && mkdir -p /app \
    && chown -R app:app /app

# Set work directory
WORKDIR /app

# Copy application code
COPY --chown=app:app . .

# Switch to non-root user
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import enhanced_mcp_server; print('OK')" || exit 1

# Expose port for web interface
EXPOSE 8001

# Default command
CMD ["python", "-m", "enhanced_mcp_server.main"]
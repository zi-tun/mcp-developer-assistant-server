# Use Python 3.13 to match your development environment
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create app directory
WORKDIR /app

# Install uv for faster dependency management
RUN pip install uv

# Copy dependency files
COPY uv_requirements.txt .

# Install dependencies using uv
RUN uv pip install --system -r uv_requirements.txt

# Copy application code
COPY . .


# Expose port 8080 (or make it configurable)
EXPOSE 8080

# Run MCP server in HTTP mode
CMD ["python", "main.py"]

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY deployment_requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "main:app"]
# Use a slim Python image for a smaller footprint
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser

# Copy requirements and install them
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY app/ .

# Set ownership to our non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the application port
EXPOSE 5000

# Use Gunicorn as a production-ready WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
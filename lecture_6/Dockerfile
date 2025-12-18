# Use Python 3.10.8 as the base image
FROM python:3.10.8-slim

# Prevent Python from writing __pycache__ 
ENV PYTHONDONTWRITEBYTECODE=1

# Needed for instant log output in Docker (disables output buffering)
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .

# Install Python dependencies without caching to reduce image size
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Start the application using Python, which runs uvicorn inside main.py
# Alternatively, uvicorn could be started directly as: CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "main.py"]

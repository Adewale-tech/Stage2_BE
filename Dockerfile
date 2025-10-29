
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt first for dependency caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose the port your app will run on
EXPOSE 8000

# Command to run the app
CMD ["python", "main.py"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

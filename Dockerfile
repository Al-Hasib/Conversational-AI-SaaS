# 1. Use official Python image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the application code
COPY . .

# 5. Expose port
EXPOSE 8000

# 6. Run the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

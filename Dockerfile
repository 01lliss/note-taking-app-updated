# Use slim Python image for smaller footprint
FROM python:3.11-slim

# set workdir
WORKDIR /app

# copy only dependency files first for better caching
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

# Expose is informational; Vercel provides the port via $PORT at runtime
EXPOSE 5001

# Run gunicorn using the PORT environment variable provided by Vercel
# Use shell form so that $PORT is expanded at container runtime
CMD ["sh", "-lc", "gunicorn -b 0.0.0.0:$PORT src.main:app --workers 2"]

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

# Expose port (Vercel will handle mapping)
EXPOSE 5001

# Use gunicorn to run the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:5001", "src.main:app", "--workers", "2"]

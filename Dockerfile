# Use official Python image
FROM python:3.12


# Set working directory
WORKDIR /app


# Install system dependencies to run psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


#Copy requirements file and install dependencies
COPY requirements.txt .


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .


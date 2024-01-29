FROM python:3.9

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.pip .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.pip

# Copy the application code
COPY pc_builder_backend/ .

CMD ["python", "app.py"]

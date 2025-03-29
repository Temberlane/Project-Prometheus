# filepath: /Users/thomas/GitHub/Project-Prometheus/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y protobuf-compiler && rm -rf /var/lib/apt/lists/*

# Copy files
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Compile proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. distributed_ai.proto

EXPOSE 50051

CMD ["python", "node_server.py"]
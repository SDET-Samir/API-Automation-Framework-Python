FROM python:3.11-slim
WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly copy web directories to guarantee UI delivery inside the container sandbox
COPY templates/ ./templates/
COPY static/ ./static/

COPY . .
EXPOSE 5000
CMD ["python", "server.py"]

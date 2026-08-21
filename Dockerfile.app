FROM python:3.11-slim

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application scripts, templates, and style sheets into the image workspace context smoothly
COPY . .

EXPOSE 5000

CMD ["python", "server.py"]

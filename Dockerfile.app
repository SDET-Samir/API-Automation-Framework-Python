FROM python:3.11-slim
WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Case-insensitive wildcard mappings to find the folders regardless of casing
COPY [tT]emplates/ ./templates/
COPY [sS]tatic/ ./static/

COPY . .
EXPOSE 5000
CMD ["python", "server.py"]

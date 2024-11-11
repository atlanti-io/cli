FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    patchelf \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt && pip install nuitka

WORKDIR /app
COPY . .

ARG ARCH
RUN nuitka --standalone --onefile --include-data-dir=apps=apps --output-filename=atlanti main.py

RUN mkdir -p /app/output && mv /app/atlanti /app/output/atlanti

RUN chmod +x /app/output/atlanti && ls -lh /app/output/atlanti
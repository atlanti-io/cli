FROM python:3.10-slim

RUN mkdir -p /app/output && chmod -R 777 /app

RUN apt-get update && apt-get install -y \
    build-essential \
    patchelf \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt && pip install nuitka

COPY . .

ARG ARCH

RUN nuitka --standalone --onefile --include-data-dir=apps=apps --output-filename=atlanti main.py

RUN chmod +x /app/output/atlanti && ls -lh /app/output/atlanti

# Użyj obrazu Python 3.12.3
FROM python:3.12.3-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiowanie wszystkich plików projektu
COPY . .

# Instalacja zależności systemowych potrzebnych dla FAISS
RUN apt-get update && apt-get install -y gcc && apt-get clean

# Instalacja zależności Pythonowych
RUN pip install --no-cache-dir -r requirements.txt

# Uniwersalny punkt startowy – określany w docker-compose.yml
CMD ["python", "run_publisher.py"]

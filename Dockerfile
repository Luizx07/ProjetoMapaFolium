FROM python:3

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY App/mapa.py .
COPY App/capitais_brasil_ibge.csv .

CMD ["python", "mapa.py"]
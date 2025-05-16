FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

# Instala gcc y libpq-dev para compilar psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
# CMD ["python", "app.py"]
# CMD ["flask", "run", "--host=
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
ENV DB_PATH=/data/customers.db

RUN mkdir -p /data

EXPOSE 8080

CMD ["python", "app.py"]

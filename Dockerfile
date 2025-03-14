FROM python:3.13

WORKDIR /app

COPY requirements.txt requirements.txt
COPY app.py app.py
COPY templates templates

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]

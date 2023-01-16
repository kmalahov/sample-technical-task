FROM python:3.9-slim

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python3", "main.py"]
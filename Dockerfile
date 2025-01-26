FROM python:3.11-slim

WORKDIR /main

COPY requirements.txt /main

RUN pip install --no-cache-dir -r requirements.txt

COPY . /main

CMD ["python", "main.py"]
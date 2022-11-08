# syntax=docker/dockerfile:1

FROM python:3.9.0

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python", "-u", "server1.py"]
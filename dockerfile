FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y iputils-ping

COPY . .

CMD [ "python3", "main.py"]
FROM python:3.8

WORKDIR /cmd

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3 main.py" ]
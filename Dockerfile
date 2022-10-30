FROM python:3.9-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ls
COPY app.py .
CMD ls
COPY project project
CMD flask run -h 0.0.0.0 -p 80

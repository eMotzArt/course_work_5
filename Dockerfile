FROM python:3.9-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY project project
EXPOSE 80
CMD flask run -h 0.0.0.0 -p 80


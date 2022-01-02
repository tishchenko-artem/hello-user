FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY . /app
WORKDIR /app
ENV FLASK_APP=app.py FLASK_ENV=production DATABASE_URL='sqlite:///db.sqlite3' DATABASE_URL_DIRECT='db.sqlite3'
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]
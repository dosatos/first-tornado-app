FROM python:3.6

EXPOSE 8888

# RUN apt-get update && apt-get install -y mysql-client

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader averaged_perceptron_tagger

COPY . /usr/src/app

CMD ["python", "app.py"]
# --mysql_host=mysql
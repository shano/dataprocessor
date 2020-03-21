FROM python:buster3.7
COPY . /app
WORKDIR /app
RUN apt-get install python-pip python-dev libmysqlclient-dev
RUN pip install -r requirements.txt
CMD python ./index.py
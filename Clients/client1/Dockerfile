FROM ubuntu:18.04
RUN apt-get clean && apt-get update -qqy
RUN apt-get install -qqy python-pip
RUN apt-get install -qqy python3-pip
RUN pip3 install thrift
RUN pip3 install Flask

COPY ./src ./src
COPY ./client.py ./client.py

CMD ["python3", "./client.py"]
FROM ubuntu:18.04
RUN apt-get clean && apt-get update -qqy
RUN apt-get install -qqy python3-pip
RUN pip3 install thrift

COPY ./gen-py ./gen-py
COPY ./country_server.py ./country_server.py

CMD ["python3", "./country_server.py"]

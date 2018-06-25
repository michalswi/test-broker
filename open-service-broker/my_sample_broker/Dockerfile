# docker build -t local/sample-broker:v0.1.0 .

FROM frolvlad/alpine-python2

# ENV http_proxy=..
# ENV https_proxy=..

RUN pip install flask

WORKDIR /app

ADD sample_broker.py sample_broker.py
ADD sample_health_check.py sample_health_check.py

ENTRYPOINT ["./sample_broker.py"]
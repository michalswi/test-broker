#docker build -t local/run-broker:v0.1.0 .
FROM frolvlad/alpine-python3

# ENV http_proxy=...
# ENV https_proxy=...

RUN pip3 install flask
RUN pip3 install openbrokerapi
WORKDIR /app

ADD run_broker.py run_broker.py

# EXPOSE 5000

ENTRYPOINT ["./run_broker.py"]

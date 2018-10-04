FROM python:3-alpine

WORKDIR /build

COPY . ./

COPY ./boatd-config.yaml.example /opt/boatd/config/boatd-config.yaml
COPY ./example/basic_behaviour.py /opt/boatd/behaviours/
COPY ./example/basic_driver.py /opt/boatd/drivers/
COPY ./bin/boatd /usr/local/bin/

# Bind on all adapters so dockers bridge network works as expected
RUN sed -i.bak 's/127\.0\.0\.1/0\.0\.0\.0/' /opt/boatd/config/boatd-config.yaml && \
    rm /opt/boatd/config/boatd-config.yaml.bak

RUN pip3 install -r requirements.txt && \
    python3 setup.py install && \
    rm -rf /build

EXPOSE 2222

ENV PYTHONUNBUFFERED 1

ENV CONFIG /opt/boatd/config/boatd-config.yaml

ENTRYPOINT ["/bin/sh", "-c", "boatd ${CONFIG}"]
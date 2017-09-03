FROM makercrew/pi-python-iot:latest
LABEL maintainer="kevin@sidwar.com"

WORKDIR /home/gateway/
RUN pip install paho-mqtt && \
    git clone https://github.com/etrombly/RFM69.git

ENTRYPOINT []

ADD ./gateway.py ./gateway.py

CMD ["python", "gateway.py"]
ARG UBUNTU_VERSION=24.04

FROM ubuntu:${UBUNTU_VERSION}

RUN apt update && \
    apt install -y python3 python3-pip python3-venv

RUN python3 -m venv /venv

ENV PATH="/venv/bin:$PATH"
RUN pip install pyzmq

WORKDIR /app
COPY . .

CMD ["bash"]

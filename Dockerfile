FROM python:3.7

# Install OpenJDK 8, and monitoring tooling
RUN \
  apt-get update && \
  apt-get install -y openjdk-11-jre-headless && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade setuptools
COPY requirements.txt /
RUN pip install -r /requirements.txt

ENV PATH=$PATH:/src
ENV PYTHONPATH /src

ADD ./ /src
WORKDIR /src/

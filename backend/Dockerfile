FROM python:3.9
RUN mkdir /usr/src/time-circle /usr/src/time-circle/logs -p
COPY . /usr/src/time-circle
WORKDIR /usr/src/time-circle
RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
WORKDIR /usr/src/time-circle
CMD bin/run.sh

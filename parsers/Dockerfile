FROM ubuntu:latest

ADD app.py /root/app.py
ADD models.py /root/models.py

RUN apt-get update
RUN apt-get -y install cron python3.11 python3-pip
RUN pip3 install redis_om fastapi uvicorn requests
RUN crontab -l | { cat; echo "* * * * * python3 /root/app.py"; } | crontab -

CMD cron
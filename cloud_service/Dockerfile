FROM python:3.9-slim

WORKDIR /app/cloud_service

# install chromium and driver
RUN apt-get update && apt-get install -y \
    vim \
    tzdata \
    cron

# update timezone
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

COPY . /app/cloud_service
COPY ./config/crontab /etc/cron.d/crontab

RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod 0644 /etc/cron.d/crontab

CMD ["/usr/sbin/cron", "-f"]

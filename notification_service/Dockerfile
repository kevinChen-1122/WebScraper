FROM python:3.9-slim

WORKDIR /app/notification_service

# install chromium and driver
RUN apt-get update && apt-get install -y \
    vim \
    tzdata \
    cron \
    supervisor \
    ca-certificates && \
    apt-get clean

# update timezone
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

COPY . /app/notification_service
COPY ./config/crontab /etc/cron.d/crontab
COPY ./config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod 0644 /etc/cron.d/crontab

#CMD ["/usr/sbin/cron", "-f"]
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


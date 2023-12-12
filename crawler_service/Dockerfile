FROM python:3.9-slim

WORKDIR /app/crawler_service

# install chromium and driver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    vim \
    tzdata

# update timezone
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata

COPY . /app/crawler_service

RUN pip3 install --no-cache-dir -r requirements.txt

CMD python3 main.py & tail -f /dev/null
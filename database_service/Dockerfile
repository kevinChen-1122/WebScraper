FROM mongo:latest

COPY config/mongod.conf /etc/mongod.conf
COPY deployment/mongo_init.sh /docker-entrypoint-initdb.d/mongo_init.sh

CMD ["mongod"]
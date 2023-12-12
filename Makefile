SERVICES := crawler-service database-service

.PHONY: all build start stop restart logs clean

all: build

build:
	@for service in $(SERVICES); do \
  		echo "Building $$service..."; \
  		docker-compose build --no-cache $$service; \
    done

up:
	@docker-compose up -d

down:
	@docker-compose down

restart: down up

logs:
	@docker-compose logs -f

clean:
	@docker-compose down --volumes

shell:
	@docker exec -it $(t) /bin/bash

SERVICES := crawler-service database-service

.PHONY: all build start stop restart logs clean

all: build

build:
	@for service in $(SERVICES); do \
  		echo "Building $$service..."; \
  		docker-compose build --no-cache $$service; \
    done

up:
ifdef $(service)
	@docker-compose up -d $(service)
else
	@docker-compose up -d
endif

down:
	@docker-compose down

restart: down up

logs:
ifdef $(service)
	@docker-compose logs -f $(service)
else
	@docker-compose logs -f
endif

clean:
	@docker-compose down --volumes

shell:
	@docker exec -it $(service) /bin/bash

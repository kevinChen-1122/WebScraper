# WebScraper
## Project Structure
```
WebScraper
├─ cloud_service/
│  ├─ config/
│  │  ├─ config.ini
│  │  └─ crontab
│  ├─ module/
│  │  ├─ __init__.py
│  │  ├─ get_config_module.py
│  │  ├─ google_spreadsheets_module.py
│  │  └─ mongo_module.py
│  ├─ Dockerfile
│  ├─ main.py
│  ├─ README.md
│  └─ requirements.txt
├─ crawler_service/
│  ├─ config/
│  │  ├─ carousell_query_params.json
│  │  ├─ config.ini
│  │  └─ crontab
│  ├─ crawler/
│  │  ├─ spiders/
│  │  │  ├─ __init__.py
│  │  │  └─ search_product.py
│  │  ├─ __init__.py
│  │  ├─ items.py
│  │  ├─ middlewares.py
│  │  ├─ pipelines.py
│  │  └─ settings.py
│  ├─ module/
│  │  ├─ __init__.py
│  │  ├─ generator_url_module.py
│  │  ├─ get_config_module.py
│  │  └─ search_product_module.py
│  ├─ Dockerfile
│  ├─ README.md
│  ├─ requirements.txt
│  └─ scrapy.cfg
├─ database_service/
│  └─ config/
│  │  └─ mongod.conf
│  └─ data/
│  └─ Dockerfile
├─ notification_service/
│  ├─ config/
│  │  ├─ config.ini
│  │  └─ crontab
│  ├─ module/
│  │  ├─ __init__.py
│  │  ├─ get_config_module.py
│  │  ├─ line_notify_module.py
│  │  └─ mongo_module.py
│  ├─ Dockerfile
│  ├─ main.py
│  ├─ README.md
│  └─ requirements.txt
├─ .gitattributes
├─ .gitignore
├─ docker-compose.yml
├─ Makefile
└─ README.md
```
---
## How To Use
- build image
    ```
    make build
    ```
- start container
    ```
    make up
    ```
- stop container
    ```
    make down
    ```
- enter container
    ```
    make bash service={container_name}
    ```
  container_name :
  - cloud-service 
  - crawler-service
  - database-service
  - notification-service
---
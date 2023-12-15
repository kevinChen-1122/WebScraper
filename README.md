# WebScraper
## Project Structure
```
WebScraper
├─ crawler_service/
│  ├─ config/
│  │  ├─ __init__.py
│  │  ├─ carousell_query_params.json
│  │  ├─ carousell_search_keyword.json
│  │  ├─ config.ini
│  │  └─ config.py
│  ├─ data/
│  ├─ log/
│  ├─ module/
│  │  ├─ __init__.py
│  │  ├─ logger.py
│  │  ├─ mongo_module.py
│  │  ├─ search_product.py
│  │  └─ url_generator.py
│  ├─ test/
│  │  ├─ __init__.py
│  │  └─ test.py
│  ├─ Dockerfile
│  ├─ main.py
│  ├─ README.md
│  └─ requirements.txt
├─ database_service/
│  └─ config/
│  │  └─ mongod.conf
│  └─ data/
│  └─ log/
│  └─ Dockerfile
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
    make shell t= {container_name}
    ```
  container_name :
  - crawler-service
---
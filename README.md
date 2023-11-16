# WebScraper
## Project Structure
```
WebScraper
├─ crawler_service/
│  ├─ config/
│  │  ├─ __init__.py
│  │  └─ config.py
│  ├─ data/
│  ├─ log/
│  ├─ module/
│  │  ├─ __init__.py
│  │  ├─ logger.py
│  │  ├─ search_product.py
│  │  └─ url_generator.py
│  ├─ test/
│  │  ├─ __init__.py
│  │  └─ test.py
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
    make shell t= {container_name}
    ```
  container_name :
  - crawler-service
---
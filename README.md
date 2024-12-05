# taller-NoSQL-redis
This project present some examples to get a overview of what is possible with Redis. These are located in `examples`.

# Instalation
## Docker

Start Docker
```bash
docker compose up --build -d
```

Run an especific file, from an especific folder, e.g. document-database create.
**Commands for data-store**
```bash
docker compose run --rm data-store create
docker compose run --rm data-store read
docker compose run --rm data-store update
docker compose run --rm data-store delete
```

**Commands for document-database**
```bash
docker compose run --rm document-database create
docker compose run --rm document-database query
```

**Commands for vector-database**
```bash
docker compose run --rm vector-database create
docker compose run --rm vector-database query
```
## Manual instalation
```bash
pip install -r requirements.txt
```

# taller-NoSQL-redis

install redis (manual instalation)
```bash
pip install redis==5.2.0
```

## Using docker, the best thing in the world
start docker (dont forget to stop it after)
```bash
docker compose up --build -d
```

run an especific file, from an especific folder, e.g. document-database create (for dante and lucas: modify the entrypoint to add more examples that can be runned with docker)
```bash
docker compose run --rm document-database create
docker compose run --rm document-database query
```
NOTE: not working in data-store because it doesn't have create or query
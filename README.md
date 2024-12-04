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

run an especific file, e.g. data-store (for dante and lucas: modify the entrypoint to add more examples that can be runned with docker)
```bash
docker compose run --rm python-app data-store
```
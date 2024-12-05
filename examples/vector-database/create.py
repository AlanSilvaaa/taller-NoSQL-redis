"""
EXAMPLE FROM: https://redis.io/docs/latest/develop/get-started/vector-database/
"""

import os
import redis
import requests
import numpy as np
from redis.commands.search.field import (
    NumericField,
    TagField,
    TextField,
    VectorField,
)
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from sentence_transformers import SentenceTransformer

# Fetch the data
URL = ("https://raw.githubusercontent.com/bsbodden/redis_vss_getting_started"
       "/main/data/bikes.json")
response = requests.get(URL, timeout=10)
bikes = response.json()

# Connect to Redis
# use the REDIS_HOST environment variable if running on docker
# or localhost if running localy
redis_host = os.getenv('REDIS_HOST', 'localhost')
client = redis.Redis(host=redis_host, port=6379, decode_responses=True)
assert client.ping(), "Unable to connect to Redis"

# Populate the data
pipeline = client.pipeline()
for i, bike in enumerate(bikes, start=1):
    redis_key = f"bikes:{i:03}"
    pipeline.json().set(redis_key, "$", bike)
pipeline.execute()

# Generate and store embeddings
descriptions = [
    item for sublist in client.json().mget(client.keys("bikes:*"), "$.description")
    for item in sublist
]
embedder = SentenceTransformer("msmarco-distilbert-base-v4")
embeddings = embedder.encode(descriptions).astype(np.float32).tolist()

pipeline = client.pipeline()
for key, embedding in zip(client.keys("bikes:*"), embeddings):
    pipeline.json().set(key, "$.description_embeddings", embedding)
pipeline.execute()

# Create index schema
VECTOR_DIMENSION = len(embeddings[0])
schema = (
    TextField("$.model", no_stem=True, as_name="model"),
    TextField("$.brand", no_stem=True, as_name="brand"),
    NumericField("$.price", as_name="price"),
    TagField("$.type", as_name="type"),
    TextField("$.description", as_name="description"),
    VectorField(
        "$.description_embeddings",
        "FLAT",
        {
            "TYPE": "FLOAT32",
            "DIM": VECTOR_DIMENSION,
            "DISTANCE_METRIC": "COSINE",
        },
        as_name="vector",
    ),
)
definition = IndexDefinition(prefix=["bikes:"], index_type=IndexType.JSON)
client.ft("idx:bikes_vss").create_index(fields=schema, definition=definition)

print("Index and data creation completed successfully.")

"""
EXAMPLE FROM: https://redis.io/docs/latest/develop/get-started/vector-database/
"""

import os
import redis
import numpy as np
import pandas as pd
from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer

# Connect to Redis
# use the REDIS_HOST environment variable if running on docker
# or localhost if running localy
redis_host = os.getenv('REDIS_HOST', 'localhost')
client = redis.Redis(host=redis_host, port=6379, decode_responses=True)
assert client.ping(), "Unable to connect to Redis"

# Queries to execute
queries = [
    "Bike for small kids",
    "Best Mountain bikes for kids",
    "Cheap Mountain bike for kids",
    "Female specific mountain bike",
    "Road bike for beginners",
    "Commuter bike for people over 60",
    "Comfortable commuter bike",
    "Good bike for college students",
    "Mountain bike for beginners",
    "Vintage bike",
    "Comfortable city bike",
]

# Generate embeddings for queries
embedder = SentenceTransformer("msmarco-distilbert-base-v4")
encoded_queries = embedder.encode(queries).astype(np.float32)


def create_query_table(query, encoded_queries, query_texts, extra_params=None):
    """
    Creates a query table.
    """
    results_list = []
    for i, encoded_query in enumerate(encoded_queries):
        result_docs = (
            client.ft("idx:bikes_vss")
            .search(
                query,
                {"query_vector": np.array(encoded_query, dtype=np.float32).tobytes()}
                | (extra_params if extra_params else {}),
            )
            .docs
        )
        for doc in result_docs:
            vector_score = round(1 - float(doc.vector_score), 2)
            results_list.append(
                {
                    "query": query_texts[i],
                    "score": vector_score,
                    "id": doc.id,
                    "brand": doc.brand,
                    "model": doc.model,
                    "description": doc.description,
                }
            )

    queries_table = pd.DataFrame(results_list)
    queries_table.sort_values(by=["query", "score"], ascending=[True, False], inplace=True)
    return queries_table


# KNN Query
knn_query = (
    Query("(*)=>[KNN 3 @vector $query_vector AS vector_score]")
    .sort_by("vector_score")
    .return_fields("vector_score", "id", "brand", "model", "description")
    .dialect(2)
)
knn_table = create_query_table(knn_query, encoded_queries, queries)
print(knn_table.to_markdown(index=False))

# Hybrid Query
hybrid_query = (
    Query("(@brand:Peaknetic)=>[KNN 3 @vector $query_vector AS vector_score]")
    .sort_by("vector_score")
    .return_fields("vector_score", "id", "brand", "model", "description")
    .dialect(2)
)
hybrid_table = create_query_table(hybrid_query, encoded_queries, queries)
print(hybrid_table.to_markdown(index=False))

# Range Query
range_query = (
    Query(
        "@vector:[VECTOR_RANGE $range $query_vector]=>"
        "{$YIELD_DISTANCE_AS: vector_score}"
    )
    .sort_by("vector_score")
    .return_fields("vector_score", "id", "brand", "model", "description")
    .paging(0, 4)
    .dialect(2)
)
range_table = create_query_table(
    range_query, encoded_queries[:1], queries[:1], {"range": 0.55}
)
print(range_table.to_markdown(index=False))

import os
import redis

# Connect to Redis
# use the REDIS_HOST environment variable if running on docker
# or localhost if running localy
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

def create_entry(key, value):
    """Create a key-value pair in Redis."""
    r.set(key, value)
    print(f"Created key: {key} with value: {value}")

def create_hash(key, mapping):
    """Create a hash entry in Redis."""
    r.hset(key, mapping=mapping)
    print(f"Created hash: {key} with fields: {mapping}")

if __name__ == "__main__":
    # Create operations
    create_entry("foo", "bar")
    create_hash("user-session:123", {
        "name": "John",
        "surname": "Smith",
        "company": "Redis",
        "age": 29
    })
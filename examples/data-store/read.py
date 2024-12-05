import os
import redis

# Connect to Redis
# use the REDIS_HOST environment variable if running on docker
# or localhost if running localy
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

def read_entry(key):
    """Read a value for a given key."""
    value = r.get(key)
    print(f"Value for key '{key}': {value}")
    return value

def read_hash(key):
    """Read all fields from a hash."""
    fields = r.hgetall(key)
    print(f"Fields for hash '{key}': {fields}")
    return fields

def read_hash_field(key, field):
    """Read a specific field from a hash."""
    value = r.hget(key, field)
    print(f"Value for field '{field}' in hash '{key}': {value}")
    return value

if __name__ == "__main__":
    # Read operations
    read_entry("foo")
    read_hash("user-session:123")
    read_hash_field("user-session:123", "name")
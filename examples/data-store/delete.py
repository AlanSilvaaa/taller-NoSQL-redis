import os
import redis

# Connect to Redis
# use the REDIS_HOST environment variable if running on docker
# or localhost if running localy
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

def delete_entry(key):
    """Delete a key-value pair."""
    r.delete(key)
    print(f"Deleted key: {key}")

def delete_hash_field(key, field):
    """Delete a specific field from a hash."""
    r.hdel(key, field)
    print(f"Deleted field '{field}' from hash '{key}'")

if __name__ == "__main__":
    # Delete operations
    delete_entry("foo")
    delete_hash_field("user-session:123", "age")
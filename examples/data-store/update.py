import os
import redis

# Connect to Redis
# use the REDIS_HOST environment variable if running on docker
# or localhost if running localy
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

def update_entry(key, new_value):
    """Update the value of a key."""
    r.set(key, new_value)
    print(f"Updated key: {key} with new value: {new_value}")

def update_hash_field(key, field, new_value):
    """Update a specific field in a hash."""
    r.hset(key, field, new_value)
    print(f"Updated field '{field}' in hash '{key}' with new value: {new_value}")

if __name__ == "__main__":
    # Update operations
    update_entry("foo", "baz")
    update_hash_field("user-session:123", "company", "Redis Labs")
import os
import redis

redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

r.set('foo', 'bar')
print(r.get('foo'))

r.hset('user-session:123', mapping={
    'name': 'John',
    "surname": 'Smith',
    "company": 'Redis',
    "age": 29
})

print(r.hget('user-session:123', 'name'))
print(r.hgetall('user-session:123'))
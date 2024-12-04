import redis
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.json.path import Path
from redis.commands.search.field import NumericField, TagField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
import os


# Connect to Redis
# use the REDIS_HOST environment variable if running on docker
# or localhost if running localy
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

index = r.ft("idx:bicycle")

res = index.search(Query("*"))
print("Documents found:", res.total)

res = index.search(Query("@model:Jigger"))
print(res)
# >>> Result{1 total, docs: [
# Document {
#   'id': 'bicycle:0',
#   'payload': None,
#   'json': '{
#       "brand":"Velorim",
#       "model":"Jigger",
#       "price":270,
#       ...
#       "condition":"new"
#    }'
# }]}

res = index.search(Query("@model:Jigger").return_field("$.price", as_field="price"))
print(res)
# >>> [Document {'id': 'bicycle:0', 'payload': None, 'price': '270'}]

res = index.search(Query("basic @price:[500 1000]"))
print(res)
# >>> Result{1 total, docs: [
# Document {
#   'id': 'bicycle:5',
#   'payload': None,
#   'json': '{
#       "brand":"Breakout",
#       "model":"XBN 2.1 Alloy",
#       "price":810,
#       ...
#       "condition":"new"
#    }'
# }]}

res = index.search(Query('@brand:"Noka Bikes"'))
print(res)
# >>> Result{1 total, docs: [
# Document {
#   'id': 'bicycle:4',
#   'payload': None,
#   'json': '{
#       "brand":"Noka Bikes",
#       "model":"Kahuna",
#       "price":3200,
#       ...
#       "condition":"used"
#    }'
# }]}

res = index.search(
    Query("@description:%analitics%").dialect(  # Note the typo in the word "analytics"
        2
    )
)
print(res)
# >>> Result{1 total, docs: [
# Document {
#   'id': 'bicycle:3',
#   'payload': None,
#   'json': '{
#       "brand":"Eva",
#       "model":"Eva 291",
#       "price":3400,
#       "description":"...using analytics from a body metrics database...",
#       "condition":"used"
#    }'
# }]}

res = index.search(
    Query("@description:%%analitycs%%").dialect(  # Note 2 typos in the word "analytics"
        2
    )
)
print(res)
# >>> Result{1 total, docs: [
# Document {
#   'id': 'bicycle:3',
#   'payload': None,
#   'json': '{
#       "brand":"Eva",
#       "model":"Eva 291",
#       "price":3400,
#       "description":"...using analytics from a body metrics database...",
#       "condition":"used"
#    }'
# }]}

res = index.search(Query("@model:hill*"))
print(res)
# >>> Result{1 total, docs: [
# Document {
#   'id': 'bicycle:1',
#   'payload': None,
#   'json': '{
#       "brand":"Bicyk",
#       "model":"Hillcraft",
#       "price":1200,
#       ...
#       "condition":"used"
#    }'
# }]}

res = index.search(Query("@model:*bike"))
print(res)
# >>> Result{1 total, docs: [
# Document {
#   'id': 'bicycle:6',
#   'payload': None,
#   'json': '{
#       "brand":"ScramBikes",
#       "model":"WattBike",
#       "price":2300,
#       ...
#       "condition":"new"
#   }'
# }]}

res = index.search(Query("w'H?*craft'").dialect(2))
print(res.docs[0].json)
# >>> {
#   "brand":"Bicyk",
#   "model":"Hillcraft",
#   "price":1200,
#   ...
#   "condition":"used"
# }


res = index.search(Query("mountain").with_scores())
for sr in res.docs:
    print(f"{sr.id}: score={sr.score}")

res = index.search(Query("mountain").with_scores().scorer("BM25"))
for sr in res.docs:
    print(f"{sr.id}: score={sr.score}")

req = aggregations.AggregateRequest("*").group_by(
    "@condition", reducers.count().alias("count")
)
res = index.aggregate(req).rows
print(res)
# >>> [['condition', 'refurbished', 'count', '1'],
#      ['condition', 'used', 'count', '4'],
#      ['condition', 'new', 'count', '5']]

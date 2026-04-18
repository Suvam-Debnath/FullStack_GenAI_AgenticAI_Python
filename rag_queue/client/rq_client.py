from redis import Redis
from rq import Queue

# Initialize the Redis connection and RQ queue
queue = Queue(connection=Redis(
    host="localhost",
    port="6379"
))
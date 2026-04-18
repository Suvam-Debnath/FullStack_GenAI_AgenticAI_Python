from redis import Redis
from rq import Queue

# rq queue running in docker 
queue = Queue(connection=Redis(
    host="localhost",
    port="6379"
))
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.worker import process_query

app = FastAPI()

# Define API endpoints
@app.get('/')
def root():
    return {"status": 'Server is up and running'}

# Endpoint to receive chat queries and enqueue them for processing
@app.post('/chat')
def chat(
        query: str = Query(..., description="The chat query of user")
):
    job = queue.enqueue(process_query, query)

    return { "status": "queued", "job_id": job.id }

# Endpoint to check the status of a job and retrieve the result
@app.get('/job-status')
def get_result(
        job_id: str = Query(..., description="Job ID")
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()
    
    return { "result":  result}
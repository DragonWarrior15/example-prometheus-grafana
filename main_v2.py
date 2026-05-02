"""Setup a FastAPI server exposing a /metrics endpoint
to broadcast custom metrics to Prometheus.
"""

from fastapi import FastAPI

app = FastAPI()

# Define a "path operation decorator" for the root URL
@app.get("/metrics")
def read_root():
    return {"message": "Hello World"}

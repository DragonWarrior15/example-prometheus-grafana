"""Setup a FastAPI server exposing a /metrics endpoint
to broadcast custom metrics to Prometheus.
"""

import asyncio
import random
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI, Response
from prometheus_client import (
    CollectorRegistry,
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    generate_latest,
)

# Use this to supppress the metrics for garbage collector etc
CUSTOM_REGISTRY = CollectorRegistry()

METRIC_SLOW = Counter(
    "counter_slow",
    "A simple Counter for slow updating metrics",
    registry=CUSTOM_REGISTRY,
)
METRIC_FAST = Gauge(
    "gauge_fast", "A simple Gauge for fast updating metrics", registry=CUSTOM_REGISTRY
)


async def metric_slow():
    # simulate a slow function
    await asyncio.sleep(5)
    # A continuously increasing metric, like Request Count
    METRIC_SLOW.inc()


async def metric_fast():
    # simulate a fast function
    await asyncio.sleep(2)
    # A point in time metric, like CPU Usage
    METRIC_FAST.set(random.randint(0, 100))


async def prometheus_metrics_loop():
    while True:
        # This can be any set of functions that have metrics
        await asyncio.gather(metric_slow(), metric_fast())
        # non blocking sleep, a simulation of polling interval
        await asyncio.sleep(10)


# Define the Lifespan (The modern way) to run the loop
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the background task
    task = asyncio.create_task(prometheus_metrics_loop())
    yield
    # Shutdown: Stop the task cleanly
    task.cancel()


# Pass the lifespan context manager here!
app = FastAPI(lifespan=lifespan)


# Define a "path operation decorator" for the root URL
@app.get("/metrics")
def get_metrics():
    return Response(generate_latest(CUSTOM_REGISTRY), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    # Standard uvicorn run command inside the script
    uvicorn.run(app, host="0.0.0.0", port=8000)

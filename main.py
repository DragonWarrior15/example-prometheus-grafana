import random
import time

from prometheus_client import Gauge, start_http_server, Summary

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")
ACTIVE_USERS_GAUGE = Gauge("active_users_count", "Current active users")
ACTIVE_USERS_GAUGE_VALUE: int = 0


# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)


def get_active_users():
    """A dummy function that fetches the current active users."""
    global ACTIVE_USERS_GAUGE_VALUE

    # we choose randomly if we want to increase or decrease the value
    if random.random() <= 0.6:
        # do increment
        _delta = random.randint(1, 20)
        ACTIVE_USERS_GAUGE_VALUE += _delta
        ACTIVE_USERS_GAUGE.inc(_delta)
    else:
        # decrease
        _delta = min(random.randint(1, 20), ACTIVE_USERS_GAUGE_VALUE)
        ACTIVE_USERS_GAUGE_VALUE -= _delta
        ACTIVE_USERS_GAUGE.dec(_delta)

    # some sleep timer
    time.sleep(2)


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(random.random())
        get_active_users()

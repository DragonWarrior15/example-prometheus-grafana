# example-prometheus-grafana
Tiny repo for demonstrating example of prometheus and grafana.

## `uv`
### Initial Setup
- Download using `curl -LsSf https://astral.sh/uv/install.sh | sh`
    - Do check the official website for latest installation instructions
- After changing to the project directory, initialize virtual env using `uv init`
- Install dependencies using `uv add prometheus-client`

### Using existing `.lock` file
- Install dependencies using `uv sync`
- Activate environment `source .venv/bin/activate`

## `main.py`
- This script houses the base code to setup a `/metrics` endpoint
- Activate the environment using `source .venv/bin/activate`
- Run the script using `uv run main.py`
- In another terminal, type the following
```bash
% curl http://127.0.0.1:8000/metrics | grep "request_processing_seconds"
# HELP request_processing_seconds Time spent processing request
# TYPE request_processing_seconds summary
request_processing_seconds_count 259.0
request_processing_seconds_sum 130.79554020400974
# HELP request_processing_seconds_created Time spent processing request
# TYPE request_processing_seconds_created gauge
request_processing_seconds_created 1.776709245650259e+09
```
- These are the _metrics_ exposed by our _app_

## Prometheus
### Get your IP Address
- `ifconfig | grep "inet " | grep -v "127.0.0.1"`
- Use this when creating `prometheus.yml`

### Local Setup
- Create a local directory to store prometheus data `prometheus_data`
- Create a local configuration file `prometheus.yml`

### Install `brew`
- `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

### Install Docker
- `brew install docker`
- Also install and run Docker Desktop

### Docker Image
- Download image from docker
    ```bash
    docker pull prom/prometheus
    ```

### Start Prometheus
- Ensure current working directory is `example-prometheus-grafana`
```bash
docker run -p 9090:9090 \
    -v ./prometheus.yml:/etc/prometheus/prometheus.yml:ro \
    -v prometheus_data:/prometheus \
    prom/prometheus
```
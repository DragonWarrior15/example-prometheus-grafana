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

#!/usr/bin/env bash
set -euo pipefail

# Initialize conda in non-interactive shells and activate rag_env if present
if [ -f "/opt/conda/etc/profile.d/conda.sh" ]; then
  . /opt/conda/etc/profile.d/conda.sh
  if conda env list | awk '{print $1}' | grep -q "^rag_env$"; then
    conda activate rag_env
  else
    echo "Warning: conda environment 'rag_env' not found — continuing with base Python"
  fi
fi

START_MODE="${START_MODE:-streamlit}"
PORT="${PORT:-8501}"

if [ "$START_MODE" = "api" ]; then
  # Use uvicorn for the API. Default to port 80 when PORT not provided.
  PORT_VAL=${PORT:-80}
  echo "Starting API server on 0.0.0.0:$PORT_VAL"
  exec uvicorn src.api:app --host 0.0.0.0 --port "$PORT_VAL"
else
  # Start Streamlit. Streamlit uses environment variables for configuration.
  echo "Starting Streamlit app on 0.0.0.0:$PORT"
  export STREAMLIT_SERVER_PORT="$PORT"
  export STREAMLIT_SERVER_ADDRESS="0.0.0.0"
  # Avoid launching the browser
  export STREAMLIT_BROWSER_GATHER_USAGE_STATS="false"
  exec streamlit run app.py --server.port "$PORT" --server.address 0.0.0.0
fi

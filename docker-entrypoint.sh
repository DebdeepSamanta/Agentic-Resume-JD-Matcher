#!/bin/bash
set -e

echo "Starting FastAPI backend on :8000 ..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

echo "Starting Streamlit frontend on :8501 ..."
API_URL=http://localhost:8000 streamlit run frontend/app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true

wait

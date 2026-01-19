FROM python:3.10-slim

WORKDIR /app

# System deps (graphviz needs this)
RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Optional (Render ignores it, Docker users benefit)
EXPOSE 8504

# CRITICAL: use Render's dynamic PORT
CMD streamlit run app/ui_streamlit.py \
  --server.port=$PORT \
  --server.address=0.0.0.0

from fastapi import FastAPI
from metrics import setup_metrics

app = FastAPI(title="DevOps Demo App")

# Initialize Prometheus metrics
setup_metrics(app)

@app.get("/health")
def health():
    """Simple health check endpoint"""
    return {"status": "ok"}

@app.get("/hello")
def hello():
    """Demo endpoint"""
    return {"message": "Hello from DevOps app"}

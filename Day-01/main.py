from fastapi import FastAPI
from metrics import setup_metrics

app = FastAPI(title="DevOps Demo App")

# Initialize Prometheus metrics
setup_metrics(app)

@app.get("/health")
def health():
    """Simple health check endpoint"""
    # return {"status": "ok"}
    # To test out the readiness probe in kubernetes.
    return JSONResponse(status_code=500, content={"status": "fail"})

@app.get("/hello")
def hello():
    """Demo endpoint"""
    return {"message": "Hello from DevOps app"}

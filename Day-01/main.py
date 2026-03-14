import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from metrics import setup_metrics

app = FastAPI(title="DevOps Demo App")

setup_metrics(app)

health_ok = True

@app.get("/health")
def health():
    if health_ok:
        return {"status": "ok"}
    return JSONResponse(status_code=500, content={"status": "fail"})

@app.post("/fail")
def fail():
    global health_ok
    health_ok = False
    return {"message": "health check failing"}

@app.post("/recover")
def recover():
    global health_ok
    health_ok = True
    return {"message": "health restored"}

@app.get("/hello")
def hello():
    return {"message": "Hello from DevOps app"}

@app.post("/crash")
def crash():
    """Simulate container crash for liveness probe demo"""
    os._exit(1)  # Immediately kill the process

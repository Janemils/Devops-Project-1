from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Request latency in seconds"
)

def setup_metrics(app: FastAPI):
    """Middleware and /metrics endpoints for Prometheus + snapshot"""
    
    @app.middleware("http")
    async def metrics_middleware(request, call_next):
        start_time = time.time()
        response = await call_next(request)
        latency = time.time() - start_time

        # Increment counter with labels
        REQUEST_COUNT.labels(
            request.method,
            request.url.path,
            response.status_code
        ).inc()

        # Observe latency
        REQUEST_LATENCY.observe(latency)
        return response

    @app.get("/metrics")
    def metrics():
        """Prometheus-formatted metrics (full history)"""
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    @app.get("/metrics-snapshot")
    def metrics_snapshot():
        """Current snapshot of request counts (latest only)"""
        snapshot = {}
        for labels, metric in REQUEST_COUNT._metrics.items():
            snapshot[str(labels)] = metric._value.get()
        return snapshot

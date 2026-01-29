from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

# -------------------------------
# Prometheus Metrics Definitions
# -------------------------------

# Counter to track total number of HTTP requests.
# Labels allow counting by HTTP method, endpoint path, and status code.
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

# Histogram to track request latency (time taken to process requests)
# This allows monitoring response times and building latency dashboards.
REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Request latency in seconds"
)

def setup_metrics(app: FastAPI):
    """
    Attach Prometheus monitoring to a FastAPI app.
    
    This function does three things:
    1. Adds middleware to count requests and measure latency for every API call.
    2. Adds a '/metrics' endpoint that exposes Prometheus-formatted metrics (full history).
    3. Adds a '/metrics-snapshot' endpoint for quick inspection of current request counts only.
    """
    
    @app.middleware("http")
    async def metrics_middleware(request, call_next):
        """
        Middleware executed for every HTTP request.
        
        - Starts a timer before calling the endpoint.
        - Executes the actual endpoint function (call_next).
        - Measures request latency.
        - Updates Prometheus counters and histograms in memory.
        """
        
        start_time = time.time()
        response = await call_next(request)  # Call the actual endpoint.
        latency = time.time() - start_time

        # Increment the request counter with HTTP method, path, and status code.
        REQUEST_COUNT.labels(
            request.method,
            request.url.path,
            response.status_code
        ).inc()

        # Record the latency of this request in the histogram.
        REQUEST_LATENCY.observe(latency)
        return response

    @app.get("/metrics")
    def metrics():
        """
        Endpoint to expose Prometheus metrics.
        
        Returns all metrics (counters, histograms, etc.) in the Prometheus text format.
        Prometheus server can scrape this endpoint periodically.
        """
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    @app.get("/metrics-snapshot")
    def metrics_snapshot():
        """
        Endpoint to expose a quick snapshot of current request counts.
        
        Only returns the latest value for each counter, as a JSON object.
        Useful for debugging or lightweight inspection without full Prometheus formatting.
        """
        snapshot = {}
        for labels, metric in REQUEST_COUNT._metrics.items():
            snapshot[str(labels)] = metric._value.get()
        return snapshot

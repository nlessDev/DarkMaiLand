from prometheus_client import start_http_server, Counter, Gauge, Histogram

class Metrics:
    def __init__(self):
        self.requests = Counter('smtpx_requests', 'Total requests', ['method', 'status'])
        self.errors = Counter('smtpx_errors', 'Total errors', ['type'])
        self.active_connections = Gauge('smtpx_active_connections', 'Current connections')
        self.processing_time = Histogram('smtpx_processing_time', 'Request processing time')

metrics = Metrics()

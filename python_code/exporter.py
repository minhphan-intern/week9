from prometheus_client import start_http_server, Gauge, Histogram, Summary
import requests
import time
import os

class WebServerExporter:
    def __init__(self, web_server_ip, port, polling_interval_seconds=5):
        self.web_server_ip = web_server_ip
        self.port = port
        self.web_server_up = Gauge('web_server_up', 'Web server status (1 if UP, 0 if DOWN)')
        self.app_uptime = Gauge('app_uptime_seconds', 'Application uptime in seconds')
        self.total_uptime = Gauge('total_uptime_seconds', 'Total application uptime in seconds')
        self.polling_interval_seconds = polling_interval_seconds
        self.request_duration_histogram = Histogram('request_duration_seconds', 'Histogram of request durations', buckets=[0.1, 0.5, 1, 2, 5, 10])
        self.request_duration_summary = Summary('request_duration_summary_seconds', 'Summary of request durations')

    def check_web_server(self):
        url = f'{self.web_server_ip}'
        try:
            start_time = time.time()
            response = requests.get(url)
            duration = time.time() - start_time

            if response.ok:
                self.web_server_up.set(1)
                app_uptime_seconds = time.time() - self.start_time
                self.app_uptime.set(app_uptime_seconds)
                total_uptime_seconds = time.time() - self.exporter_start_time
                self.total_uptime.set(total_uptime_seconds)

                # Record request duration to Histogram and Summary
                self.request_duration_histogram.observe(duration)
                self.request_duration_summary.observe(duration)
            else:
                self.web_server_up.set(0)  
                self.total_uptime.set(0)
        except requests.ConnectionError:
            self.web_server_up.set(0) 
            self.total_uptime.set(0)

    def run(self):
        start_http_server(self.port)
        self.start_time = time.time()
        self.exporter_start_time = self.start_time
        while True:
            self.check_web_server()
            time.sleep(self.polling_interval_seconds)

if __name__ == '__main__':
    web_server_ip = os.getenv("APP_PORT", "http://192.168.56.10:8069/web/database/selector")
    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "5"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "8068"))
    exporter = WebServerExporter(web_server_ip, exporter_port, polling_interval_seconds)
    exporter.run()

#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 5000
HOST = "0.0.0.0"

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self.path = "/cover_guard.html"
        for h in ("If-Modified-Since", "If-None-Match", "If-Range"):
            if h in self.headers:
                del self.headers[h]
        return super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}", flush=True)

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

with ThreadedServer((HOST, PORT), Handler) as httpd:
    print(f"Serving on http://{HOST}:{PORT}", flush=True)
    httpd.serve_forever()

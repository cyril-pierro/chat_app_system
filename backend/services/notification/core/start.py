from wsgiref.simple_server import make_server

from prometheus_client import make_wsgi_app


def start_metrics():
    app = make_wsgi_app()
    httpd = make_server("", 8082, app)
    httpd.serve_forever()

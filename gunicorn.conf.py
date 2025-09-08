# Gunicorn configuration file
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 2
worker_connections = 1000
timeout = 30
keepalive = 2

# Process naming
proc_name = "fbc_library"

# Logging
errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = os.getenv("SSL_PRIVATE_KEY_PATH")
certfile = os.getenv("SSL_CERTIFICATE_PATH")
ssl_version = "TLS"
ciphers = "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256"
do_handshake_on_connect = True

# Process management
reload = os.getenv("DEBUG", "False") == "True"
reload_engine = "auto"
reload_extra_files = []

# App loading
preload_app = True


# Hook points
def on_starting(server):
    pass


def on_reload(server):
    pass


def when_ready(server):
    pass


def on_exit(server):
    pass

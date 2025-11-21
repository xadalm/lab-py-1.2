import logging
from datetime import datetime

logging.basicConfig(
    filename='shell.log',
    level=logging.INFO,
    format='%(message)s',
    encoding='utf-8'
)

def log(cmd, ok=True, error=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if ok:
        logging.info(f"[{timestamp}] {cmd}")
    else:
        logging.info(f"[{timestamp}] ERROR: {error}")
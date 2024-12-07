# app/core/logger.py

import logging
from fastapi import FastAPI

# Global logger oluşturun
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)

# StreamHandler ekle (logları terminale yazdırır)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

# Eğer logger zaten handler içeriyorsa, tekrar eklemeyin
if not logger.handlers:
    logger.addHandler(handler)

def setup_logger(app: FastAPI):
    # FastAPI uygulamasının logger'ını yapılandırın
    app.logger = logger
    logger.info("Logger ayarlandı.")

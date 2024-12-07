# app/core/logger.py

import logging
from fastapi import FastAPI

def setup_logger(app: FastAPI):
    # Uvicorn'un error logger'ını al
    logger = logging.getLogger("uvicorn.error")
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

    # Uygulama seviyesinde logger'ı ayarla
    app.logger = logger

    # FastAPI'nin kendi logger'ını da ayarlayın
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

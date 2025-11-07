import time
import logging
from fastapi import Request

# Configure le logger pour écrire dans stdout
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("api-logger")

async def access_log_middleware(request: Request, call_next):
    """
    Middleware pour journaliser chaque requête HTTP.
    Affiche :
      - Méthode (GET/POST/…)
      - Chemin (/clients, /clients/{id}, etc.)
      - Code HTTP
      - Durée en ms
      - Et si erreur → message d'erreur dans le log
    """
    start_time = time.time()
    status_code = 500
    reason = "-"

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response

    except Exception as e:
        # Si une exception remonte, on log son message
        reason = str(e)
        raise

    finally:
        elapsed_ms = (time.time() - start_time) * 1000
        logger.info(
            f"{request.method} {request.url.path} → {status_code} "
            f"({elapsed_ms:.2f} ms){' – ' + reason if reason != '-' else ''}"
        )
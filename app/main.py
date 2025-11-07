from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.errors import NotFoundError,ConflictError
from app.core.logging import access_log_middleware
from app.api.v1.endpoints.clients import router as clients_router

app = FastAPI(title="Clients & Orders")
app.include_router(clients_router)

#  Ajout du middleware global
app.middleware("http")(access_log_middleware)

# ✅ Enregistrement des routes
app.include_router(clients_router)

@app.exception_handler(NotFoundError)
async def handle_not_found(_: Request, exc: NotFoundError):
    return JSONResponse(status_code= 404, content={"detail": exc.detail})

@app.exception_handler(ConflictError)
async def handle_conflict_error(_: Request, exc: ConflictError):
    return JSONResponse(status_code= 409, content={"detail": exc.detail})

@app.exception_handler(RequestValidationError)
async def handle_validation_error(_: Request, exc: RequestValidationError):
    errors = exc.errors()
    messages = [err["msg"] for err in errors]
    return JSONResponse(status_code= 422, content={"detail": "; ".join(messages)})
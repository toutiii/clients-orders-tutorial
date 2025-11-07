from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.data.db import SessionLocal
from app.shemas.clients import ClientCreate, ClientRead, ClientUpdate
from app.service.clients import (create_client, get_client, list_clients, update_client, delete_client)

router = APIRouter(prefix="/clients", tags=["clients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST /clients -> 201 + ClientRead
@router.post("", response_model=ClientRead, status_code=201)
def create_client_route(payload: ClientCreate, db: Session = Depends(get_db)):
    # Lève ConflictError en cas d'email en doublon -> mappé globalement en 409
    return create_client(db, payload)

# GET /clients -> 200 + list[ClientRead]
@router.get("", response_model=list[ClientRead])
def list_clients_route(db: Session = Depends(get_db)):
    return list_clients(db)

# GET /clients/{id} -> 200 ou 404 (mappé globalement)
@router.get("/{client_id}", response_model=ClientRead)
def get_client_route(client_id: int, db: Session = Depends(get_db)):
    return get_client(db, client_id)

# PATCH /clients/{id} -> 200 ; 404/409 mappés globalement
@router.patch("/{client_id}", response_model=ClientRead)
def update_client_route(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db)):
    return update_client(db, client_id, payload)

# DELETE /clients/{id} -> 204 ; 404 mappé globalement
@router.delete("/{client_id}", status_code=204)
def delete_client_route(client_id: int, db: Session = Depends(get_db)):
    delete_client(db, client_id)
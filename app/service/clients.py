from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.data.models.clients import Clients
from app.core.errors import ConflictError, NotFoundError
from app.shemas.clients import ClientCreate, ClientUpdate

# Create client in database
def create_client(session: Session, data: ClientCreate) -> Clients:
    normalized_email = data.email.strip().lower()
    client = Clients(name= data.name.strip(), email= normalized_email)
    session.add(client)

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise ConflictError("email already exist") from e
    
    session.refresh(client)
    return client

def get_client(session: Session, client_id: int) -> Clients:
    client = session.get(Clients, client_id)
    if not client:
        raise NotFoundError("client not found")
    return client

def list_clients(session: Session) -> list[Clients]:
    result = session.execute(select(Clients).order_by(Clients.id))
    return list(result.scalars())

def update_client(session:Session, client_id: int, data: ClientUpdate) -> Clients:
    client = session.get(Clients, client_id)
    if not client:
        raise NotFoundError("client not found")
    if data.name is not None:
        client.name = data.name.strip()
    if data.email is not None:
        client.email = data.email.strip().lower()
    
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise ConflictError("email already exists") from e
    
    session.refresh(client)
    return client

def delete_client(session: Session, client_id: int) -> None:
    client = session.get(Clients, client_id)
    if not client:
        raise NotFoundError("client not found")
    
    session.delete(client)
    session.commit()
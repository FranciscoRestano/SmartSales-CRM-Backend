import uvicorn
import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base, relationship
from pydantic import BaseModel

# --- 1. CONFIGURACION ---
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("ERROR: No se encontro DATABASE_URL en .env")

# --- 2. BASE DE DATOS ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 3. MODELOS SQL (RELACIONALES) ---
# Alembic leera esto para crear las tablas

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    empresa = Column(String, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    # Relacion: Un cliente tiene muchas ventas
    ventas = relationship("Venta", back_populates="cliente")

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id")) # Clave Foranea
    producto = Column(String)
    monto = Column(Float)
    fecha = Column(DateTime, default=datetime.utcnow)

    # Relacion: Una venta pertenece a un cliente
    cliente = relationship("Cliente", back_populates="ventas")

# NOTA: Eliminamos 'Base.metadata.create_all(bind=engine)' para que Alembic tenga el control total.

# --- 4. SCHEMAS PYDANTIC ---

class ClienteCreate(BaseModel):
    nombre: str
    email: str
    empresa: Optional[str] = None

class ClienteResponse(ClienteCreate):
    id: int
    fecha_registro: datetime
    class Config:
        from_attributes = True

class VentaCreate(BaseModel):
    cliente_id: int
    producto: str
    monto: float

class VentaResponse(VentaCreate):
    id: int
    fecha: datetime
    class Config:
        from_attributes = True

# --- 5. API ENDPOINTS ---
app = FastAPI(title="SmartSales CRM - Pro Version")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"sistema": "CRM Relacional", "estado": "Activo"}

# CLIENTES
@app.post("/clientes/", response_model=ClienteResponse)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.email == cliente.email).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")
    
    nuevo_cliente = Cliente(
        nombre=cliente.nombre, 
        email=cliente.email, 
        empresa=cliente.empresa
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

@app.get("/clientes/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

# VENTAS
@app.post("/ventas/", response_model=VentaResponse)
def crear_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    # Validamos que el cliente exista
    cliente = db.query(Cliente).filter(Cliente.id == venta.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    nueva_venta = Venta(
        cliente_id=venta.cliente_id,
        producto=venta.producto,
        monto=venta.monto
    )
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)
    return nueva_venta

@app.get("/ventas/", response_model=List[VentaResponse])
def listar_ventas(db: Session = Depends(get_db)):
    return db.query(Venta).all()

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
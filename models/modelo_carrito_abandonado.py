from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

class ProductoEnCarrito(BaseModel):
    id: str
    nombre: str
    cantidad: int

class CarritoAbandonado(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    username: str
    email: EmailStr
    nombre: str
    numero_telefono: str
    descripcion: List[ProductoEnCarrito]
    total: float
    direccion_entrega: Optional[str] = None
    tienda: str  # 🆕 Tienda asociada
    fecha_ingreso: datetime = Field(default_factory=datetime.utcnow)

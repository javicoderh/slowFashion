from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductoDetalle(BaseModel):
    nombre: str
    precio_unitario: float
    cantidad: int

class Factura(BaseModel):
    fecha_ingreso: datetime
    total: float
    productos: List[ProductoDetalle]
    username: str
    telefono: str
    email: str
    tienda: str

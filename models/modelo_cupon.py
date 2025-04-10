from pydantic import BaseModel
from typing import Optional

class Cupon(BaseModel):
    nombre: str
    multiplicador: float  # ej: 0.8 = 20% descuento
    codigo: str
    veces_usado: int = 0
    activo: bool
    limite_uso: Optional[int] = None  # opcional

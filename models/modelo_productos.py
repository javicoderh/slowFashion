from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Producto(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: str
    precio: float
    moneda: str = "CLP"
    stock: int
    categoria: str
    etiquetas: Optional[List[str]] = []
    imagen_portada_url: Optional[str] = None
    imagenes_url: List[str] = []
    creado_en: datetime = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)
    activo: bool = True
    veces_visto: int = 0
    veces_comprado: int = 0
    calificacion_promedio: Optional[float] = None
    cantidad_resenas: int = 0
    tienda: str
    autor: Optional[str] = None
    preferencia: int = 0  # 🆕 Prioridad manual del admin para orden

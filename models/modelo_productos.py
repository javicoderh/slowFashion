from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Producto(BaseModel):
    id: Optional[str] = None  # Firestore generará este ID
    nombre: str
    descripcion: str
    precio: float  # Precio en CLP
    moneda: str = "CLP"  # Moneda actualizada (por defecto CLP)
    stock: int
    categoria: str
    etiquetas: Optional[List[str]] = []
    imagen_portada_url: Optional[str] = None  # ✅ Imagen principal
    imagenes_url: List[str] = []              # ✅ Galería adicional
    creado_en: datetime = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)
    activo: bool = True
    veces_visto: int = 0
    veces_comprado: int = 0
    calificacion_promedio: Optional[float] = None
    cantidad_resenas: int = 0
    tienda: str
    autor: Optional[str] = None

# models/articulo.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Articulo(BaseModel):
    id: str
    titulo: str
    bajada: str
    contenido: str
    imagen_destacada: Optional[str] = None
    fecha_publicacion: Optional[date] = None
    autor: Optional[str] = "Slow Fashion Collective"
    etiquetas: Optional[List[str]] = []

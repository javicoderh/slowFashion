from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Producto(BaseModel):
    id: Optional[str] = None  # Firestore generará este ID
    nombre: str  # Nombre del producto
    descripcion: str  # Descripción del producto
    precio: float  # Precio del producto
    moneda: str = "USD"  # Moneda (por defecto: USD)
    stock: int  # Cantidad disponible en inventario
    categoria: str  # Categoría del producto (ej: "bolsos", "calzado")
    etiquetas: Optional[List[str]] = []  # Etiquetas para clasificación adicional
    imagen_url: Optional[str] = None  # URL de la imagen del producto
    creado_en: datetime = Field(default_factory=datetime.utcnow)  # Fecha de creación del producto
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)  # Última actualización del producto
    activo: bool = True  # Si el producto está disponible o no
    veces_visto: int = 0  # Número de veces que se ha consultado el producto
    veces_comprado: int = 0  # Número de veces que se ha comprado el producto
    calificacion_promedio: Optional[float] = None  # Calificación promedio del producto (opcional)
    cantidad_resenas: int = 0  # Número de reseñas del producto
    tienda: str  # Tienda o marca que vende el producto
    autor: Optional[str] = None  # Diseñador/autor del producto (opcional)

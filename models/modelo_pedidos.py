from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List, Optional, Literal
from uuid import uuid4

class ProductoEnPedido(BaseModel):
    id_producto: str
    nombre: str
    cantidad: int

class Pedido_tabla_pedidos(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    username: str
    nombre: str
    numero_telefono: str
    descripcion: List[ProductoEnPedido]
    total: float  # 💰 Total del pedido
    fecha_ingreso: datetime = Field(default_factory=datetime.utcnow)
    estado: Literal["pendiente", "enviado", "entregado"] = "pendiente"
    direccion_entrega: str
    fecha_estimada_entrega: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=72))
    responsable: Optional[str] = None  # username del delivery asignado

import re
from pydantic import BaseModel, EmailStr, Field 
from typing import Optional, List
from datetime import datetime

# Modelo de un pedido dentro del usuario
class Pedido(BaseModel):
    id_pedido: str
    total: float
    fecha: datetime = Field(default_factory=datetime.utcnow)
    estado: str  # "pendiente", "enviado", "entregado"
    direccion_entrega: str
    fecha_entrega: Optional[datetime] = None
    descripcion: Optional[str] = None

# Para el cambio de contraseña del usuario
class CambioContrasenaRequest(BaseModel):
    username: str
    contrasena_actual: str
    nueva_contrasena: str

# Modelo de un usuario
class Usuario(BaseModel):
    id: Optional[str] = None
    nombre: str
    username: str
    email: EmailStr
    telefono: str
    edad: Optional[int] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    genero: Optional[str] = None
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)
    tipo_usuario: str  # cliente, admin, etc.
    activo: bool = True
    pedidos: List[Pedido] = []  # Lista de pedidos (puedes usar List en lugar de list para Pydantic 1.x o 2.x)
    token: str
    last_login: datetime = Field(default_factory=datetime.utcnow)
    desea_catalogo: bool = False  # 🆕 Preferencia para recibir catálogo

# Modelo de login
class LoginRequest(BaseModel):
    username: str
    token: str

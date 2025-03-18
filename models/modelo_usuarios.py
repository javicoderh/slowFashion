import re
from pydantic import BaseModel, EmailStr 
from typing import Optional, List
from datetime import datetime

class Pedido(BaseModel):
    id_pedido: str
    total: float
    fecha: datetime
    estado: str  # "pendiente", "enviado", "entregado"
    direccion_entrega: str
    fecha_entrega: Optional[datetime] = None
    descripcion: Optional[str] = None

class CambioContrasenaRequest(BaseModel):
    nombre_usuario: str
    contrasena_actual: str
    nueva_contrasena: str

class Usuario(BaseModel):
    id: Optional[str] = None  # ID del usuario en Firestore (opcional)
    nombre: str  # Nombre personal
    username: str  # Nombre de usuario (sin validación en el backend)
    email: EmailStr  # Email
    telefono: str  # Teléfono
    edad: Optional[int] = None  # Edad
    ciudad: Optional[str] = None  # Ciudad
    pais: Optional[str] = None  # País
    genero: Optional[str] = None  # Género
    fecha_registro: datetime = datetime.utcnow()  # Fecha de registro
    tipo_usuario: str  # Tipo de usuario (cliente, admin, etc.)
    activo: bool = True  # Si el usuario está activo o no
    pedidos: List = []  # Lista de pedidos (vacío por defecto)
    token: str  # Contraseña (token)
    last_login: datetime = datetime.utcnow()  # Último login

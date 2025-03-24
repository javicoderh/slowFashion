from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class Admin(BaseModel):
    id: Optional[str] = None  # Hacer el id opcional
    nombre: str
    email: EmailStr
    telefono: str  # 📌 Nuevo campo obligatorio
    tipo: str  # "admin_tienda" o "admin_plataforma"
    activo: bool = True
    fecha_registro: datetime = datetime.utcnow()
    tienda_a_cargo: str  # 📌 Tienda asignada, si es un admin de tienda
    token: str  # 📌 Token de autenticación
    username: str

class CambioContrasenaAdminRequest(BaseModel):
    username: str
    contrasena_actual: str
    nueva_contrasena: str
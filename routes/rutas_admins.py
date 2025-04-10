from fastapi import APIRouter
from models.modelo_admins import Admin, CambioContrasenaAdminRequest
from services.admins import obtener_admins, crear_admin, eliminar_admin, cambiar_contrasena_admin

router = APIRouter(prefix="/admins", tags=["Admins"])

@router.get("/")
def get_admins():
    return obtener_admins()

@router.post("/")
def post_admin(admin: Admin):
    return crear_admin(admin)

@router.delete("/{id}")
def delete_admin(id: str):
    return eliminar_admin(id)

@router.patch("/cambiar-contrasena")
async def cambiar_contrasena_admin_route(cambio: CambioContrasenaAdminRequest):
    return cambiar_contrasena_admin(cambio.nombre_usuario, cambio.contrasena_actual, cambio.nueva_contrasena)

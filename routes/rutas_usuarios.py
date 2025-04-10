from fastapi import APIRouter
from models.modelo_usuarios import Usuario, Pedido, CambioContrasenaRequest
from services.usuarios import (
    obtener_usuarios,
    crear_usuario,
    agregar_pedido,
    eliminar_usuario,
    eliminar_pedido,
    cambiar_contrasena
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/")
def get_usuarios():
    return obtener_usuarios()

@router.post("/")
def post_usuario(usuario: Usuario):
    return crear_usuario(usuario)

@router.post("/{id}/pedidos")
def post_pedido(id: str, pedido: Pedido):
    return agregar_pedido(id, pedido)

@router.delete("/{id}")
def delete_usuario(id: str):
    return eliminar_usuario(id)

@router.delete("/{id_usuario}/pedidos/{id_pedido}")
def delete_pedido(id_usuario: str, id_pedido: str):
    return eliminar_pedido(id_usuario, id_pedido)

@router.patch("/cambiar-contrasena")
def patch_cambiar_contrasena(request: CambioContrasenaRequest):
    return cambiar_contrasena(request.nombre_usuario, request.contrasena_actual, request.nueva_contrasena)

@router.patch("/{id}/actualizar_catalogo")
def patch_catalogo(id: str, desea_catalogo: bool):
    return actualizar_catalogo_usuario(id, desea_catalogo)


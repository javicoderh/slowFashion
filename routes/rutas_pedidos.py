from fastapi import APIRouter, Path, Body
from models.modelo_pedidos import Pedido_tabla_pedidos
from services.pedidos import (
    crear_pedido_tabla_pedidos,
    obtener_pedidos_tabla_pedidos,
    obtener_pedido_por_id_tabla_pedidos,
    actualizar_estado_pedido_tabla_pedidos,
    actualizar_pedido_tabla_pedidos,
    eliminar_pedido_tabla_pedidos
)

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/")
def crear_pedido(pedido: Pedido_tabla_pedidos):
    return crear_pedido_tabla_pedidos(pedido)

@router.get("/")
def obtener_pedidos():
    return obtener_pedidos_tabla_pedidos()

@router.get("/{pedido_id}")
def obtener_pedido_por_id(pedido_id: str = Path(..., title="ID del pedido")):
    return obtener_pedido_por_id_tabla_pedidos(pedido_id)

@router.patch("/{pedido_id}/estado")
def actualizar_estado_pedido(
    pedido_id: str = Path(..., title="ID del pedido"),
    nuevo_estado: str = Body(..., embed=True, title="Nuevo estado")
):
    return actualizar_estado_pedido_tabla_pedidos(pedido_id, nuevo_estado)

@router.put("/{pedido_id}")
def actualizar_pedido(pedido_id: str, pedido: Pedido_tabla_pedidos):
    return actualizar_pedido_tabla_pedidos(pedido_id, pedido)

@router.delete("/{pedido_id}")
def eliminar_pedido(pedido_id: str):
    return eliminar_pedido_tabla_pedidos(pedido_id)

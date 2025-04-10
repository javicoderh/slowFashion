from fastapi import APIRouter, Path
from models.modelo_productos import Producto
from services.productos import (
    crear_producto,
    obtener_productos,
    obtener_producto_por_nombre,
    actualizar_producto,
    modificar_producto,
    eliminar_producto,
    aumentar_veces_comprado
)
from typing import Dict

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/")
def crear_producto_route(producto: Producto):
    return crear_producto(producto)

@router.get("/")
def obtener_productos_route():
    return obtener_productos()

@router.get("/{nombre}")
def obtener_producto_por_nombre_route(nombre: str = Path(..., title="Nombre del producto")):
    return obtener_producto_por_nombre(nombre)

@router.put("/{id}")
def actualizar_producto_route(id: str, producto: Producto):
    return actualizar_producto(id, producto)

@router.patch("/{id}")
def modificar_producto_route(id: str, cambios: Dict[str, str]):
    return modificar_producto(id, cambios)

@router.delete("/{id}")
def eliminar_producto_route(id: str):
    return eliminar_producto(id)

@router.patch("/{id}/veces_comprado")
def patch_veces_comprado(id: str, cantidad: int):
    return aumentar_veces_comprado(id, cantidad)
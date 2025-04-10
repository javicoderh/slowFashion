from fastapi import APIRouter
from models.modelo_cupon import Cupon
from services.cupones import (
    crear_cupon,
    obtener_cupon,
    actualizar_cupon,
    obtener_todos_cupones
)

router = APIRouter(prefix="/cupones", tags=["Cupones"])

@router.post("/")
def crear_cupon_route(cupon: Cupon):
    return crear_cupon(cupon)

@router.get("/{nombre}")
def obtener_cupon_route(nombre: str):
    return obtener_cupon(nombre)

@router.patch("/{nombre}")
def actualizar_cupon_route(nombre: str, cambios: dict):
    return actualizar_cupon(nombre, cambios)

@router.get("/")
def obtener_todos_cupones_route():
    return obtener_todos_cupones()

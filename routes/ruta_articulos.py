# rutas/articulos_routes.py
from fastapi import APIRouter, HTTPException
from models.modelo_articulos import Articulo
from services.articulos import (
    crear_articulo,
    obtener_articulos,
    obtener_articulo_por_id,
    actualizar_articulo,
    eliminar_articulo
)

router = APIRouter(prefix="/articulos", tags=["Articulos"])

@router.post("/")
def crear(data: Articulo):
    return crear_articulo(data)

@router.get("/")
def listar():
    return obtener_articulos()

@router.get("/{id}")
def obtener(id: str):
    articulo = obtener_articulo_por_id(id)
    if not articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return articulo

@router.patch("/{id}")
def actualizar(id: str, data: dict):
    return actualizar_articulo(id, data)

@router.delete("/{id}")
def eliminar(id: str):
    return eliminar_articulo(id)

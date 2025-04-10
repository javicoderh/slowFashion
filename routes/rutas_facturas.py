from fastapi import APIRouter
from models.modeloFactura import Factura
from services.facturas import (
    crear_factura,
    obtener_facturas,
    eliminar_factura,
    actualizar_factura,
    obtener_facturas_por_usuario,
    obtener_facturas_por_fecha
)
from datetime import datetime

router = APIRouter(prefix="/facturas", tags=["Facturas"])

@router.post("/")
def crear_factura_route(factura: Factura):
    return crear_factura(factura)

@router.get("/")
def obtener_facturas_route():
    return obtener_facturas()

@router.delete("/{factura_id}")
def eliminar_factura_route(factura_id: str):
    return eliminar_factura(factura_id)

@router.patch("/{factura_id}")
def actualizar_factura_route(factura_id: str, cambios: dict):
    return actualizar_factura(factura_id, cambios)

@router.get("/usuario/{username}")
def obtener_facturas_usuario_route(username: str):
    return obtener_facturas_por_usuario(username)

@router.get("/fechas")
def obtener_facturas_fecha_route(fecha_inicio: str, fecha_fin: str):
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        return obtener_facturas_por_fecha(inicio, fin)
    except ValueError:
        return {"error": "Formato de fecha incorrecto. Usa YYYY-MM-DD"}

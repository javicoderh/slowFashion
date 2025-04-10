from fastapi import APIRouter
from models.modelo_carrito_abandonado import CarritoAbandonado
from services.carrito_abandonado import guardar_carrito_abandonado

router = APIRouter(prefix="/carritos-abandonados", tags=["Carritos Abandonados"])

@router.post("/")
def post_carrito_abandonado(carrito: CarritoAbandonado):
    return guardar_carrito_abandonado(carrito)

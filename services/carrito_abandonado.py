from firebase_config import db
from models.modelo_carrito_abandonado import CarritoAbandonado
from fastapi import HTTPException
from datetime import datetime

def guardar_carrito_abandonado(carrito: CarritoAbandonado):
    try:
        nuevo_carrito = carrito.dict()
        nuevo_carrito["fecha_ingreso"] = datetime.utcnow()

        doc_ref = db.collection("carritos_abandonados").add(nuevo_carrito)
        carrito_id = doc_ref[1].id

        db.collection("carritos_abandonados").document(carrito_id).update({"id": carrito_id})
        return {"message": "Carrito abandonado guardado correctamente", "id": carrito_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

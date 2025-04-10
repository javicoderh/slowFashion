from firebase_config import db
from fastapi import HTTPException
from models.modelo_cupon import Cupon

# Crear cupón
def crear_cupon(cupon: Cupon):
    try:
        db.collection("cupones").document(cupon.nombre).set(cupon.dict())
        return {"message": "Cupón creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener cupón por nombre
def obtener_cupon(nombre: str):
    try:
        doc = db.collection("cupones").document(nombre).get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Cupón no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Actualizar cupón
def actualizar_cupon(nombre: str, cambios: dict):
    try:
        db.collection("cupones").document(nombre).update(cambios)
        return {"message": "Cupón actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener todos los cupones
def obtener_todos_cupones():
    try:
        cupones = db.collection("cupones").stream()
        return [ { "nombre": doc.id, **doc.to_dict() } for doc in cupones ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

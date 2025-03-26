from firebase_config import db
from models.modelo_pedidos import Pedido_tabla_pedidos
from fastapi import HTTPException
from datetime import datetime, timedelta
from typing import Optional, List

# 📌 Crear pedido
def crear_pedido_tabla_pedidos(pedido: Pedido):
    try:
        nuevo_pedido = pedido.dict()
        nuevo_pedido["fecha_ingreso"] = datetime.utcnow()
        nuevo_pedido["fecha_estimada_entrega"] = datetime.utcnow() + timedelta(hours=72)

        doc_ref = db.collection("pedidos").add(nuevo_pedido)
        pedido_id = doc_ref[1].id

        db.collection("pedidos").document(pedido_id).update({"id": pedido_id})
        return {"message": "Pedido creado correctamente", "id": pedido_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📌 Obtener todos los pedidos
def obtener_pedidos_tabla_pedidos():
    try:
        pedidos_ref = db.collection("pedidos").stream()
        pedidos = [{"id": doc.id, **doc.to_dict()} for doc in pedidos_ref]
        return {"pedidos": pedidos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📌 Obtener un pedido por ID
def obtener_pedido_por_id_tabla_pedidos(pedido_id: str):
    try:
        pedido_ref = db.collection("pedidos").document(pedido_id).get()
        if not pedido_ref.exists:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return pedido_ref.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📌 Actualizar estado del pedido (PATCH)
def actualizar_estado_pedido_tabla_pedidos(pedido_id: str, nuevo_estado: str):
    try:
        pedido_ref = db.collection("pedidos").document(pedido_id)

        if not pedido_ref.get().exists:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        if nuevo_estado not in ["pendiente", "enviado", "entregado"]:
            raise HTTPException(status_code=400, detail="Estado inválido")

        pedido_ref.update({
            "estado": nuevo_estado,
            "actualizado_en": datetime.utcnow()
        })

        return {"message": "Estado del pedido actualizado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📌 Editar pedido completo (PUT)
def actualizar_pedido_tabla_pedidos(pedido_id: str, pedido: Pedido):
    try:
        pedido_ref = db.collection("pedidos").document(pedido_id)

        if not pedido_ref.get().exists:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        pedido_dict = pedido.dict()
        pedido_dict["actualizado_en"] = datetime.utcnow()

        pedido_ref.set(pedido_dict, merge=True)
        return {"message": "Pedido actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📌 Eliminar un pedido
def eliminar_pedido_tabla_pedidos(pedido_id: str):
    try:
        pedido_ref = db.collection("pedidos").document(pedido_id)

        if not pedido_ref.get().exists:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        pedido_ref.delete()
        return {"message": "Pedido eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

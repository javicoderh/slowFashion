from firebase_config import db
from models.modelo_productos import Producto
from fastapi import HTTPException
from datetime import datetime
from typing import Optional

# 📌 Crear producto
def crear_producto(producto: Producto):
    try:
        nuevo_producto = producto.dict()
        nuevo_producto["creado_en"] = datetime.utcnow()
        nuevo_producto["actualizado_en"] = datetime.utcnow()

        # 🔒 Forzar la moneda a CLP siempre
        nuevo_producto["moneda"] = "CLP"

        # 🔥 Agregar producto a Firestore
        doc_ref = db.collection("productos").add(nuevo_producto)
        producto_id = doc_ref[1].id

        # 🔥 Guardar el ID dentro del propio documento
        db.collection("productos").document(producto_id).update({"id": producto_id})

        return {"message": "Producto agregado correctamente", "id": producto_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📌 Obtener todos los productos
def obtener_productos():
    try:
        productos_ref = db.collection("productos").stream()
        productos = [{"id": doc.id, **doc.to_dict()} for doc in productos_ref]
        return {"productos": productos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 📌 Obtener un producto por nombre
def obtener_producto_por_nombre(nombre: str):
    try:
        productos_ref = db.collection("productos").where("nombre", "==", nombre).stream()
        productos = [doc.to_dict() for doc in productos_ref]

        if not productos:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        return productos[0]  # Devuelve el primer producto encontrado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 📌 Actualizar un producto completo (PUT)
def actualizar_producto(id: str, producto: Producto):
    try:
        producto_ref = db.collection("productos").document(id)

        if not producto_ref.get().exists:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        producto_dict = producto.dict()
        producto_dict["actualizado_en"] = datetime.utcnow()

        producto_ref.set(producto_dict, merge=True)
        return {"message": "Producto actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 📌 Modificar solo campos específicos (PATCH)
def modificar_producto(id: str, cambios: dict):
    try:
        producto_ref = db.collection("productos").document(id)

        if not producto_ref.get().exists:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        cambios["actualizado_en"] = datetime.utcnow()  # Registrar la fecha de actualización

        producto_ref.update(cambios)
        return {"message": "Producto modificado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 📌 Eliminar un producto
def eliminar_producto(id: str):
    try:
        producto_ref = db.collection("productos").document(id)

        if not producto_ref.get().exists:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        producto_ref.delete()
        return {"message": "Producto eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# servicios/articulos_service.py
from firebase_admin import firestore
from models.modelo_articulos import Articulo

db = firestore.client()
collection = db.collection('articulos')

def crear_articulo(data: Articulo):
    articulo_dict = data.dict()
    
    # 🔁 convertir fecha a string ISO si existe
    if articulo_dict.get("fecha_publicacion"):
        articulo_dict["fecha_publicacion"] = articulo_dict["fecha_publicacion"].isoformat()

    doc_ref = collection.document(data.id)
    doc_ref.set(articulo_dict)
    return {"mensaje": "Artículo creado exitosamente."}

def obtener_articulos():
    docs = collection.stream()
    return [doc.to_dict() for doc in docs]

def obtener_articulo_por_id(id: str):
    doc = collection.document(id).get()
    if doc.exists:
        return doc.to_dict()
    return None

def actualizar_articulo(id: str, data: dict):
    collection.document(id).update(data)
    return {"mensaje": "Artículo actualizado."}

def eliminar_articulo(id: str):
    collection.document(id).delete()
    return {"mensaje": "Artículo eliminado."}

from firebase_admin import firestore
from models.modeloFactura import Factura
from datetime import datetime, timedelta

db = firestore.client()

# Crear una factura
def crear_factura(data: Factura):
    data_dict = data.dict()
    data_dict["fecha_ingreso"] = datetime.utcnow()
    db.collection("facturas").add(data_dict)
    return {"message": "Factura creada con éxito"}

# Obtener todas las facturas
def obtener_facturas():
    facturas = db.collection("facturas").stream()
    return [f.to_dict() for f in facturas]

# Eliminar una factura por ID
def eliminar_factura(factura_id: str):
    db.collection("facturas").document(factura_id).delete()
    return {"message": "Factura eliminada"}

# Actualizar una factura por ID
def actualizar_factura(factura_id: str, cambios: dict):
    db.collection("facturas").document(factura_id).update(cambios)
    return {"message": "Factura actualizada"}

# Obtener facturas por nombre de usuario
def obtener_facturas_por_usuario(username: str):
    facturas = db.collection("facturas")\
        .where("username", "==", username)\
        .stream()
    return [f.to_dict() for f in facturas]

# Obtener facturas por rango de fecha (día, semana, etc.)
def obtener_facturas_por_fecha(fecha_inicio: datetime, fecha_fin: datetime):
    facturas = db.collection("facturas")\
        .where("fecha_ingreso", ">=", fecha_inicio)\
        .where("fecha_ingreso", "<", fecha_fin)\
        .stream()
    return [f.to_dict() for f in facturas]

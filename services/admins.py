from firebase_config import db
from models.modelo_admins import Admin
from datetime import datetime
from fastapi import HTTPException
import secrets  # 📌 Para generar el token de seguridad
import bcrypt

def hash_password(password: str) -> str:
    """Hashea la contraseña antes de guardarla en la base de datos"""
    salt = bcrypt.gensalt()  # Genera un salt único
    hashed_password = bcrypt.hashpw(password.encode(), salt)  # Hashea la contraseña con el salt
    return hashed_password.decode()  # Devolvemos el hash como string

def obtener_admins():
    try:
        admins_ref = db.collection("admins").stream()
        admins = [{"id": doc.id, **doc.to_dict()} for doc in admins_ref]
        return {"admins": admins}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def crear_admin(admin: Admin):
    try:
        nuevo_admin = admin.dict()
        nuevo_admin["last_login"] = datetime.utcnow()

        # Hashear la contraseña antes de guardarla
        nuevo_admin["token"] = hash_password(admin.token)

        # Agregar admin a Firestore y obtener el ID generado
        doc_ref = db.collection("admins").add(nuevo_admin)
        admin_id = doc_ref[1].id

        # Guardar el ID dentro del propio documento
        db.collection("admins").document(admin_id).update({"id": admin_id})

        return {"message": "Admin agregado correctamente", "id": admin_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def eliminar_admin(id: str):
    try:
        admin_ref = db.collection("admins").document(id)
        if admin_ref.get().exists:
            admin_ref.delete()
            return {"message": f"Admin con ID {id} eliminado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Admin no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def verificar_password(password: str, hashed_password: str) -> bool:
    """Compara la contraseña ingresada con el hash almacenado en la base de datos"""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def cambiar_contrasena_admin(nombre_usuario: str, contrasena_actual: str, nueva_contrasena: str):
    try:
        # Buscar admin por nombre en Firestore
        admins_ref = db.collection("admins").where("nombre", "==", nombre_usuario).stream()
        admins = [doc for doc in admins_ref]

        if not admins:
            raise HTTPException(status_code=404, detail="Admin no encontrado")

        if len(admins) > 1:
            raise HTTPException(status_code=400, detail="Nombre de admin duplicado, contacta soporte")

        admin_ref = admins[0].reference
        admin_data = admins[0].to_dict()

        # Verificar si la contraseña actual ingresada coincide con el hash almacenado
        if not verificar_password(contrasena_actual, admin_data["token"]):
            raise HTTPException(status_code=403, detail="Contraseña actual incorrecta")

        # Hashear la nueva contraseña antes de almacenarla
        nueva_contrasena_hashed = bcrypt.hashpw(nueva_contrasena.encode(), bcrypt.gensalt()).decode()

        # Actualizar la contraseña en la base de datos
        admin_ref.update({"token": nueva_contrasena_hashed})

        return {"message": "Contraseña de admin actualizada correctamente"}

    except Exception as e:
        # Capturar cualquier error y lanzar una excepción HTTP
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
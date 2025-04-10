import bcrypt
from firebase_config import db
from models.modelo_usuarios import Usuario, Pedido, CambioContrasenaRequest, LoginRequest
from datetime import datetime
from fastapi import HTTPException
import secrets  # 📌 Para generar el token de seguridad
import traceback  # 👈


def hash_password(password: str) -> str:
    """Hashea la contraseña antes de guardarla en la base de datos"""
    salt = bcrypt.gensalt()  # Genera un salt único
    hashed_password = bcrypt.hashpw(password.encode(), salt)  # Hashea la contraseña con el salt
    return hashed_password.decode()  # Devolvemos el hash como string

def obtener_usuarios():
    try:
        usuarios_ref = db.collection("usuarios").stream()
        usuarios = [{"id": doc.id, **doc.to_dict()} for doc in usuarios_ref]
        return {"usuarios": usuarios}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def crear_usuario(usuario: Usuario):
    try:
        nuevo_usuario = usuario.dict()
        nuevo_usuario["last_login"] = datetime.utcnow()

        # Hashear la contraseña antes de guardarla
        nuevo_usuario["token"] = hash_password(usuario.token)

        # Agregar usuario a Firestore y obtener el ID generado
        doc_ref = db.collection("usuarios").add(nuevo_usuario)
        usuario_id = doc_ref[1].id

        # Guardar el ID dentro del propio documento
        db.collection("usuarios").document(usuario_id).update({"id": usuario_id})

        # Devolver el usuario completo con ID actualizado
        usuario_data = {**nuevo_usuario, "id": usuario_id}

        return {"message": "Usuario agregado correctamente", "usuario": usuario_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def agregar_pedido(id: str, pedido: Pedido):
    try:
        usuario_ref = db.collection("usuarios").document(id)
        usuario = usuario_ref.get()

        if usuario.exists:
            usuario_data = usuario.to_dict()
            pedidos_actuales = usuario_data.get("pedidos", [])
            pedidos_actuales.append(pedido.dict())

            usuario_ref.update({"pedidos": pedidos_actuales})
            return {"message": "Pedido agregado correctamente", "pedido": pedido.dict()}
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

    except Exception as e:
        print("🔥 ERROR AGREGANDO PEDIDO 🔥")
        print("Payload recibido:", pedido.dict())
        traceback.print_exc()  # 👈 Muestra traza completa en logs
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


def eliminar_usuario(id: str):
    try:
        usuario_ref = db.collection("usuarios").document(id)
        if usuario_ref.get().exists:
            usuario_ref.delete()
            return {"message": f"Usuario con ID {id} eliminado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def eliminar_pedido(id_usuario: str, id_pedido: str):
    try:
        usuario_ref = db.collection("usuarios").document(id_usuario)
        usuario = usuario_ref.get()

        if usuario.exists:
            usuario_data = usuario.to_dict()
            pedidos_actuales = usuario_data.get("pedidos", [])

            # Filtrar los pedidos para eliminar el que coincide con id_pedido
            pedidos_actualizados = [pedido for pedido in pedidos_actuales if pedido["id_pedido"] != id_pedido]

            if len(pedidos_actualizados) == len(pedidos_actuales):
                raise HTTPException(status_code=404, detail="Pedido no encontrado")

            usuario_ref.update({"pedidos": pedidos_actualizados})
            return {"message": f"Pedido {id_pedido} eliminado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def verificar_password(password: str, hashed_password: str) -> bool:
    """Compara la contraseña ingresada con el hash almacenado en la base de datos"""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def cambiar_contrasena(username: str, contrasena_actual: str, nueva_contrasena: str):
    try:
        usuarios_ref = db.collection("usuarios").where("username", "==", username).stream()
        usuarios = [doc for doc in usuarios_ref]

        if not usuarios:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if len(usuarios) > 1:
            raise HTTPException(status_code=400, detail="Username duplicado, contacta soporte")

        usuario_ref = usuarios[0].reference
        usuario_data = usuarios[0].to_dict()

        if not verificar_password(contrasena_actual, usuario_data["token"]):
            raise HTTPException(status_code=403, detail="Contraseña actual incorrecta")

        nueva_contrasena_hashed = bcrypt.hashpw(nueva_contrasena.encode(), bcrypt.gensalt()).decode()
        usuario_ref.update({"token": nueva_contrasena_hashed})

        return {"message": "Contraseña actualizada correctamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


def login_usuario(username: str, token: str):
    try:
        # Buscar primero en admins
        admins_ref = db.collection("admins").where("username", "==", username).stream()
        admins = [doc for doc in admins_ref]

        if admins:
            admin_data = admins[0].to_dict()

            if not verificar_password(token, admin_data["token"]):
                raise HTTPException(status_code=401, detail="Contraseña incorrecta (admin)")

            admins[0].reference.update({"last_login": datetime.utcnow()})

            tipo = admin_data.get("tipo", "admin")
            admin_data.pop("token", None)

            return {
                "message": "Login exitoso (admin)",
                "usuario": {
                    **admin_data,
                    "tipo_usuario": "admin"  # 🔥 estándar como acordamos
                }
            }

        # Si no es admin, buscar en usuarios
        usuarios_ref = db.collection("usuarios").where("username", "==", username).stream()
        usuarios = [doc for doc in usuarios_ref]

        if not usuarios:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        usuario_data = usuarios[0].to_dict()

        if not verificar_password(token, usuario_data["token"]):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        usuarios[0].reference.update({"last_login": datetime.utcnow()})
        usuario_data.pop("token", None)

        return {
            "message": "Login exitoso",
            "usuario": {
                **usuario_data,
                "tipo_usuario": usuario_data.get("tipo_usuario", "cliente")
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



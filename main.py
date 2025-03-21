from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, APIRouter, Path
from pydantic import BaseModel, EmailStr
from models.modelo_usuarios import Usuario, Pedido, CambioContrasenaRequest
from models.modelo_admins import Admin, CambioContrasenaAdminRequest
from models.modelo_productos import Producto
from services.usuarios import obtener_usuarios, crear_usuario, agregar_pedido, eliminar_usuario, eliminar_pedido, cambiar_contrasena
from services.admins import obtener_admins, crear_admin, eliminar_admin, cambiar_contrasena_admin 
from services.productos import crear_producto ,obtener_producto_por_nombre, obtener_productos, eliminar_producto, obtener_producto_por_nombre, actualizar_producto, modificar_producto
from fastapi.middleware.cors import CORSMiddleware
from firebase_config import db
from typing import Optional, List
from datetime import datetime
from typing import Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las fuentes (puedes restringirlo a tu frontend)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/usuarios")
def get_usuarios():
    return obtener_usuarios()

@app.post("/usuarios")
def post_usuario(usuario: Usuario):
    return crear_usuario(usuario)

@app.post("/usuarios/{id}/pedidos")
def post_pedido(id: str, pedido: Pedido):
    return agregar_pedido(id, pedido)

@app.delete("/usuarios/{id}")
def delete_usuario(id: str):
    return eliminar_usuario(id)

@app.delete("/usuarios/{id_usuario}/pedidos/{id_pedido}")
def delete_pedido(id_usuario: str, id_pedido: str):
    return eliminar_pedido(id_usuario, id_pedido)

@app.get("/admins")
def get_admins():
    return obtener_admins()

@app.post("/admins")
def post_admin(admin: Admin):
    return crear_admin(admin)

@app.delete("/admins/{id}")
def delete_admin(id: str):
    return eliminar_admin(id)

# 📌 Ruta correcta para cambiar la contraseña
@app.patch("/usuarios/cambiar-contrasena")
def patch_cambiar_contrasena(request: CambioContrasenaRequest):
    return cambiar_contrasena(request.nombre_usuario, request.contrasena_actual, request.nueva_contrasena)

@app.patch("/admins/cambiar-contrasena")
async def cambiar_contrasena_admin_route(cambio: CambioContrasenaAdminRequest ):
    return cambiar_contrasena_admin(cambio.nombre_usuario, cambio.contrasena_actual, cambio.nueva_contrasena)

# 📌 Crear producto
@app.post("/productos")
def crear_producto_route(producto: Producto):
    return crear_producto(producto)

# 📌 Obtener todos los productos
@app.get("/productos")
def obtener_productos_route():
    return obtener_productos()

# 📌 Obtener un producto por nombre
@app.get("/productos/{nombre}")
def obtener_producto_por_nombre_route(nombre: str = Path(..., title="Nombre del producto")):
    return obtener_producto_por_nombre(nombre)

# 📌 Actualizar producto completo (PUT)
@app.put("/productos/{id}")
def actualizar_producto_route(id: str, producto: Producto):
    return actualizar_producto(id, producto)

# 📌 Modificar campos específicos de un producto (PATCH)
@app.patch("/productos/{id}")
def modificar_producto_route(id: str, cambios: Dict[str, str]):
    return modificar_producto(id, cambios)

# 📌 Eliminar producto
@app.delete("/productos/{id}")
def eliminar_producto_route(id: str):
    return eliminar_producto(id)
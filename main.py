from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_config import db

# 🚀 Importar los routers
from routes.rutas_usuarios import router as usuarios_router
from routes.rutas_admins import router as admins_router
from routes.rutas_productos import router as productos_router
from routes.rutas_pedidos import router as pedidos_router
from routes.rutas_carrito_abandonado import router as carritos_abandonados_router
from routes.rutas_facturas import router as facturas_router
from routes.ruta_login import router as login_router
from routes.rutas_cupon import router as cupones_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a dominios específicos si lo deseas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Incluir todos los routers aquí
app.include_router(usuarios_router)
app.include_router(admins_router)
app.include_router(productos_router)
app.include_router(pedidos_router)
app.include_router(carritos_abandonados_router)
app.include_router(facturas_router)
app.include_router(login_router)
app.include_router(cupones_router)

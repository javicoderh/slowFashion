import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# 📌 Cargar credenciales desde una variable de entorno en vez de un archivo JSON
firebase_config_json = os.getenv("FIREBASE_CONFIG")

if not firebase_config_json:
    raise ValueError("⚠️ No se encontraron credenciales de Firebase en variables de entorno.")

# 📌 Convertir la cadena JSON a un diccionario
firebase_config_dict = json.loads(firebase_config_json)

# 📌 Inicializar Firebase con las credenciales en formato dict
cred = credentials.Certificate(firebase_config_dict)
firebase_admin.initialize_app(cred)

# 📌 Inicializar Firestore
db = firestore.client()

import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# Cargar credenciales desde el JSON
cred = credentials.Certificate("slowfashion-users-firebase-adminsdk-fbsvc-cfabc3828e.json")
firebase_admin.initialize_app(cred)

# Inicializar Firestore
db = firestore.client()

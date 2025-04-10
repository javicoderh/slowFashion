from fastapi import APIRouter
from models.modelo_usuarios import LoginRequest
from services.usuarios import login_usuario

router = APIRouter(tags=["Login"])

@router.post("/login")
def login_route(request: LoginRequest):
    return login_usuario(request.username, request.token)

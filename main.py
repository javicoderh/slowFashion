from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a Slow Fashion API"}

@app.get("/usuarios")
def get_usuarios():
    return {"usuarios": ["usuario1", "usuario2", "usuario3"]}

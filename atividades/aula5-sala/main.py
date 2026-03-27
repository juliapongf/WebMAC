from fastapi import FastAPI, Request
from fastapi import Depends, HTTPException, status, Cookie, Response
from typing import Annotated
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Usuario(BaseModel):
    nome: str
    senha: str
    bio: str

# Base de dados
users_db = []

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request, "signin.html")

@app.post("/users")
async def create_user(usuario: Usuario):
    users_db.append(usuario)
    return {"message": "Usuário criado com sucesso"}

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")


# 1. Rota para "Logar" (Define o Cookie)
@app.post("/login")
def login(username: str, password: str, response: Response):
    # Buscamos o usuário usando um laço simples
    usuario_encontrado = None
    for u in users_db:
        if u["nome"] == username:
            usuario_encontrado = u
            break
    
    if not usuario_encontrado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # O servidor diz ao navegador: "Guarde esse nome no cookie 'session_user'"
    response.set_cookie(key="session_user", value=username)
    return {"message": "Logado com sucesso"}

# 2. A Dependência: Lendo o Cookie
def get_active_user(session_user: Annotated[str | None, Cookie()] = None):
    # O FastAPI busca automaticamente um cookie chamado 'session_user'
    if not session_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acesso negado: você não está logado."
        )
    
    user = next((u for u in users_db if u["nome"] == session_user), None)
    if not user:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    return user

# 3. Rota Protegida
@app.get("/home")
def show_profile(request: Request, user: dict = Depends(get_active_user)):
    return templates.TemplateResponse(
        request=request, 
        name="profile.html", 
        context={"nome": user["nome"], "bio": user["bio"]})
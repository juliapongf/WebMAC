from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

#Inicializando aplicativo
app = FastAPI()

# Preparando templates e arquivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Funções que renderizam html
@app.get("/home")
async def pagina_inicial(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse(request, "index.html")

@app.get("/editar")
async def pagina_editar(request: Request, response_class=HTMLResponse):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "editar.html", {"pagina": "/editar/filmes"})
    return templates.TemplateResponse(request, "editar.html")

@app.get("/editar/filmes")
async def pagina_filmes(request: Request, response_class=HTMLResponse):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "editar.html", {"pagina": "/editar/filmes"})
    return templates.TemplateResponse(request, "filmes.html")


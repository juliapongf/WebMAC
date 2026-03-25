from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

contador = 0
aba_ativa = 0

@app.get("/home", response_class=HTMLResponse)
async def curtida(request: Request):
    global aba_ativa
    aba_ativa = 0
    if (not "HX-Request" in request.headers):
        global contador
        contador = 0
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/curtidas", "contador": contador})
    return templates.TemplateResponse(request, "index.html")

@app.get("/home/curtidas", response_class=HTMLResponse)
async def curtida(request: Request):
    global aba_ativa
    aba_ativa = 0
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/curtidas", "contador": contador})
    return templates.TemplateResponse(request, "curtidas.html", {"contador": contador})

@app.get("/home/pagina1", response_class=HTMLResponse)
async def pag1(request: Request):
    global aba_ativa
    aba_ativa = 1
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/pagina1"})
    return templates.TemplateResponse(request, "jupiter.html")

@app.get("/home/pagina2", response_class=HTMLResponse)
async def pag2(request: Request):
    global aba_ativa
    aba_ativa = 2
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/pagina2"})
    return templates.TemplateResponse(request, "professor.html")


@app.post("/curtir")
async def curtir(request: Request):
    global contador
    contador = contador+1
    return templates.TemplateResponse(request, "contador.html", {"contador": contador})

@app.delete("/curtir")
async def deletar_curtidas(request: Request):
    global contador
    contador = 0
    return templates.TemplateResponse(request, "contador.html", {"contador": contador})

@app.get("/abas")
async def alternar_abas(request: Request):
    global aba_ativa
    if (aba_ativa == 0):
        aba_ativa = 1
        return templates.TemplateResponse(request, "jupiter.html")
    elif (aba_ativa == 1):
        aba_ativa = 2
        return templates.TemplateResponse(request, "professor.html")
    else:
        aba_ativa = 0
        return templates.TemplateResponse(request, "curtidas.html", {"contador": contador})
        

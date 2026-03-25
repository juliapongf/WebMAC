from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/home",response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"pagina": "/home/curtidas"})

@app.get("/home/curtidas", response_class=HTMLResponse)
async def curtida(request: Request):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/curtidas"})
    return templates.TemplateResponse(request, "curtidas.html")

@app.get("/home/pagina1", response_class=HTMLResponse)
async def pag1(request: Request):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/curtidas"})
    return templates.TemplateResponse(request, "jupiter.html")

@app.get("/home/pagina2", response_class=HTMLResponse)
async def pag2(request: Request):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "index.html", {"pagina": "/home/curtidas"})
    return templates.TemplateResponse(request, "professor.html")

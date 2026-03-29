from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select, SQLModel, create_engine
from models import *
from typing import List, Optional


#Criando a engine do banco de dados
arquivo_sqlite = "cinefilo.db"
url_sqlite = f"sqlite:///{arquivo_sqlite}"

engine = create_engine(url_sqlite)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#Inicializando aplicativo
app = FastAPI()

# Preparando templates e arquivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


################################################################################################
# Funções que renderizam html
################################################################################################


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

@app.get("/editar/ator")
async def pagina_filmes(request: Request, response_class=HTMLResponse):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "editar.html", {"pagina": "/editar/filmes"})
    return templates.TemplateResponse(request, "atores.html")

@app.get("/editar/diretor")
async def pagina_filmes(request: Request, response_class=HTMLResponse):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "editar.html", {"pagina": "/editar/filmes"})
    return templates.TemplateResponse(request, "diretores.html")

@app.get("/pesquisar")
async def pagina_pesquisar(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse(request, "pesquisar.html")

@app.get("/configurar")
async def pagina_configurar(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse(request, "configurar.html")


######################################################################################################
# Manipulação do banco de dados
######################################################################################################


##### Criação de itens no banco de dados #####

@app.post("/novoFilme", response_class=HTMLResponse)
def criar_filme(titulo: str = Form(...), ano: int = Form(...), lista: str = Form(...), nota: int = Form(...), resenha: Optional[str] = Form(None)):
    with Session(engine) as session:
        novo_filme = Filme(titulo=titulo, ano=ano, lista=lista, nota=nota, resenha=resenha)
        session.add(novo_filme)
        session.commit()
        session.refresh(novo_filme)
        return HTMLResponse(content=f"<p>O filme {novo_filme.titulo} foi salvo na lista {novo_filme.lista}!</p>")
    
@app.post("/novoDiretor", response_class=HTMLResponse)
def criar_diretor(nome: str = Form(...), biografia: Optional[str] = Form(None)):
    with Session(engine) as session:
        novo_diretor= Diretor(nome=nome, biografia=biografia)
        session.add(novo_diretor)
        session.commit()
        session.refresh(novo_diretor)
        return HTMLResponse(content=f"<p>O(a) diretor(a) {novo_diretor.nome} foi salvo(a)!</p>")
    
@app.post("/novoAtor", response_class=HTMLResponse)
def criar_ator(nome: str = Form(...), biografia: Optional[str] = Form(None)):
    with Session(engine) as session:
        novo_ator= Ator(nome=nome, biografia=biografia)
        session.add(novo_ator)
        session.commit()
        session.refresh(novo_ator)
        return HTMLResponse(content=f"<p>O(a) ator/atriz {novo_ator.nome} foi salvo(a)!</p>")
    
@app.post("/novaDirecao", response_class=HTMLResponse)
def criar_direcao(idfilme: int = Form(...), iddiretor: int = Form(...)):
    with Session(engine) as session:
        query1 = select(Filme).where(Filme.id == idfilme)
        filme = session.exec(query1).first()
        if (not filme):
            return HTMLResponse(content="<p>Filme não encontrado!</p>")
        query2 = select(Diretor).where(Diretor.id == iddiretor)
        diretor = session.exec(query2).first()
        if (not diretor):
            return HTMLResponse(content="<p>Diretor(a) não encontrado(a)!</p>")
        nova_direcao= Direcao(filme_id=idfilme, diretor_id=iddiretor)
        session.add(nova_direcao)
        session.commit()
        session.refresh(nova_direcao)
        return HTMLResponse(content=f"<p>{diretor.nome} dirigiu o filme {filme.titulo}!</p>")
    
@app.post("/novaAtuacao", response_class=HTMLResponse)
def criar_atuacao(idfilme: int = Form(...), idator: int = Form(...)):
    with Session(engine) as session:
        query1 = select(Filme).where(Filme.id == idfilme)
        filme = session.exec(query1).first()
        if (not filme):
            return HTMLResponse(content="<p>Filme não encontrado!</p>")
        query2 = select(Ator).where(Ator.id == iddiretor)
        ator = session.exec(query2).first()
        if (not ator):
            return HTMLResponse(content="<p>Ator/atriz não encontrado(a)!</p>")
        nova_atuacao= Atuacao(filme_id=idfilme, ator_id=idator)
        session.add(nova_atuacao)
        session.commit()
        session.refresh(nova_atuacao)
        return HTMLResponse(content=f"<p>{ator.nome} atuou no filme {filme.titulo}!</p>")
    
    
##### Deleção de itens do banco de dados #####

@app.delete("/deletaFilme", response_class=HTMLResponse)
def deletar_filme(id: int):
    with Session(engine) as session:
        query = select(Filme).where(Filme.id == id)
        filme = session.exec(query).first()
        if (not filme):
            return HTMLResponse(content="<p>Filme não encontrado!</p>")
        titulo = filme.titulo
        session.delete(filme)
        session.commit()
        return HTMLResponse(content=f"<p>O filme {titulo} foi deletado!</p>")
    
@app.delete("/deletaDiretor", response_class=HTMLResponse)
def deletar_diretor(id: int):
    with Session(engine) as session:
        query = select(Diretor).where(Diretor.id == id)
        diretor = session.exec(query).first()
        if (not diretor):
            return HTMLResponse(content="<p>Diretor não encontrado!</p>")
        nome = diretor.nome
        session.delete(diretor)
        session.commit()
        return HTMLResponse(content=f"<p>O(a) diretor(a) {nome} foi deletado(a)!</p>")
    
@app.delete("/deletaAtor", response_class=HTMLResponse)
def deletar_ator(id: int):
    with Session(engine) as session:
        query = select(Ator).where(Ator.id == id)
        ator = session.exec(query).first()
        if (not ator):
            return HTMLResponse(content="<p>Ator/atriz não encontrado(a)!</p>")
        nome = ator.nome
        session.delete(ator)
        session.commit()
        return HTMLResponse(content=f"<p>O(a) ator/atriz {nome} foi deletado(a)!</p>")
    

##### Busca de itens no banco de dados #####

def buscar_filmes(busca, lista, pagina):
    limite = 3
    with Session(engine) as session:
        query = select(Filme).where((Filme.titulo).contains(busca)).order_by(Filme.titulo)
        filmes = session.exec(query).all()
        inicio = pagina*limite
        tamanho = len(filmes)
        if (pagina == 0):
            temanterior = False
        else:
            temanterior = True
        if (inicio+limite < tamanho):
            temproximo = True
        else:
            temproximo = False
        if (inicio+limite <= tamanho):
            paginacao = filmes[inicio: inicio+limite]
        else:
            paginacao = filmes[inicio:tamanho]

        return paginacao, pagina, temanterior, temproximo, busca
    
def buscar_diretores(busca, pagina):
    limite=3
    with Session(engine) as session:
        query = select(Diretor).where((Diretor.nome).contains(busca)).order_by(Diretor.nome)
        diretores = session.exec(query).all()
        inicio = pagina*limite
        tamanho = len(diretores)
        if (pagina == 0):
            temanterior = False
        else:
            temanterior = True
        if (inicio+limite < tamanho):
            temproximo = True
        else:
            temproximo = False
        if (inicio+limite <= tamanho):
            paginacao = diretores[inicio: inicio+limite]
        else:
            paginacao = diretores[inicio:tamanho]

        return paginacao, pagina, temanterior, temproximo, busca

def buscar_atores(busca, pagina):
    limite=3
    with Session(engine) as session:
        query = select(Ator).where((Ator.nome).contains(busca)).order_by(Ator.nome)
        atores = session.exec(query).all()
        inicio = pagina*limite
        tamanho = len(atores)
        if (pagina == 0):
            temanterior = False
        else:
            temanterior = True
        if (inicio+limite < tamanho):
            temproximo = True
        else:
            temproximo = False
        if (inicio+limite <= tamanho):
            resultados = atores[inicio: inicio+limite]
        else:
            resultados = atores[inicio:tamanho]

        return resultados, pagina, temanterior, temproximo, busca
    
@app.get("/buscar", response_class=HTMLResponse)
def pesquisar(request: Request, campo1: str, campo2: str, pagina: int=0, busca: str | None=''):
    if (campo1 == "filme"):
        resultados, pagina, temanterior, temproximo, busca = buscar_filmes(busca, campo2, pagina)
    elif (campo1 == "ator"):
        resultados, pagina, temanterior, temproximo, busca = buscar_atores(busca, pagina)
    else:
        resultados, pagina, temanterior, temproximo, busca = buscar_diretores(busca, pagina)
    return templates.TemplateResponse(request, "resultados.html", {"resultados": resultados, "campo1": campo1, "campo2": campo2, "pagina": pagina, "temanterior": temanterior, "temproximo": temproximo, "busca": busca})

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select, SQLModel, create_engine
from models import *
from typing import List, Optional
from sqlalchemy import func


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


# Tela 1
@app.get("/home")
async def pagina_inicial(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse(request, "index.html")

# Tela 2
@app.get("/editar")
async def pagina_editar(request: Request, response_class=HTMLResponse):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "editar.html", {"pagina": "/editar/filmes"})
    return templates.TemplateResponse(request, "editar.html")

# HTMLs parciais da tela 2
@app.get("/editar/filmes")
async def pagina_filmes(request: Request, response_class=HTMLResponse):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "editar.html", {"pagina": "/editar/filmes"})
    return templates.TemplateResponse(request, "filmes.html")

@app.get("/editar/ator")
async def pagina_atores(request: Request, response_class=HTMLResponse):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "editar.html", {"pagina": "/editar/filmes"})
    return templates.TemplateResponse(request, "atores.html")

@app.get("/editar/diretor")
async def pagina_diretores(request: Request, response_class=HTMLResponse):
    if (not "HX-Request" in request.headers):
        return templates.TemplateResponse(request, "editar.html", {"pagina": "/editar/filmes"})
    return templates.TemplateResponse(request, "diretores.html")

# Tela 3
@app.get("/pesquisar")
async def pagina_pesquisar(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse(request, "pesquisar.html")

# Tela 4
@app.get("/configurar")
async def pagina_configurar(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse(request, "configurar.html")


######################################################################################################
# Manipulação do banco de dados
######################################################################################################


##### Criação de itens no banco de dados #####

@app.post("/novoFilme", response_class=HTMLResponse)
def criar_filme(titulo: str = Form(...), ano: int = Form(...), lista: str = Form(...), nota: Optional[int] = Form(None), resenha: Optional[str] = Form(None)):
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
        query2 = select(Ator).where(Ator.id == idator)
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
        return HTMLResponse(content=f"<p>O filme {titulo} foi excluído!</p>")
    
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
        return HTMLResponse(content=f"<p>O(a) diretor(a) {nome} foi excluído(a)!</p>")
    
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
        return HTMLResponse(content=f"<p>O(a) ator/atriz {nome} foi excluído(a)!</p>")
    
@app.delete("/deletaDirecao", response_class=HTMLResponse)
def deletar_direcao(idfilme: int, iddiretor: int):
    with Session(engine) as session:
        query1 = select(Direcao).where(Direcao.filme_id == idfilme, Direcao.diretor_id == iddiretor)
        direcao = session.exec(query1).first()
        if (not direcao):
            return HTMLResponse(content="<p>Diretor(a) já não dirigia esse filme!</p>")
        query2 = select(Filme).where(Filme.id == idfilme)
        filme = session.exec(query2).first()
        query3 = select(Diretor).where(Diretor.id == iddiretor)
        diretor = session.exec(query3).first()
        session.delete(direcao)
        session.commit()
        return HTMLResponse(content=f"<p>O(a) diretor(a) {diretor.nome} não dirigiu o filme {filme.titulo}!</p>")
    
@app.delete("/deletaAtuacao", response_class=HTMLResponse)
def deletar_atuacao(idfilme: int, idator: int):
    with Session(engine) as session:
        query = select(Atuacao).where(Atuacao.filme_id == idfilme, Atuacao.ator_id == idator)
        atuacao = session.exec(query).first()
        if (not atuacao):
            return HTMLResponse(content="<p>Ator/atriz já não fazia parte desse filme!</p>")
        query2 = select(Filme).where(Filme.id == idfilme)
        filme = session.exec(query2).first()
        query3 = select(Ator).where(Ator.id == idator)
        ator = session.exec(query3).first()
        session.delete(atuacao)
        session.commit()
        return HTMLResponse(content=f"<p>O(a) ator/atriz {ator.nome} não participou do filme {filme.titulo}!</p>")
    

##### Busca de itens no banco de dados #####

# Funções de busca para cada tipo de objeto

def buscar_filmes(busca, lista, pagina):
    limite = 3
    with Session(engine) as session:
        if (lista == "ambas"): # Seleciona filmes de ambas as listas
            query = select(Filme).where((Filme.titulo).contains(busca)).order_by(func.lower(Filme.titulo))
        else: # Seleciona filmes de apenas uma das listas, "Favoritos" ou "Para assistir"
            query = select(Filme).where(Filme.lista == lista, (Filme.titulo).contains(busca)).order_by(Filme.titulo)
        filmes = session.exec(query).all()

        # Implementando paginação
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
            resultados = filmes[inicio: inicio+limite]
        else:
            resultados = filmes[inicio:tamanho]

        # Obtendo as listas de diretores e atores de cada filme
        diretores1 = {}
        atores1 = {}
        for filme in resultados:
            diretores2 = []
            atores2 = []
            for diretor in filme.diretores:
                d_nome = diretor.nome
                diretores2.append(d_nome)
            for ator in filme.atores:
                a_nome = ator.nome
                atores2.append(a_nome)
            diretores1[filme.id] = list(diretores2)
            atores1[filme.id] = list(atores2)

        return resultados, pagina, temanterior, temproximo, busca, diretores1, atores1
    
def buscar_diretores(busca, pagina):
    limite=3
    with Session(engine) as session:
        query = select(Diretor).where((Diretor.nome).contains(busca)).order_by(func.lower(Diretor.nome))
        diretores = session.exec(query).all()

        # Implementando paginação
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
            resultados = diretores[inicio: inicio+limite]
        else:
            resultados = diretores[inicio:tamanho]
        
        # Obtendo as listas de filmes de cada diretor
        filmes1 = {}
        for diretor in resultados:
            filmes2 = []
            for filme in diretor.filmes:
                titulo = filme.titulo
                filmes2.append(titulo)
            filmes1[diretor.id] = list(filmes2)

        return resultados, pagina, temanterior, temproximo, busca, filmes1

def buscar_atores(busca, pagina):
    limite=3
    with Session(engine) as session:
        query = select(Ator).where((Ator.nome).contains(busca)).order_by(func.lower(Ator.nome))
        atores = session.exec(query).all()

        # Implementando paginação
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

        # Obtendo as listas de filmes de cada ator
        filmes1 = {}
        for ator in resultados:
            filmes2 = []
            for filme in ator.filmes:
                titulo = filme.titulo
                filmes2.append(titulo)
            filmes1[ator.id] = list(filmes2)

        return resultados, pagina, temanterior, temproximo, busca, filmes1
    
# Função de busca geral
    
@app.get("/buscar", response_class=HTMLResponse)
def pesquisar(request: Request, campo1: str, campo2: str, pagina: int=0, busca: str | None=''):
    if (campo1 == "filme"):
        resultados, pagina, temanterior, temproximo, busca, diretores, atores = buscar_filmes(busca, campo2, pagina)
        return templates.TemplateResponse(request, "resultados.html", {"resultados": resultados, "campo1": campo1, "campo2": campo2, "pagina": pagina, "temanterior": temanterior, "temproximo": temproximo, "busca": busca, "diretores": diretores, "atores": atores})
    elif (campo1 == "ator"):
        resultados, pagina, temanterior, temproximo, busca, filmes = buscar_atores(busca, pagina)
        return templates.TemplateResponse(request, "resultados.html", {"resultados": resultados, "campo1": campo1, "campo2": campo2, "pagina": pagina, "temanterior": temanterior, "temproximo": temproximo, "busca": busca, "filmes": filmes})
    else:
        resultados, pagina, temanterior, temproximo, busca, filmes = buscar_diretores(busca, pagina)
        return templates.TemplateResponse(request, "resultados.html", {"resultados": resultados, "campo1": campo1, "campo2": campo2, "pagina": pagina, "temanterior": temanterior, "temproximo": temproximo, "busca": busca, "filmes": filmes})


##### Atualização de itens no banco de dados #####

@app.put("/atualizaFilme", response_class=HTMLResponse)
def atualizar_filme(id: int = Form(...), campo: str = Form(...), novoTitulo: Optional[str] = Form(None), novoAno: Optional[int] = Form(None), novaLista: Optional[str] = Form(None), novaNota: Optional[int] = Form(None), novaResenha: Optional[str] = Form(None)):
    with Session(engine) as session:
        query = select(Filme).where(Filme.id == id)
        filme = session.exec(query).first()
        if (not filme):
            return HTMLResponse(content="<p>Filme não encontrado!</p>")
        
        if (campo == "titulo"):
            tituloAntigo = filme.titulo
            filme.titulo = novoTitulo
            session.commit()
            session.refresh(filme)
            return HTMLResponse(content=f"<p>O título do filme {tituloAntigo} foi atualizado para {filme.titulo}!</p>")
        elif (campo == "ano"):
            anoAntigo = filme.ano
            filme.ano = novoAno
            session.commit()
            session.refresh(filme)
            return HTMLResponse(content=f"<p>O ano do filme {filme.titulo} foi atualizado de {anoAntigo} para {filme.ano}!</p>")
        elif (campo == "lista"):
            listaAntiga = filme.lista
            filme.lista = novaLista
            session.commit()
            session.refresh(filme)
            return HTMLResponse(content=f"<p>A lista do filme {filme.titulo} foi atualizada de {listaAntiga} para {filme.lista}!</p>")
        elif (campo == "nota"):
            notaAntiga = filme.nota
            filme.nota = novaNota
            session.commit()
            session.refresh(filme)
            return HTMLResponse(content=f"<p>A nota do filme {filme.titulo} foi atualizada para {filme.nota}!</p>")
        else:
            resenhaAntiga = filme.resenha
            filme.resenha = novaResenha
            session.commit()
            session.refresh(filme)
            return HTMLResponse(content=f"<p>A resenha do filme {filme.titulo} foi atualizada!</p>")
        

@app.put("/atualizaDiretor", response_class=HTMLResponse)
def atualizar_diretor(id: int = Form(...), campo: str = Form(...), novoNome: Optional[str] = Form(None), novaBiografia: Optional[str] = Form(None)):
    with Session(engine) as session:
        query = select(Diretor).where(Diretor.id == id)
        diretor = session.exec(query).first()
        if (not diretor):
            return HTMLResponse(content="<p>Diretor(a) não encontrado(a)!</p>")
        
        if (campo == "nome"):
            nomeAntigo = diretor.nome
            diretor.nome = novoNome
            session.commit()
            session.refresh(diretor)
            return HTMLResponse(content=f"<p>O nome do(a) diretor(a) {nomeAntigo} foi atualizado para {diretor.nome}!</p>")
        else:
            diretor.biografia = novaBiografia
            session.commit()
            session.refresh(diretor)
            return HTMLResponse(content=f"<p>A biografia do(a) diretor(a) {diretor.nome} foi atualizada!</p>")
        
@app.put("/atualizaAtor", response_class=HTMLResponse)
def atualizar_ator(id: int = Form(...), campo: str = Form(...), novoNome: Optional[str] = Form(None), novaBiografia: Optional[str] = Form(None)):
    with Session(engine) as session:
        query = select(Ator).where(Ator.id == id)
        ator = session.exec(query).first()
        if (not ator):
            return HTMLResponse(content="<p>Ator/atriz não encontrado(a)!</p>")
        
        if (campo == "nome"):
            nomeAntigo = ator.nome
            ator.nome = novoNome
            session.commit()
            session.refresh(ator)
            return HTMLResponse(content=f"<p>O nome do(a) ator/atriz {nomeAntigo} foi atualizado para {ator.nome}!</p>")
        else:
            ator.biografia = novaBiografia
            session.commit()
            session.refresh(ator)
            return HTMLResponse(content=f"<p>A biografia do(a) diretor(a) {ator.nome} foi atualizada!</p>")

from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class Atuacao(SQLModel, table=True):
    filme_id: Optional[int] = Field(
        default=None,
        foreign_key="filme.id",
        primary_key=True,
    )
    ator_id: Optional[int] = Field(
        default=None,
        foreign_key="ator.id",
        primary_key=True,
    )

class Direcao(SQLModel, table=True):
    filme_id: Optional[int] = Field(
        default=None,
        foreign_key="filme.id",
        primary_key=True,
    )
    diretor_id: Optional[int] = Field(
        default=None,
        foreign_key="diretor.id",
        primary_key=True,
    )

class Filme(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    titulo: str
    ano: int
    lista: str
    nota:  Optional[int] = Field(default=None)
    resenha:  Optional[str] = Field(default=None)


    atores: List["Ator"] = Relationship(
        back_populates="filmes",
        link_model=Atuacao,
    )

    diretores: List["Diretor"] = Relationship(
        back_populates="filmes",
        link_model=Direcao,
    )

class Ator(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    nome: str
    biografia:  Optional[str] = Field(default=None)


    filmes: List["Filme"] = Relationship(
        back_populates="atores",
        link_model=Atuacao,
    )

class Diretor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    nome: str
    biografia:  Optional[str] = Field(default=None)


    filmes: List["Filme"] = Relationship(
        back_populates="diretores",
        link_model=Direcao,
    )


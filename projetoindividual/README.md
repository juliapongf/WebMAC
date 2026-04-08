# Projeto Individual da disciplina "MAC0350 - Introdução ao Desenvolvimento de Sistemas de Software

## Aplicativo de filmes "O Cinéfilo"

### Funcionalidades:
 - Adicionar filmes, diretores e atores (com hx-post);
 - Busca de filmes, filtrados por "assistidos" e "para assistir", busca de diretores, e busca de atores, com a exibição de todas as informações sobre eles (com hx-get). Resultados da busca têm paginação;
 - Opção de modificar as informações sobre os filmes, diretores e atores (com hx-put);
 - Deletar filmes/séries (com hx-delete)
 - Opção de customizar o site com a cor que o usuário prefere (feito por Javascript)

### Relações
 - Muitos para muitos: um mesmo filme pode ter vários atores e diretores, o mesmo diretor ou ator pode ter vários filmes. As listas de atores e diretores de um filme, a lista de filmes de um ator, e a lista de filmes de um diretor são exibidas entre as informações da busca.


# Projeto Individual da disciplina "MAC0350 - Introdução ao Desenvolvimento de Sistemas de Software

## Agenda de filmes e séries

### Funcionalidades:
 - Adicionar séries ou filmes (com hx-post)
 - Busca de tarefas ou filmes, filtrados por "assistidos" e "para assistir no futuro", "filmes" ou "séries" ou por gênero (com hx-get)
 - Opção de modificar as informações sobre o filme/série, como descrição, gênero e se já foi assistido ou não (com hx-put)
 - Rankeamento por notas (com paginação)
 - Atualizar tarefas
 - Deletar filmes/séries (com hx-delete)

### Relações
 - Muitos para muitos: um mesmo filme pode ter vários gêneros, o mesmo gênero pode ter vários filmes
 - Um pra um: um filme só pode ter um valor de assistido/não assistido, uma nota e um valor de filme/série


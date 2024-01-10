## Blog-API é uma API feita em Django + PostgreSQL, experimental e para estudos

O foco deste app é mostrar meus conhecimentos em API RESTful, utilizando Django, Django Rest Framework e PostgreSQL.

### Ferramentas:
- Fácil criação e manutenção de usuários
- Segurança em diferentes tipos de usuários
- Personalização de views de acordo com permissões de usuário
- Segurança baseada em login e tokens jwt (access e refresh tokens)
- Código simples e de fácil entendimento (seu código é a sua documentação)

### Como implementar:
As credenciais de banco e etc estão sendo lidas de um arquivo env.py, na mesma pasta de settings.py, o mesmo está incluido no .gitignore deste projeto.
Foi escolhido esta forma de armazenamento para evitar problemas com variáveis de ambiente no futuro deploy do sistema, mas fique a contade para coloca-las onde preferir.
Deve ser criado uma venv, e instalado todos as libs de requirements.txt, para evitar conflito. Não esqueça de migrar suas configurações para o seu banco.

### Como usar:
Depois de tudo instalado e as primeiras migrações feitas, é recomendável que seja feito a criação de um superuser com `py manage.py createsuperuser`
Para criação de usuário não é necessário nenhuma credencial, as rotas são:
- admin/ - para entrar no portal admin do Django
- api/token/ - criação de token (exige email e password)
- api/token/refresh/ - refresh do token
- api/token/verify/ - verificação da validade do token
- ~~api/blog/v1/posts/ - para acessar os posts a partir das primeiras funções feitas (function based view), permite get e post. Não é recomendável o seu uso~~
- ~~api/blog/v1/posts/int:pk - mesmo caso anterior, mas para um post em específico, permite get, patch e delete. Não é recomendável o seu uso~~
- api/blog/v2/posts/ - view feita com ModelViewSet, permite get, post, patch e delete. É preciso está autenticado para post, e ser dono do post para patch e delete. Os posts já trazem consigo a lista de comentários que o compoem.
- api/blog/v2/users/ - view feita com ModelViewSet, permite get, post, patch e delete. Para criar um usuário com Post, ou dar um get nos usuários, não é necessário autenticação.
Usuário normal só conseguem editar os seus próprios dados e não conseguem se promover. Usuários Admin conseguem mudar os dados de outros usuários, inclusive subir seus acessos.
- api/blog/v2/comments/ - view feita com ModelViewSet, permite get, post, patch e delete. É preciso está autenticado para post, e ser dono do comentário para patch e delete.

### Testes automatizados:
  Ainda serão implementados

### Changelog:
  v1.0 - 10/01/2023

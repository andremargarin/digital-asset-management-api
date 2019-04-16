# Digital Asset Management API

API para gerenciamento de arquivos de áudio e vídeo.

## Rodando o projeto no ambiente local
Executa o build e roda o projeto:

`docker-compose -f local.yml up --build`

Executa as migrações:

`docker-compose -f local.yml exec django python manage.py migrate`

Cria superuser para testes:

`docker-compose -f local.yml exec django python manage.py createsuperuser`

Coleta arquivos estáticos:

`docker-compose -f local.yml exec django python manage.py collecstatic`


## Rodando os testes
`docker-compose -f local.yml exec django manage.py test`

### Rodando os testes e verificando cobertura
`docker-compose -f local.yml exec django coverage run --source='.' manage.py test`

`docker-compose -f local.yml exec django coverage report`

# Desafio Stone API

## Como executar o projeto ?

#
Clone este repositório
```shell
$ git clone git@github.com:vhmvcitor/desafio-stone
```

Acesse a pasta do projeto no terminal/cmd
```shell
$ cd/desafio-stone
```

Crie um arquivo .env e insira as suas credênciais, como mostra o exemplo abaixo
```shell
# CREDENCIAIS BANCO DE DADOS - Psycopg2

DB_NAME= “db_name”
DB_USER= “db_user”
DB_PASS= “db_password”
DB_HOST= “db_host”
DB_PORT= “db_password”
PORT= “db_port”

# CREDENCIAIS TOKEN JWT

SECRET_KET=“jwt_secret_key”
ALGORITHM=“jwt_algorithm”
ACCESS_TOKEN_EXPIRE_MINUTES=“jwt_token_exíre_minutes”

```

Instale as dependências: Executar comando de Build do Docker
```shell
$ docker build . -t desafio-stone
```

Execute a aplicação: Run do Docker
```shell
$ docker run -it -p 8080:8080 --env-file .env -t desafio-stone
```

Fiz o deploy da aplicação na plataforma do Heroku. Também instânciei um BD de testes na mesma plataforma. Segue url da RESTAPI: "https://api-desafio-stone.herokuapp.com/docs" 

Para fins de teste, utilizar o usuário(adm):
```shell
email: victor@teste.com
senha: 123456
```

## Arquivo main - API:

Arquivo principal da REST API. Aqui é feito o redirecionamento das principais rotas através do "FastAPI"
```py
import os
import uvicorn

from fastapi import FastAPI

from auth import controller as authController
from rota import controller as rotaController
from vendedor import controller as vendedorController
from cliente import controller as clienteController
from log import controller as logController

app = FastAPI(title="Desafio Stone - RestAPI",  description="<h3>EndPoints referentes a aplicação</h3>")

app.include_router(authController.router)
app.include_router(rotaController.router)
app.include_router(vendedorController.router)
app.include_router(clienteController.router)
app.include_router(logController.router)
```

# Funções:
- findExistuser(user_email):
    Função utilizada para auxiliar o processo de inserção de novos usuários.

- findExistedSeller(seller_email): 
    Função utilizada para auxiliar o processo de inserção de novos vendedores.

- findExistedSeller(seller_id): 
    Função utilizada para auxiliar o processo de inserção de novos usuários. Aqui o parâmetro da função é o id do ventedor

- findExistedRoute(route_bounds):
    Função utilizada para auxiliar o processo de inserção de novas rotas.

- findRouteIntersection(route_bounds):
    Função utilizada para auxiliar o processo de inserção de novas rotas. É feito uma verificação nas rotas existentes e caso haja intersecção entre a rota adicionada e as rotas presentes no sistema, ocorre um erro, não permitindo o cadastro da nova rota.

- getAllRoutes():
    Função utilizada para buscar todas rotas cadastradas no banco de dados.

- getAllBounds:
    Função utilizada para buscar as coordenadas dos polígonos(rotas) cadastradas, afim de fazer a verificação da intercção entre as rotas.

- gindExistedClient(client_bounds):
    Função utilizada para auxiliar o processo de inserção de novos clientes.

- findClientContainsRoute(client_bounds):
    Função utilizada o mapeamento automáticos da rota a qual pertence as coordenadas do cliente.

- create_log():
    Função utilizada para motoriramento de alterações realizadas no sistema, como cadastro/edição/exclusão de dados.

## Visualização das rotas e clientes cadastrados:
Implementei um script ("map.py") que faz a busca de todas as rotas e clientes cadastrados no banco e faz a plotagem de suas geolocalizações no mapa gerando o arquivo "map.html", localizado na pasta "map". Utilizei a biblioteca "folium" para executar essa função. Abaixo coloquei uma demonstração das rotas e clientes cadastrados

![alt text](/map/rotas.png)

# Entidades:

Lista com todas as entidades/tables que compõem a REST API

#
## Usuário

| Atributos         | Tipo              |   
|-------------------|-------------------|
| id                | integer           |
| email             | text              |
| senha             | text              |
| nome              | text              |
| is_adm            | boolean           |
| status            | integer           |
| data_criacao      | timestamp         |
| data_atualizacao  | timestamp         |

#
## Rota

| Atributos         | Tipo              |   
|-------------------|-------------------|
| id                | integer           |
| bounds            | doublue precision |
| nome              | text              |
| vendedor_id       | integer           |
| data_criacao      | timestamp         |
| data_atualizacao  | timestamp         |
| data_deletacao    | timestamp         |

#
## Cliente

| Atributos         | Tipo              |   
|-------------------|-------------------|
| id                | integer           |
| nome              | text              |
| geolocalizacao    | doublue precision |
| rota_id           | integer           |
| vendedor_id       | integer           |
| data_criacao      | timestamp         |
| data_atualizacao  | timestamp         |
| data_deletacao    | timestamp         |

#
## Vendedor

| Atributos         | Tipo              |   
|-------------------|-------------------|
| id                | integer           |
| nome              | text              |
| email             | text              |
| data_criacao      | timestamp         |
| data_atualizacao  | timestamp         |
| data_deletacao    | timestamp         |

#
## Log

| Atributos         | Tipo              |   
|-------------------|-------------------|
| id                | integer           |
| acao              | text              |
| entidade          | text              |
| usuario_id        | integer           |
| usuario_nome      | text              |
| registro          | text              |
| data_criacao      | timestamp         |

#
# $hopkeeper

Sistema de gestão para pequenos negócios.

Desenvolvido em Python com interface baseada em Tkinter.

## Direitos Autorais

Copyright © 2025 Rafael Renó Corrêa | owariyumi@gmail.com

Todos os direitos reservados.

## Execução

Instale o Python:

`sudo apt install python3 python3-venv`

Inicie um ambiente virtual Python:

`python3 -m venv .venv`

Acesse o ambiente virtual:

`source .venv/bin/activate`

Instale as dependências:

`pip install -r requirements.txt`

Inicialize as tabelas no banco PostgreSQL a partir do arquivo `db/schema.sql`. Em seguida, copie o arquivo `core/components/.env.example` para `core/components/.env` e preencha com as informações necessárias.

Por fim, inicie a aplicação:

`python3 app.py`

## Compatibilidade

Disponível para sistemas Linux e Windows.

Testado no Ubuntu 25.10.
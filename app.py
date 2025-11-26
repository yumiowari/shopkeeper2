from core.controller import Controller

import os
'''
    os provê uma forma portátil de usar operações dependentes do sistema operacional.
'''

import core.components.db as db
'''
    db implementa funções para manipulação do banco de dados.
'''

if __name__ == '__main__':
    credentials = db.fetch_credentials()
    
    if credentials == []:
        print('\n===== CADASTRO DE USUÁRIO ADMINISTRADOR =====\n')
        username = input('Insira o nome de usuário: ')
        email = input('Insira o e-mail do usuário: ')
        password = input('Insira a senha: ')

        db.update_credentials({'username': username, 'email': email, 'password': password})

    app = Controller()
    app.bootstrap()
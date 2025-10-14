from core.controller import Controller

import os
'''
    os provê uma forma portátil de usar operações dependentes do sistema operacional.
'''

import core.components.SGBD as SGBD
'''
    SGBD implementa funções para manipulação do banco de dados.
'''

if __name__ == '__main__':
    if not os.path.isfile('data/credentials.pkl'):
        print('\n===== CADASTRO DE USUÁRIO ADMINISTRADOR =====\n')
        username = input('Insira o nome de usuário: ')
        password = input('Insira a senha: ')

        SGBD.update_credentials({'username': username, 'password': password})

    app = Controller()
    app.bootstrap()
import pickle as pkl
'''
    O módulo pickle em Python permite serializar e desserializar objetos Python,
    transformando-os em uma sequência de bytes que pode ser armazenada em um arquivo.
'''

import os
'''
    os provê uma forma portátil de usar operações dependentes do sistema operacional.
'''

'''
    Inventário
'''
def fetch_stock():
    if os.path.isfile('data/stock.pkl'):
        with open('data/stock.pkl', 'rb') as file:
            try:
                return pkl.load(file)
            except EOFError:
                return []
    else:
        return []

def update_stock(stock):
    with open('data/stock.pkl', 'wb') as file:
        pkl.dump(stock, file)

'''
    Comandas
'''
def fetch_curr_order():
    if os.path.isfile('data/order.pkl'):
        with open('data/order.pkl', 'rb') as file:
            try:
                return pkl.load(file)
            except EOFError:
                return []
    else:
        return []
    
def update_curr_order(order):
    with open('data/order.pkl', 'wb') as file:
        pkl.dump(order, file)

def delete_curr_order():
    if os.path.isfile('data/order.pkl'):
        os.remove('data/order.pkl')

def store_comm_order(order):
    path = 'data/' + order.timestamp

    os.makedirs(path, exist_ok=True)

    path += '/order.pkl'

    with open(path, 'wb') as file:
        pkl.dump(order, file)
import core.components.SGBD as SGBD
'''
    SGBD implementa funções para manipulação do banco de dados.
'''

from core.components.objects import *
'''
    Importa as definições dos objetos de dados.
'''

import os
'''
    os provê uma forma portátil de usar operações dependentes do sistema operacional.
'''

import pickle as pkl
'''
    O módulo pickle em Python permite serializar e desserializar objetos Python,
    transformando-os em uma sequência de bytes que pode ser armazenada em um arquivo.
'''

from datetime import datetime
'''
    O módulo datetime oferece classes para manipulação de data e hora.
'''

class CreateOrderModel:
    def __init__(self):
        self.__stock = []

        # current order
        self.__curr_order = [] # (list of sales)

    def on_close(self):
        #SGBD.delete_curr_order() # deleta a comanda atual (ainda não deferida) do disco rígido
        pass

    '''
        Retorna a lista de produtos no estoque
    '''
    def fetch_product_names(self):
        self.__stock = SGBD.fetch_stock()

        # ordena o estoque de acordo com os identificadores dos produtos
        self.__stock.sort(key=lambda p: p.id)

        product_names = []

        for product in self.__stock:
            product_names.append(product.name)

        return product_names
    
    '''
        Defere a comanda no banco de dados

        Retorna...
            >0 - Sucesso;
             0 - Estoque indisponível;
            <1 - Produto inválido.
    '''
    def commit_order(self, curr_order):
        self.__stock = SGBD.fetch_stock()

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        comm_order = Order(timestamp)

        for sale in curr_order:
            flag = False

            for product in self.__stock:
                if sale['name'] == product.name:
                    flag = True

                    sale_qty = int(sale['qty'])
                    sale_value = float(float(product.price) * sale_qty)

                    sale = Sale(product.id, sale_qty, sale_value)

                    comm_order.append_sale(sale)

                    comm_order.value += sale_value

                    if product.qty - sale_qty < 0:
                        return 0
                    else:
                        product.qty -= sale_qty

                    break

            if not flag:
                return -1

        SGBD.update_stock(self.__stock)

        SGBD.commit_order(comm_order)

        return comm_order.value

class ConferOrderModel:
    def __init__(self):
        # commited orders
        self.__comm_orders = []

    def on_close(self):
        pass

    '''
        Recupera a lista de comandas deferidas
    '''
    def fetch_order_list(self, selected_date):
        #self.__comm_orders = []
        #
        #for folder_name in os.listdir('data'):
        #    folder_path = os.path.join('data', folder_name)
        #
        #    if os.path.isdir(folder_path):
        #        # verifica se o nome da pasta começa com a data selecionada
        #        if folder_name.startswith(selected_date.strftime('%Y-%m-%d')):
        #            file_path = os.path.join(folder_path, 'order.pkl')
        #
        #            if os.path.exists(file_path):
        #                with open(file_path, 'rb') as file:
        #                    comm_order = pkl.load(file)
        #
        #                    self.__comm_orders.append(comm_order)

        self.__comm_orders = SGBD.fetch_order_list(selected_date)

        return SGBD.fetch_order_list(selected_date)
    
    '''
        Retorna a comanda referente ao timestamp selecionado
    '''
    def fetch_order(self, selected_timestamp):
        for comm_order in self.__comm_orders:
            if comm_order.timestamp == selected_timestamp:
                return comm_order
        # método rápido, aproveita a consulta anterior em fetch_order_list
            
        return None
    
    '''
        Retorna o inventário
    '''
    def fetch_stock(self):
        return SGBD.fetch_stock()
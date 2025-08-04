from core.components.SGBD import *
'''
    SGBD implementa funções para manipulação do banco de dados.
'''

from datetime import datetime
'''
    O módulo datetime oferece classes para manipulação de data e hora.
'''

import os
'''
    os provê uma forma portátil de usar operações dependentes do sistema operacional.
'''

class Model:
    def __init__(self):
        self.__stock = []

        # current order
        self.__curr_order = [] # list of sales

        # commited order
        self.__comm_order = {
            'timestamp': '',
            'sales': [],
            'value': 0.0
        }

    def on_close(self):
        delete_curr_order() # deleta a comanda atual (ainda não deferida) do disco rígido

    '''
        Retorna a lista de produtos selecionados...
        No formato: (<Quantidade>) <Nome do produto>
    '''
    def fetch_selected_items(self):
        self.__curr_order = fetch_curr_order()

        products = []

        for sale in self.__curr_order:
            product = '(' + str(sale['qty']) + ') ' + sale['name']
            products.append(product)

        return products
    
    '''
        Defere a comanda no banco de dados

        Retorna...
            >0 - Sucesso;
             0 - Comanda vazia;
            <0 - Estoque indisponível.
    '''
    def commit_sale(self):
        self.__curr_order = fetch_curr_order()
        self.__stock = fetch_stock()

        self.__comm_order['value'] = 0.0
        self.__comm_order['items'] = []

        flag = True

        for sale in self.__curr_order:
            for item in self.__stock:
                if sale['name'] == item['name']:
                    comm_sale = {
                        'name': sale['name'],
                        'qty' : int(sale['qty']),
                        'value': float(float(item['price']) * int(sale['qty']))
                    }

                    self.__comm_order['value'] += comm_sale['value']

                    self.__comm_order['sales'].append(comm_sale)

                    # atualiza o estoque (na memória)
                    self.__stock.remove(item)

                    item['qty'] -= int(comm_sale['qty'])
                    if item['qty'] < 0:
                        flag = False

                        break

                    self.__stock.insert(0, item)
                    #

        self.__comm_order['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        store_comm_order(self.__comm_order)

        # atualiza o estoque (no disco rígido)
        if flag:
            update_stock(self.__stock)

            return self.__comm_order['value']
        else:
            return -1
                
    '''
        Remove o produto selecionado

        Retorna...
            0 - Sucesso;
            1 - Item não encontrado.
    '''
    def remove_product(self, item_name):
        self.__curr_order = fetch_curr_order() # redundante

        for product in self.__curr_order:
            if product['name'] == item_name:
                self.__curr_order.remove(product)

                update_curr_order(self.__curr_order)

                return 0
            
        return 1

class ProductModel:
    def __init__(self):
        self.__stock = []

        # current order
        self.__curr_order = [] # list of sales

    def on_close(self):
        pass

    '''
        Retorna a lista de produtos no estoque
    '''
    def fetch_item_names(self):
        self.__stock = fetch_stock()

        if not self.__stock:
            return []
        else:
            return [item['name'] for item in self.__stock]
        
    '''
        Confirma o produto selecionado

        Retorna...
            0 - Sucesso;
            1 - Item não encontrado.
    '''
    def confirm_product(self, item_name, item_qty):
        self.__stock = fetch_stock()

        for item in self.__stock:
            if item['name'] == item_name:
                selected_item = {
                    'name': item_name,
                    'qty': item_qty
                }

                self.__curr_order = fetch_curr_order()

                flag = False

                for sale in self.__curr_order:
                    if sale['name'] == item_name:
                        # se o produto já foi selecionado, apenas atualiza a quantidade
                        self.__curr_order.remove(sale)

                        curr_qty = int(sale['qty'])
                        curr_qty += int(item_qty)
                        sale['qty'] = curr_qty

                        self.__curr_order.append(sale)

                        flag = True

                if not flag:
                    self.__curr_order.append(selected_item)

                update_curr_order(self.__curr_order)
                
                return 0

        return 1
    
class ConferOrderModel:
    def __init__(self):
        # commited orders
        self.__comm_order_list = []

    def on_close(self):
        pass

    '''
        Recupera a lista de comandas deferidas
    '''
    def fetch_order_list(self, selected_date):
        self.__comm_order_list = []

        for folder_name in os.listdir('data'):
            folder_path = os.path.join('data', folder_name)

            if os.path.isdir(folder_path):
                # verifica se o nome da pasta começa com a data selecionada
                if folder_name.startswith(selected_date.strftime('%Y-%m-%d')):
                    file_path = os.path.join(folder_path, 'order.pkl')

                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as file:
                            comm_order = pkl.load(file)

                            self.__comm_order_list.append(comm_order)

        return self.__comm_order_list
    
    '''
        Retorna a comanda referente ao timestamp selecionado
    '''
    def fetch_order(self, selected_timestamp):
        for comm_order in self.__comm_order_list:
            if comm_order['timestamp'] == selected_timestamp:
                return comm_order
            
        return {}
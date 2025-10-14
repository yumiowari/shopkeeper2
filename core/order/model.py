import core.components.SGBD as SGBD
'''
    SGBD implementa funções para manipulação do banco de dados.
'''

from core.components.objects import *
'''
    Importa as definições dos objetos de dados.
'''

from datetime import datetime
'''
    O módulo datetime oferece classes para manipulação de data e hora.
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

class CreateOrderModel:
    def __init__(self):
        self.__stock = []

        # current order
        self.__curr_order = [] # (list of sales)

    def on_close(self):
        SGBD.delete_curr_order() # deleta a comanda atual (ainda não deferida) do disco rígido

    '''
        Retorna a lista de produtos selecionados...
        No formato: (<Quantidade>) <Nome do produto>
    '''
    def fetch_selected_products(self):
        self.__curr_order = SGBD.fetch_curr_order()

        curr_products = []

        for sale in self.__curr_order:
            product = '(' + str(sale.qty) + ') ' + sale.name
            curr_products.append(product)

        return curr_products
    
    '''
        Defere a comanda no banco de dados

        Retorna...
            >0 - Sucesso;
             0 - Comanda vazia;
            <0 - Estoque indisponível.
    '''
    def commit_sale(self):
        self.__curr_order = SGBD.fetch_curr_order()
        self.__stock = SGBD.fetch_stock()

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        comm_order = Order(timestamp)

        flag = True

        for curr_product in self.__curr_order:
            product_id = curr_product.id
            qty = int(curr_product.qty)
            value = float(float(curr_product.price) * int(curr_product.qty))

            comm_sale = Sale(product_id, qty, value)

            comm_order.value += comm_sale.value

            comm_order.append_sale(comm_sale)

            # atualiza o estoque (na memória)
            for product in self.__stock:
                if product.id == product_id:
                    product.qty -= int(comm_sale.qty)
                    if product.qty < 0:
                        flag = False

                        break

                    # empurra o produto para o começo da lista
                    self.__stock.remove(product)
                    self.__stock.insert(0, product)
            #

        if comm_order.value == 0:
            return 0 # nenhum produto foi selecionado

        # defere a comanda no disco rígido
        if flag:
            SGBD.store_comm_order(comm_order)

            SGBD.update_stock(self.__stock)

            return comm_order.value
        else:
            return -1 # não havia estoque disponível
                
    '''
        Remove o produto selecionado

        Retorna...
            0 - Sucesso;
            1 - Produto não encontrado.
    '''
    def remove_product(self, product_name):
        self.__curr_order = SGBD.fetch_curr_order()

        for product in self.__curr_order:
            if product.name == product_name:
                self.__curr_order.remove(product)

                SGBD.update_curr_order(self.__curr_order)

                return 0
            
        return 1

class SelectProductModel:
    def __init__(self):
        self.__stock = []

        # current order
        self.__curr_order = [] # (list of sales)

    def on_close(self):
        pass

    '''
        Retorna a lista de produtos no estoque
    '''
    def fetch_product_names(self):
        self.__stock = SGBD.fetch_stock()

        if not self.__stock:
            return []
        else:
            return [product.name for product in self.__stock]
        
    '''
        Confirma o produto selecionado

        Retorna...
            0 - Sucesso;
            1 - Produto não encontrado.
    '''
    def confirm_product(self, product_name, product_qty):
        self.__stock = SGBD.fetch_stock()

        # se inseriu o ID do produto,
        if product_name.isdigit():
            for product in self.__stock:
                if product.id == int(product_name):
                    product_name = product.name # sobrescreve com o nome do produto

                    break

        if product_name.isdigit():
            return 1 # o ID do produto não era válido.

        for product in self.__stock:
            if product.name == product_name:
                id = product.id
                name = product.name
                cost = product.cost
                price = product.price
                qty = product_qty

                selected_product = Product(id, name, cost, price, qty)

                self.__curr_order = SGBD.fetch_curr_order()

                flag = False

                for curr_product in self.__curr_order:
                    if curr_product.name == product_name:
                        # se o produto já foi selecionado, apenas atualiza a quantidade
                        self.__curr_order.remove(curr_product)

                        curr_qty = int(curr_product.qty)
                        curr_qty += int(product_qty)
                        curr_product.qty = curr_qty

                        self.__curr_order.append(curr_product)

                        flag = True

                if not flag:
                    self.__curr_order.append(selected_product)

                SGBD.update_curr_order(self.__curr_order)
                
                return 0

        return 1
    
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
        self.__comm_orders = []

        for folder_name in os.listdir('data'):
            folder_path = os.path.join('data', folder_name)

            if os.path.isdir(folder_path):
                # verifica se o nome da pasta começa com a data selecionada
                if folder_name.startswith(selected_date.strftime('%Y-%m-%d')):
                    file_path = os.path.join(folder_path, 'order.pkl')

                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as file:
                            comm_order = pkl.load(file)

                            self.__comm_orders.append(comm_order)

        return self.__comm_orders
    
    '''
        Retorna a comanda referente ao timestamp selecionado
    '''
    def fetch_order(self, selected_timestamp):
        for comm_order in self.__comm_orders:
            if comm_order.timestamp == selected_timestamp:
                return comm_order
            
        return None
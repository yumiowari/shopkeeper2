from core.components.SGBD import *
from datetime import datetime

class Model:
    def __init__(self):
        self.__item = {
            'name': '',
            'cost': 0.0,
            'price': 0.0,
            'qty': 0
        }

        self.__stock = []

        self.__sale = {
            'name': '',
            'qty': 0,
            'value': 0.0
        }

        # current order
        self.__curr_order = [] # list of sales

        # commited order
        self.__comm_order = {
            'timestamp': '',
            'sales': [],
            'value': 0.0
        }

    def on_close(self):
        delete_curr_order()

    def fetch_selected_items(self):
        self.__curr_order = fetch_curr_order()

        products = []

        for sale in self.__curr_order:
            product = "(" + str(sale['qty']) + ") " + sale['name']
            products.append(product)

        return products
    
    # finaliza a comanda e armazena no banco de dados
    #
    # retorna...
    # >0 - sucesso
    #  0 - comanda vazia
    # <0 - estoque indisponível
    def commit_sale(self):
        self.__curr_order = fetch_curr_order()
        self.__stock = fetch_stock()

        self.__comm_order['value'] = 0.0
        self.__comm_order['items'] = []

        flag = True

        for sale in self.__curr_order:
            for item in self.__stock:
                if sale['name'] == item['name']:
                    self.__sale['name'] = sale['name']
                    self.__sale['qty'] = int(sale['qty'])
                    self.__sale['value'] = float(item['price']) * int(sale['qty'])

                    self.__comm_order['value'] += self.__sale['value']

                    self.__comm_order['sales'].append(self.__sale)

                    # atualiza o estoque (localmente)
                    self.__stock.remove(item)

                    item['qty'] -= int(sale['qty'])
                    if item['qty'] < 0:
                        flag = False

                        break

                    self.__stock.append(item)
                    #

                    break # garante que o produto não será processado mais de uma vez

        self.__comm_order['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        store_comm_order(self.__comm_order)

        # atualiza o estoque (remotamente)
        if flag:
            update_stock(self.__stock)

            return self.__comm_order['value']
        else:
            return -1
                
    # remove o produto selecionado
    #
    # retorna...
    # 0 - sucesso
    # 1 - item não encontrado
    def remove_product(self, item_name):
        self.__curr_order = fetch_curr_order()

        for product in self.__curr_order:
            if product['name'] == item_name:
                self.__curr_order.remove(product)

                update_curr_order(self.__curr_order)

                return 0
            
        return 1

class ProductModel:
    def __init__(self):
        self.__item = {
            'name': '',
            'cost': 0.0,
            'price': 0.0,
            'qty': 0
        }

        self.__selected_item = {
            'name': '',
            'qty': 0
        }

        self.__stock = []

        # current order
        self.__curr_order = [] # list of sales

    def on_close(self):
        pass

    def fetch_item_names(self):
        self.__stock = fetch_stock()

        if not self.__stock:
            return []
        else:
            return [item['name'] for item in self.__stock]
        
    # confirma o produto selecionado
    #
    # retorna...
    # 0 - sucesso
    # 1 - item não encontrado
    def confirm_product(self, item_name, item_qty):
        self.__stock = fetch_stock()

        for item in self.__stock:
            if item['name'] == item_name:
                self.__selected_item['name'] = item_name
                self.__selected_item['qty'] = item_qty

                self.__curr_order = fetch_curr_order()

                flag = False

                for sale in self.__curr_order:
                    if sale['name'] == item_name:
                        self.__curr_order.remove(sale)

                        curr_qty = int(sale['qty'])
                        curr_qty += int(item_qty)
                        sale['qty'] = curr_qty

                        self.__curr_order.append(sale)

                        flag = True

                if not flag:
                    self.__curr_order.append(self.__selected_item)

                update_curr_order(self.__curr_order)
                
                return 0

        return 1
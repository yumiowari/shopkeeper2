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

        self.__selected_item = {
            'name': '',
            'qty': 0
        }

        self.__sale = {
            'name': '',
            'qty': 0,
            'value': 0
        }

        self.__items = []

        self.__curr_sale = []

        self.__comm_sale = {
            'timestamp': '',
            'items': [],
            'value': 0.0
        }

    def on_close(self):
        delete_curr_sale()

    def fetch_selected_items(self):
        self.__curr_sale = fetch_curr_sale()

        products = []

        for sale in self.__curr_sale:
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
        self.__curr_sale = fetch_curr_sale()
        self.__items = fetch_stock()

        self.__comm_sale['value'] = 0.0
        self.__comm_sale['items'] = []

        flag = True

        for product in self.__curr_sale:
            for item in self.__items:
                if product['name'] == item['name']:
                    sale_entry = {
                        'name': product['name'],
                        'qty': product['qty'],
                        'value': float(item['price']) * float(product['qty'])
                    }

                    self.__comm_sale['value'] += sale_entry['value']

                    print(f"value: f{self.__comm_sale['value']}")

                    self.__comm_sale['items'].append(sale_entry)

                    # atualiza o estoque (localmente)
                    self.__items.remove(item)

                    item['qty'] -= int(product['qty'])
                    if item['qty'] < 0:
                        flag = False

                        break

                    self.__items.append(item)
                    #

                    break # <-- isso garante que o produto não será processado mais de uma vez

        self.__comm_sale['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        store_comm_sale(self.__comm_sale)

        # atualiza o estoque (remotamente)
        if flag:
            update_stock(self.__items)

            return self.__comm_sale['value']
        else:
            return -1
                
    # remove o produto selecionado
    #
    # retorna...
    # 0 - sucesso
    # 1 - item não encontrado
    def remove_product(self, item_name):
        self.__curr_sale = fetch_curr_sale()

        for product in self.__curr_sale:
            if product['name'] == item_name:
                self.__curr_sale.remove(product)

                update_curr_sale(self.__curr_sale)

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

        self.__items = []

        self.__curr_sale = []

    def on_close(self):
        pass # to do: limpar dados

    def fetch_item_names(self):
        self.__items = fetch_stock()

        if not self.__items:
            return []
        else:
            return [item['name'] for item in self.__items]
        
    # confirma o produto selecionado
    #
    # retorna...
    # 0 - sucesso
    # 1 - item não encontrado
    def confirm_product(self, item_name, item_qty):
        self.__items = fetch_stock()

        for item in self.__items:
            if item['name'] == item_name:
                self.__selected_item['name'] = item_name
                self.__selected_item['qty'] = item_qty

                self.__curr_sale = fetch_curr_sale()

                flag = False

                for sale in self.__curr_sale:
                    if sale['name'] == item_name:
                        self.__curr_sale.remove(sale)

                        curr_qty = int(sale['qty'])
                        curr_qty += int(item_qty)
                        sale['qty'] = curr_qty

                        self.__curr_sale.append(sale)

                        flag = True

                if not flag:
                    self.__curr_sale.append(self.__selected_item)

                update_curr_sale(self.__curr_sale)
                
                return 0

        return 1
from core.components.SGBD import *

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

        self.__items = []

        self.__curr_sale = []

    def on_close(self):
        delete_curr_sale()

    def fetch_selected_items(self):
        self.__curr_sale = fetch_curr_sale()

        products = []

        for product in self.__curr_sale:
            products.append(product['name'] + ' : ' + product['qty'])

        return products

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

                self.__curr_sale.append(self.__selected_item)

                update_curr_sale(self.__curr_sale)
                
                return 0

        return 1
import pickle as pkl
import os

class Model:
    def __init__(self):
        self.__item = {
            'name': '',
            'cost': 0.0,
            'price': 0.0,
            'qty': 0
        }

        self.__items = []

    def fetch_stock(self):
        if os.path.isfile('data/stock.pkl'):
            with open('data/stock.pkl', 'rb') as file:
                try:
                    self.__items = pkl.load(file)
                except EOFError:
                    self.__items = []
        else:
            self.__items = []

    def update_stock(self):
        with open('data/stock.pkl', 'wb') as file:
            pkl.dump(self.__items, file)

    # cadastra o produto no estoque
    #
    # retorna...
    # 0 - sucesso
    # 1 - item repetido
    def create_item(self, item_name, item_cost, item_price, item_qty):
        self.__item['name'] = item_name
        self.__item['cost'] = float(item_cost)
        self.__item['price'] = float(item_price)
        self.__item['qty'] = int(item_qty)

        self.fetch_stock()

        # verifica se o item já existe com mesmo nome
        if any(item['name'] == item_name for item in self.__items):
            return 1 # item repetido

        self.__items.append(self.__item.copy())

        self.update_stock()

        return 0 # sucesso
    #

    def fetch_item_names(self):
        self.fetch_stock()

        if not self.__items:
            return []
        else:
            return [item['name'] for item in self.__items]

    # consulta o produto no estoque
    def confer_item(self, item_name):
        self.fetch_stock()

        if not self.__items:
            return None
        else:
            for item in self.__items:
                if item['name'] == item_name:
                    return item
    #

    # atualiza o produto no estoque
    #
    # retorna...
    # 0 - sucesso
    # 1 - sem alterações
    # 2 - item não encontrado
    def update_item(self, item_name, item_cost, item_price, item_qty):
        self.fetch_stock()

        for item in self.__items:
            if item['name'] == item_name:
                if float(item_cost) == item['cost'] and float(item_price) == item['price'] and int(item_qty) == item['qty']:
                    return 1 # sem alterações
                else:
                    if item_cost != 0.0:
                        item['cost'] = float(item_cost)
                    if item_price != 0.0:
                        item['price'] = float(item_price)
                    if item_qty != '':
                        item['qty'] = int(item_qty)

                self.update_stock()

                return 0
            
        return 2 # item não encontrado
    #

    # deleta o produto do estoque
    #
    # retorna...
    # 0 - sucesso
    # 1 - item não encontrado
    def delete_item(self, item_name):
        self.fetch_stock()

        for item in self.__items:
            if item['name'] == item_name:
                self.__items.remove(item)
                self.update_stock()

                return 0

        return 1
    #

class EntryModel:
    def __init__(self):
        self.__item = {
            'name': '',
            'cost': 0.0,
            'price': 0.0,
            'qty': 0
        }

        self.__items = []

    def fetch_stock(self):
        if os.path.isfile('data/stock.pkl'):
            with open('data/stock.pkl', 'rb') as file:
                try:
                    self.__items = pkl.load(file)
                except EOFError:
                    self.__items = []
        else:
            self.__items = []

    def update_stock(self):
        with open('data/stock.pkl', 'wb') as file:
            pkl.dump(self.__items, file)

    def fetch_item_names(self):
        self.fetch_stock()

        if not self.__items:
            return []
        else:
            return [item['name'] for item in self.__items]
        
    # registra a entrada/saída do produto no estoque
    #
    # retorna...
    # 0 - sucesso
    # 1 - item não encontrado
    def entry_item(self, item_name, entry_qty):
        self.fetch_stock()

        for item in self.__items:
            if item['name'] == item_name:
                curr_qty = item['qty']

                curr_qty += int(entry_qty)

                item['qty'] = curr_qty

                self.update_stock()

                return 0

        return 1
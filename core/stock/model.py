from core.components.SGBD import *
'''
    SGBD implementa funções para manipulação do banco de dados.
'''

class Model:
    def __init__(self):
        self.__item = {
            'name': '',
            'cost': 0.0,
            'price': 0.0,
            'qty': 0
        }

        self.__stock = []

    '''
        Cadastra o produto no Inventário

        Retorna...
            0 - Sucesso;
            1 - Item repetido.
    '''
    def create_item(self, item_name, item_cost, item_price, item_qty):
        self.__item['name'] = item_name
        self.__item['cost'] = float(item_cost)
        self.__item['price'] = float(item_price)
        if not item_qty:
            self.__item['qty'] = 0
        else:
            self.__item['qty'] = int(item_qty)

        self.__stock = fetch_stock()

        # verifica se o item já existe com mesmo nome
        if any(item['name'] == item_name for item in self.__stock):
            return 1 # item repetido

        self.__stock.append(self.__item.copy())

        update_stock(self.__stock)

        return 0 # sucesso

    def fetch_item_names(self):
        self.__stock = fetch_stock()

        if not self.__stock:
            return []
        else:
            return [item['name'] for item in self.__stock]

    '''
        Consulta o produto no Inventário
    '''
    def confer_item(self, item_name):
        self.__stock = fetch_stock()

        if not self.__stock:
            return None
        else:
            for item in self.__stock:
                if item['name'] == item_name:
                    return item

    '''
        Atualiza o produto no estoque

        Retorna...
            0 - Sucesso;
            1 - Sem alterações;
            2 - Item não encontrado.
    '''
    def update_item(self, item_name, item_cost, item_price, item_qty):
        # correção de campos vazios
        if not item_cost:
            item_cost = 0.0
        if not item_price:
            item_price = 0.0
        if not item_qty:
            item_qty = ''

        self.__stock = fetch_stock()

        for item in self.__stock:
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

                update_stock(self.__stock)

                return 0
            
        return 2 # item não encontrado

    '''
        Remove o produto do estoque

        Retorna...
            0 - Sucesso;
            1 - Item não encontrado.
    '''
    def delete_item(self, item_name):
        self.__stock = fetch_stock()

        for item in self.__stock:
            if item['name'] == item_name:
                self.__stock.remove(item)
                update_stock(self.__stock)

                return 0

        return 1

class EntryModel:
    def __init__(self):
        self.__item = {
            'name': '',
            'cost': 0.0,
            'price': 0.0,
            'qty': 0
        }

        self.__stock = []

    def fetch_item_names(self):
        self.__stock = fetch_stock()

        if not self.__stock:
            return []
        else:
            return [item['name'] for item in self.__stock]
        
    '''
        Registra a entrada/saída do produto no Inventário

        Retorna...
            0 - Sucesso;
            1 - Item não encontrado.
    '''
    def entry_item(self, item_name, entry_qty):
        self.__stock = fetch_stock()

        for item in self.__stock:
            if item['name'] == item_name:
                curr_qty = item['qty']
                curr_qty += int(entry_qty)
                item['qty'] = curr_qty

                update_stock(self.__stock)

                return 0

        return 1
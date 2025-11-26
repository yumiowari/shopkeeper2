import core.components.db as db
'''
    db implementa funções para manipulação do banco de dados.
'''

from core.components.objects import *
'''
    Importa as definições dos objetos de dados.
'''

class CRUDModel:
    def __init__(self):
        self.__stock = []

    '''
        Cadastra o produto no Inventário

        Retorna...
            0 - Sucesso;
            1 - Produto repetido.
    '''
    def create_product(self, name, category, cost, price, qty):
        self.__stock = db.fetch_stock()
        
        size = len(self.__stock) + 1

        if not qty:
            product = Product(int(size), name, float(cost), float(price), 0)
        else:
            product = Product(int(size), name, float(cost), float(price), int(qty))

        product.category = category

        # verifica se algum produto já existe com o mesmo nome
        if any(product.name == name for product in self.__stock):
            return 1 # produto repetido

        self.__stock.append(product)

        db.update_category(category) # /!\ deve atualizar a categoria sempre antes de inserir o produto

        db.update_stock(self.__stock)

        return 0 # sucesso

    '''
        Retorna a lista de produtos no estoque
    '''
    def fetch_product_names(self):
        self.__stock = db.fetch_stock()

        if not self.__stock:
            return []
        else:
            return [product.name for product in self.__stock]
        
    '''
        Retorna a lista de categorias disponíveis
    '''
    def fetch_product_categories(self):
        return db.fetch_categories()
        # retorna a lista de categorias disponíveis ([] se vazia ou em caso de erro)

    '''
        Consulta o produto no Inventário
    '''
    def confer_product(self, product_name):
        self.__stock = db.fetch_stock()

        if not self.__stock:
            return None
        else:
            for product in self.__stock:
                if product.name == product_name:
                    return product
                
            return None

    '''
        Atualiza o produto no estoque

        Retorna...
            0 - Sucesso;
            1 - Sem alterações;
            2 - Produto não encontrado.
    '''
    def update_product(self, product_name, product_category, product_cost, product_price, product_qty):
        # correção de campos vazios
        if not product_cost:
            product_cost = 0.0
        if not product_price:
            product_price = 0.0
        if not product_qty:
            product_qty = ''

        self.__stock = db.fetch_stock()

        for product in self.__stock:
            if product.name == product_name:
                if product_category == '' and float(product_cost) == product.cost and float(product_price) == product.price and int(product_qty) == product.qty:
                    return 1 # sem alterações
                else:
                    if product_category != '':
                        product.category = product_category
                    if product_cost != 0.0:
                        product.cost = float(product_cost)
                    if product_price != 0.0:
                        product.price = float(product_price)
                    if product_qty != '':
                        product.qty = int(product_qty)

                db.update_stock(self.__stock)

                return 0
            
        return 2 # produto não encontrado

    '''
        Remove o produto do estoque

        Retorna...
            0 - Sucesso;
            1 - Produto não encontrado.
    '''
    def delete_product(self, product_name):
        self.__stock = db.fetch_stock()

        for product in self.__stock:
            if product.name == product_name:
                self.__stock.remove(product)

                db.update_stock(self.__stock)

                return 0

        return 1

class EntryModel:
    def __init__(self):
        self.__stock = []

    def fetch_product_names(self):
        self.__stock = db.fetch_stock()

        if not self.__stock:
            return []
        else:
            return [product.name for product in self.__stock]
        
    '''
        Registra a entrada/saída do produto no Inventário

        Retorna...
            0 - Sucesso;
            1 - Produto não encontrado.
    '''
    def entry_product(self, product_name, entry_qty):
        self.__stock = db.fetch_stock()

        for product in self.__stock:
            if product.name == product_name:
                curr_qty = product.qty
                curr_qty += int(entry_qty)
                product.qty = curr_qty

                db.update_stock(self.__stock)

                return 0

        return 1
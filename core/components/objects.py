class Product:
    def __init__(self, i, n, c, p, q):
        self.__id = i
        self.__category = None
        self.__name = n
        self.__cost = c
        self.__price = p
        self.__qty = q

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, i):
        self.__id = i

    @property
    def category(self):
        return self.__category
    
    @category.setter
    def category(self, c):
        self.__category = c

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, n):
        self.__name = n

    @property
    def cost(self):
        return self.__cost
    
    @cost.setter
    def cost(self, c):
        self.__cost = c

    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, p):
        self.__price = p

    @property
    def qty(self):
        return self.__qty
    
    @qty.setter
    def qty(self, q):
        self.__qty = q
    
class Sale:
    def __init__(self, p, q, v):
        self.__product_id = p
        self.__qty = q
        self.__value = v

    @property
    def product_id(self):
        return self.__product_id
    
    @product_id.setter
    def product_id(self, p):
        self.__product_id = p

    @property
    def qty(self):
        return self.__qty
    
    @qty.setter
    def qty(self, q):
        self.__qty = q

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, v):
        self.__value = v

class Order:
    def __init__(self, t):
        self.__timestamp = t
        self.__sales = []
        self.__value = 0.0

    @property
    def timestamp(self):
        return self.__timestamp
    
    @timestamp.setter
    def timestamp(self, t):
        self.__timestamp = t

    @property
    def sales(self):
        return self.__sales
    
    @sales.setter
    def sales(self, S):
        self.__sales = S

    def append_sale(self, s):
        self.__sales.append(s)

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, v):
        self.__value = v
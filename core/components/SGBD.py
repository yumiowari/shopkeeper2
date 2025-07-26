import pickle as pkl
import os

### STOCK
def fetch_stock():
    if os.path.isfile('data/stock.pkl'):
        with open('data/stock.pkl', 'rb') as file:
            try:
                return pkl.load(file)
            except EOFError:
                return []
    else:
        return []

def update_stock(items):
    with open('data/stock.pkl', 'wb') as file:
        pkl.dump(items, file)
###

### CURRENT SALE
def fetch_curr_sale():
    if os.path.isfile('data/curr_sale.pkl'):
        with open('data/curr_sale.pkl', 'rb') as file:
            try:
                return pkl.load(file)
            except EOFError:
                return []
    else:
        return []
    
def update_curr_sale(curr_sale):
    with open('data/curr_sale.pkl', 'wb') as file:
        pkl.dump(curr_sale, file)

def delete_curr_sale():
    if os.path.isfile('data/curr_sale.pkl'):
        os.remove('data/curr_sale.pkl')
###

### COMMITED SALE
def store_comm_sale(comm_sale):
    path = 'data/' + comm_sale['timestamp']

    os.makedirs(path, exist_ok=True)

    path += '/sale.pkl'

    with open(path, 'wb') as file:
        pkl.dump(comm_sale, file)
###
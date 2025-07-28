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

def update_stock(stock):
    with open('data/stock.pkl', 'wb') as file:
        pkl.dump(stock, file)
###

### CURRENT ORDER
def fetch_curr_order():
    if os.path.isfile('data/order.pkl'):
        with open('data/order.pkl', 'rb') as file:
            try:
                return pkl.load(file)
            except EOFError:
                return []
    else:
        return []
    
def update_curr_order(order):
    with open('data/order.pkl', 'wb') as file:
        pkl.dump(order, file)

def delete_curr_order():
    if os.path.isfile('data/order.pkl'):
        os.remove('data/order.pkl')
###

### COMMITED ORDER
def store_comm_order(order):
    path = 'data/' + order['timestamp']

    os.makedirs(path, exist_ok=True)

    path += '/order.pkl'

    with open(path, 'wb') as file:
        pkl.dump(order, file)
###
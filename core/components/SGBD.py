import pickle as pkl
'''
    O módulo pickle em Python permite serializar e desserializar objetos Python,
    transformando-os em uma sequência de bytes que pode ser armazenada em um arquivo.
'''

import os
'''
    os provê uma forma portátil de usar operações dependentes do sistema operacional.
'''

from dotenv import load_dotenv
'''
    load_dotenv carrega variáveis de ambiente definidas em um arquivo .env para o ambiente do sistema.
'''

import psycopg
'''
    psycopg é o adaptador oficial do PostgreSQL para Python, permitindo conectar e executar comandos SQL no banco de dados.
'''

from core.components.objects import *
'''
    Importa as definições dos objetos de dados.
'''

import bcrypt
'''
    bcrypt é uma biblioteca para gerar e verificar hashes seguros de senhas, protegendo contra ataques de força bruta e vazamentos de dados.
'''

# carrega as variáveis do arquivo env
load_dotenv()
db_name     = os.getenv('DB_NAME')
db_user     = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host     = os.getenv('DB_HOST')

'''
    Inventário
'''
def fetch_stock():
    #if os.path.isfile('data/stock.pkl'):
    #    with open('data/stock.pkl', 'rb') as file:
    #        try:
    #            return pkl.load(file)
    #        except EOFError:
    #            return []
    #else:
    #    return []

    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT id, category_id, name, cost, price, qty FROM "Product"')
            rows = cursor.fetchall()

            stock = []
            for row in rows:
                id, category_id, name, cost, price, qty = row

                product = Product(id, name, cost, price, qty)

                cursor.execute('SELECT name FROM "Category" WHERE id = %s', (category_id,))
                category = (cursor.fetchone() or [None])[0]
                product.category = category

                stock.append(product)

            return stock


def update_stock(stock):
    #with open('data/stock.pkl', 'wb') as file:
    #    pkl.dump(stock, file)

    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as connection:
        with connection.cursor() as cursor:
            # busca todos os IDs atuais do banco
            cursor.execute('SELECT id FROM "Product"')
            db_ids = {row[0] for row in cursor.fetchall()}

            # extrai os IDs dos produtos atuais do objeto
            current_ids = {product.id for product in stock if product.id is not None}

            # descobre quais devem ser removidos (presentes no banco, mas não no objeto)
            to_remove = db_ids - current_ids

            # remove os produtos que não estão mais no estoque
            for product_id in to_remove:
                cursor.execute('DELETE FROM "Product" WHERE id = %s', (product_id,))

            for product in stock:
                cursor.execute('SELECT id FROM "Category" WHERE name = %s', (product.category,))
                category_id = (cursor.fetchone() or [None])[0]

                cursor.execute(
                    '''
                        INSERT INTO "Product" (id, name, category_id, cost, price, qty)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id)
                        DO UPDATE SET
                            category_id = EXCLUDED.category_id,
                            cost = EXCLUDED.cost,
                            price = EXCLUDED.price,
                            qty = EXCLUDED.qty
                    ''',
                    (product.id, product.name, category_id, product.cost, product.price, product.qty)
                )

'''
    Comandas
'''
def commit_order(order):
    #path = 'data/' + order.timestamp
    #
    #os.makedirs(path, exist_ok=True)
    #
    #path += '/order.pkl'
    #
    #with open(path, 'wb') as file:
    #    pkl.dump(order, file)

    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as connection:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO "Order" (timestamp, value) VALUES (%s, %s) RETURNING id', (order.timestamp, order.value))
            order_id = (cursor.fetchone() or [None])[0]

            for sale in order.sales:
                cursor.execute(
                    'INSERT INTO "Sale" (order_id, product_id, qty, value) VALUES (%s, %s, %s, %s)',
                    (order_id, sale.product_id, sale.qty, sale.value)    
                )

def fetch_order(timestamp):
    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT id, value FROM "Order" WHERE timestamp = %s', (timestamp,))
            order_row = cursor.fetchone()
            if not order_row:
                return None

            order_id, order_value = order_row
            order = Order(timestamp)
            order.value = order_value

            cursor.execute('SELECT product_id, qty, value FROM "Sale" WHERE order_id = %s', (order_id,))
            sales_rows = cursor.fetchall()
            for product_id, qty, value in sales_rows:
                sale = Sale(product_id, qty, value)
                order.append_sale(sale)

            return order
        
def fetch_order_list(selected_date):
    query_orders = '''
        SELECT id, timestamp, value
        FROM "Order"
        WHERE timestamp LIKE %s
        ORDER BY timestamp ASC;
    '''
    # ordena as orders pelo timestamp: "ORDER BY timestamp ASC"

    query_sales = '''
        SELECT product_id, qty, value
        FROM "Sale"
        WHERE order_id = %s;
    '''

    # converte a data para o padrão usado nos registros
    date_pattern = f'{selected_date.strftime('%Y-%m-%d')}%'

    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as connection:
        with connection.cursor() as cursor:
            comm_orders = []

            # busca as comandas referentes a data informada
            cursor.execute(query_orders, (date_pattern,))
            orders = cursor.fetchall()

            for order_id, timestamp, total_value in orders:
                order_obj = Order(timestamp)
                order_obj.value = total_value

                # busca as vendas associadas
                cursor.execute(query_sales, (order_id,))
                sales = cursor.fetchall()

                for product_id, qty, value in sales:
                    sale_obj = Sale(product_id, qty, value)
                    order_obj.append_sale(sale_obj)

                comm_orders.append(order_obj)

    return comm_orders

'''
    Autenticação
'''
def update_credentials(credentials):
    #with open('data/credentials.pkl', 'wb') as file:
    #    pkl.dump(credentials, file)

    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as connection:
        with connection.cursor() as cursor:
            hashed_password = bcrypt.hashpw(credentials['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            cursor.execute('INSERT INTO "User" (name, password) VALUES (%s, %s)', (credentials['username'], hashed_password))

def fetch_credentials():
    #with open('data/credentials.pkl', 'rb') as file:
    #    return pkl.load(file)

    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT name, password FROM "User"')

            rows = cursor.fetchall()

            users = []
            for row in rows:
                username, password = row

                users.append({'username': username, 'password': password})

            return users
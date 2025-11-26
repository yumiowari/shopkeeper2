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

def fetch_categories():
    try:
        with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT name FROM "Category"')
                rows = cursor.fetchall()

                # extrái apenas os nomes das tuplas retornadas
                categories = [row[0] for row in rows]

                return categories

    except Exception as e:
        print(f"Erro ao buscar as categorias: {e}")

        return []
    
def fetch_product_map():
    """
        Retorna um dicionário com os produtos agrupados por categoria:
        {
            'Categoria 1': ['Produto A', 'Produto B', ...],
            'Categoria 2': ['Produto C', 'Produto D', ...],
            ...
        }
    """
    query = """
                SELECT c.name AS category_name, p.name AS product_name
                FROM "Product" p
                JOIN "Category" c ON p.category_id = c.id
                ORDER BY c.name, p.name;
            """

    product_map = {}

    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            for category_name, product_name in rows:
                if category_name not in product_map:
                    product_map[category_name] = []
                product_map[category_name].append(product_name)

    return product_map

def update_category(name):
    try:
        with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO "Category" (name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING
                    """,
                    (name,)
                )
                connection.commit()
                return True
    except Exception as e:
        print(f"Erro ao garantir a categoria: {e}")

        return False

'''
    Comandas
'''
def commit_order(order):
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

def fetch_order_report(selected_date):
    date_pattern = f"{selected_date.strftime('%Y-%m-%d')}%"

    report = {
        'revenue': 0.0,
        'profit': 0.0
    }

    with psycopg.connect(
        f'dbname={db_name} user={db_user} password={db_password} host={db_host}'
    ) as connection:
        with connection.cursor() as cursor:

            # Receita
            cursor.execute(
                '''
                SELECT COALESCE(SUM(value), 0)
                FROM "Order"
                WHERE timestamp LIKE %s
                ''',
                (date_pattern,)
            )
            row = cursor.fetchone()
            revenue = row[0] if row else 0.0
            report['revenue'] = float(revenue)

            # Lucro
            cursor.execute(
                '''
                SELECT 
                    s.qty,
                    p.cost,
                    p.price
                FROM "Sale" s
                JOIN "Product" p ON p.id = s.product_id
                JOIN "Order" o ON o.id = s.order_id
                WHERE o.timestamp LIKE %s
                ''',
                (date_pattern,)
            )

            rows = cursor.fetchall() or []

            for qty, cost, price in rows:
                report['profit'] += (float(price) - float(cost)) * int(qty)

    return report

def undo_specific_order(selected_timestamp):
    try:
        with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as connection:
            with connection.cursor() as cursor:
                # 0. Descobrir o ID da comanda a partir do timestamp
                cursor.execute(
                    '''
                    SELECT id 
                    FROM "Order"
                    WHERE timestamp = %s
                    ''',
                    (selected_timestamp,)
                )
                row = cursor.fetchone()

                if not row:
                    return False  # comanda inexistente

                order_id = row[0]

                # 1. Buscar vendas associadas
                cursor.execute(
                    '''
                    SELECT product_id, qty
                    FROM "Sale"
                    WHERE order_id = %s
                    ''',
                    (order_id,)
                )
                sales = cursor.fetchall() or []

                if not sales:
                    return False  # sem vendas não tem o que desfazer

                # 2. Repor o estoque de acordo
                for product_id, qty in sales:
                    cursor.execute(
                        '''
                        UPDATE "Product"
                        SET qty = qty + %s
                        WHERE id = %s
                        ''',
                        (qty, product_id)
                    )

                # 3. Remover vendas associadas
                cursor.execute(
                    '''
                    DELETE FROM "Sale"
                    WHERE order_id = %s
                    ''',
                    (order_id,)
                )

                # 4. Remover comanda
                cursor.execute(
                    '''
                    DELETE FROM "Order"
                    WHERE id = %s
                    ''',
                    (order_id,)
                )

        return True

    except Exception:
        return False


'''
    Autenticação
'''
def update_credentials(credentials):
    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as connection:
        with connection.cursor() as cursor:
            hashed_password = bcrypt.hashpw(credentials['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            cursor.execute('INSERT INTO "User" (name, email, password) VALUES (%s, %s, %s)', (credentials['username'], credentials['email'], hashed_password))

def fetch_credentials():
    with psycopg.connect(f'dbname={db_name} user={db_user} password={db_password} host={db_host}') as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT name, password FROM "User"')

            rows = cursor.fetchall()

            users = []
            for row in rows:
                username, password = row

                users.append({'username': username, 'password': password})

            return users
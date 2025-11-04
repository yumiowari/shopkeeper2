CREATE TABLE IF NOT EXISTS "User"
(
    id SERIAL PRIMARY KEY,

    name     TEXT UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Category"
(
    id SERIAL PRIMARY KEY,

    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Product"
(
    id          INTEGER PRIMARY KEY,
    category_id INTEGER,

    name  TEXT UNIQUE,
    cost  FLOAT NOT NULL,
    price FLOAT NOT NULL,
    qty   INTEGER DEFAULT 0,

    FOREIGN KEY (category_id)
        REFERENCES "Category" (id)
);

CREATE TABLE IF NOT EXISTS "Order"
(
    id SERIAL PRIMARY KEY,

    timestamp TEXT NOT NULL,
    value     FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Sale"
(
    id       SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,

    product_id INTEGER NOT NULL,
    qty        INTEGER NOT NULL,
    value      FLOAT NOT NULL,

    FOREIGN KEY (order_id)
        REFERENCES "Order" (id),
    FOREIGN KEY (product_id)
        REFERENCES "Product" (id)
);
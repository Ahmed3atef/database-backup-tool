-- PostgreSQL Dummy Data: Online Shop
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    country VARCHAR(50),
    joined_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(80),
    price NUMERIC(10, 2) NOT NULL,
    stock INT DEFAULT 0
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers (id),
    product_id INT REFERENCES products (id),
    quantity INT NOT NULL,
    total NUMERIC(10, 2),
    ordered_at TIMESTAMP DEFAULT NOW()
);

-- Customers
INSERT INTO
    customers (name, email, country)
VALUES (
        'Alice Johnson',
        'alice@example.com',
        'USA'
    ),
    (
        'Bob Smith',
        'bob@example.com',
        'UK'
    ),
    (
        'Carlos Ruiz',
        'carlos@example.com',
        'Spain'
    ),
    (
        'Diana Prince',
        'diana@example.com',
        'France'
    ),
    (
        'Evan Zhao',
        'evan@example.com',
        'China'
    );

-- Products
INSERT INTO
    products (name, category, price, stock)
VALUES (
        'Laptop Pro 15',
        'Electronics',
        1299.99,
        50
    ),
    (
        'Wireless Mouse',
        'Accessories',
        29.99,
        200
    ),
    (
        'Mechanical Keyboard',
        'Accessories',
        89.99,
        150
    ),
    (
        '4K Monitor',
        'Electronics',
        399.99,
        80
    ),
    (
        'USB-C Hub',
        'Accessories',
        49.99,
        300
    );

-- Orders
INSERT INTO
    orders (
        customer_id,
        product_id,
        quantity,
        total
    )
VALUES (1, 1, 1, 1299.99),
    (1, 2, 2, 59.98),
    (2, 3, 1, 89.99),
    (3, 4, 1, 399.99),
    (4, 5, 3, 149.97),
    (5, 1, 2, 2599.98),
    (2, 2, 1, 29.99);

\echo '✅ PostgreSQL: shop_db loaded with customers, products, orders'
-- MySQL Dummy Data: Inventory System
USE inventory_db;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    name VARCHAR(150) NOT NULL,
    sku VARCHAR(50) UNIQUE,
    quantity INT DEFAULT 0,
    unit_price DECIMAL(10, 2),
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

CREATE TABLE warehouses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(200)
);

CREATE TABLE stock_movements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT,
    warehouse_id INT,
    movement ENUM('IN', 'OUT') NOT NULL,
    quantity INT,
    moved_at DATETIME DEFAULT NOW(),
    FOREIGN KEY (item_id) REFERENCES items (id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses (id)
);

-- Categories
INSERT INTO
    categories (name)
VALUES ('Raw Materials'),
    ('Finished Goods'),
    ('Packaging'),
    ('Spare Parts');

-- Warehouses
INSERT INTO
    warehouses (name, location)
VALUES ('Main Warehouse', 'Cairo, EG'),
    ('North Hub', 'Alexandria, EG'),
    ('South Depot', 'Aswan, EG');

-- Items
INSERT INTO
    items (
        category_id,
        name,
        sku,
        quantity,
        unit_price
    )
VALUES (
        1,
        'Steel Rod 6m',
        'RM-001',
        500,
        12.50
    ),
    (
        1,
        'Copper Wire 1kg',
        'RM-002',
        300,
        18.75
    ),
    (
        2,
        'Widget Type A',
        'FG-001',
        1000,
        5.99
    ),
    (
        2,
        'Gadget Pro',
        'FG-002',
        250,
        45.00
    ),
    (
        3,
        'Cardboard Box L',
        'PK-001',
        2000,
        0.75
    ),
    (
        4,
        'Bearing 6203',
        'SP-001',
        150,
        3.20
    );

-- Movements
INSERT INTO
    stock_movements (
        item_id,
        warehouse_id,
        movement,
        quantity
    )
VALUES (1, 1, 'IN', 200),
    (2, 1, 'IN', 100),
    (3, 2, 'IN', 500),
    (3, 2, 'OUT', 50),
    (4, 3, 'IN', 100),
    (5, 1, 'IN', 1000),
    (6, 2, 'IN', 80);

SELECT 'MySQL: inventory_db loaded ✅' AS status;
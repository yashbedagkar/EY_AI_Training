CREATE DATABASE supply_chain_db;
use supply_chain_db;

CREATE TABLE products (
    ProductID VARCHAR(10) PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    UnitPrice DECIMAL(10, 2)
);

CREATE TABLE warehouses (
    WarehouseID VARCHAR(10) PRIMARY KEY,
    Location VARCHAR(100),
    Capacity INT
);

INSERT INTO products (ProductID, ProductName, Category, UnitPrice) VALUES
('P101', 'Laptop', 'Electronics', 800),
('P102', 'Mouse', 'Accessories', 20),
('P103', 'Keyboard', 'Accessories', 35),
('P104', 'Monitor', 'Electronics', 150),
('P105', 'Router', 'Networking', 90);

INSERT INTO warehouses (WarehouseID, Location, Capacity) VALUES
('W01', 'Mumbai', 1000),
('W02', 'Delhi', 800),
('W03', 'Chennai', 500);

-- CRUD Operations

-- Add a new product
INSERT INTO products (ProductID, ProductName, Category, UnitPrice)
VALUES ('P106', 'Webcam', 'Accessories', 60);

--  Update warehouse capacity
UPDATE warehouses
SET Capacity = 900
WHERE WarehouseID = 'W02';

-- Delete a product 
DELETE FROM products
WHERE ProductID = 'P102';

-- Fetch all products in Electronics category
SELECT * FROM products
WHERE Category = 'Electronics';


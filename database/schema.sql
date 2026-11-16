CREATE DATABASE IF NOT EXISTS tlucafe_db
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

DROP TABLE IF EXISTS order_details;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('admin', 'staff') NOT NULL DEFAULT 'staff'
);

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category_id INT,
    product_type ENUM('homemade', 'packaged') NOT NULL DEFAULT 'homemade',
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT NULL,
    status TINYINT(1) NOT NULL DEFAULT 1,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(12, 2) NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE order_details (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE SET NULL
);

-- SEED DATA

INSERT INTO users (username, password, full_name, role) VALUES
('admin', '123456', 'QL-Vũ', 'admin'),
('staff', '123456', 'Nguyễn Minh Vũ', 'staff');

INSERT INTO categories (category_name) VALUES
('Đồ uống'),
('Đồ ăn'),
('Đồ ăn vặt'),
('Nước ngọt đóng chai');

INSERT INTO products (product_name, category_id, product_type, price, stock_quantity, status) VALUES
('Cà phê Đen đá', 1, 'homemade', 20000, NULL, 1),
('Trà Đào Cam Sả', 1, 'homemade', 25000, NULL, 1),
('Phở Bò Tái Chín', 2, 'homemade', 35000, NULL, 1),
('Bún Chả Hà Nội', 2, 'homemade', 30000, NULL, 0),
('Cơm Đùi gà', 2, 'homemade', 30000, NULL, 1);

INSERT INTO products (product_name, category_id, product_type, price, stock_quantity, status) VALUES
('Bim bim Oishi Tôm Cay', 3, 'packaged', 10000, 25, 1),
('Snack Khoai Tây Lay''s', 3, 'packaged', 15000, 12, 1),
('Coca-Cola Chai 390ml', 4, 'packaged', 15000, 30, 1),
('Nước Tăng Lực Sting Dâu', 4, 'packaged', 15000, 5, 1),
('Trà Xanh Không Độ', 4, 'packaged', 15000, 0, 0);

INSERT INTO orders (user_id, order_date, total_amount) VALUES
(1, DATE_SUB(NOW(), INTERVAL 2 DAY), 95000),
(2, DATE_SUB(NOW(), INTERVAL 1 DAY), 115000),
(2, NOW(), 85000);

INSERT INTO order_details (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 25000), -- 1 Cà phê Nâu Đá
(1, 3, 1, 45000), -- 1 Phở Bò
(1, 6, 1, 10000), -- 1 Bim bim Oishi
(1, 8, 1, 15000), -- 1 Coca-Cola
(2, 2, 2, 35000), -- 2 Trà Đào
(2, 7, 3, 15000), -- 3 Snack Lay's
(3, 4, 1, 40000), -- 1 Bún Chả
(3, 9, 3, 15000); -- 3 Sting Dâu
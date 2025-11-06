DROP DATABASE IF EXISTS car_agency;
CREATE DATABASE car_agency;

USE car_agency;
CREATE TABLE customers(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(100)
    );

USE car_agency;
CREATE TABLE vehicles(
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INT,
    price DECIMAL(10,2)
    );

USE car_agency;
CREATE TABLE sales(
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    date_sale TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
    );

USE car_agency;
INSERT INTO customers(name, email, phone, address) VALUES('Henrique Cantin', 'henrique.cantin@gmail.com', '11940401212', 'Rua Brasil, SN'),
('Lucca Bento', 'luccabento@gmail.com', '11987654321', 'Avenida Paulista, 1000'),
('Natalia Silva', 'nati.s@outlook.com', '11912345678', 'Rua das Flores, 50'),
('Maria Julia', 'maju@hotmail.com', '11923456789', 'Alameda Santos, 200'),
('Leonardo Dantas', 'dantas@outlook.com', '11945698787', 'Av Campo Limpo, 50');

USE car_agency;
INSERT INTO sales (customer_id, vehicle_id, price) VALUES
(1, 4, 42000.00),
(2, 1, 50000.00),
(3, 3, 75000.00);

USE car_agency;
INSERT INTO vehicles (brand, model, year, color, price) VALUES
('Honda', 'Civic', 2005, 'Prata', 50000.00),
('Toyota', 'Corolla', 2010, 'Preto', 42000.00),
('Ford', 'Focus', 2014, 'Branco', 75000.00),
('BMW', '320i', 2018, 'Azul', 120000.00);
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `vehicles` (
    `id` int(11) NOT NULL,
    `brand` varchar(50) NOT NULL,
    `model` varchar(100) NOT NULL,
    `year` int(11) DEFAULT NULL,
    `color` varchar(50) NOT NULL
    `price` decimal(10,2) DEFAULT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `vehicles` (`id`, `brand`, `model`, `year`, `color`, `price`) VALUES
('Honda', 'Civic', 2005, 'Prata', 50000.00),
('Toyota', 'Corolla', 2010, 'Preto', 42000.00),
('Ford', 'Focus', 2014, 'Branco', 75000.00),
('BMW', '320i', 2018, 'Azul', 120000.00);

ALTER TABLE `vehicles`
ADD PRIMARY KEY (`id`);

ALTER TABLE `vehicles`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;
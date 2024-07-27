CREATE DATABASE IF NOT EXISTS `aes_params`;
CREATE DATABASE IF NOT EXISTS `aes_bkt`;

-- create root user and grant rights
-- CREATE USER 'aes'@'localhost' IDENTIFIED WITH mysql_native_password BY 'abc123';
CREATE USER 'aes'@'localhost' IDENTIFIED WITH mysql_native_password BY 'abc123';
GRANT ALL PRIVILEGES ON *.* TO 'aes'@'%';

-- CREATE USER 'root'@'localhost' IDENTIFIED BY 'local';
-- GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
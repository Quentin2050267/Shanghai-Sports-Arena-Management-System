CREATE DATABASE IF NOT EXISTS sports_facility_management;

USE sports_facility_management;

DROP TABLE IF EXISTS reservation;
DROP TABLE IF EXISTS time_slot;
DROP TABLE IF EXISTS facility;
DROP TABLE IF EXISTS gym;
DROP TABLE IF EXISTS user;

CREATE TABLE gym (
  gym_id INT AUTO_INCREMENT PRIMARY KEY,
  gym_district VARCHAR(50) NOT NULL DEFAULT '',
  gym_name VARCHAR(255) NOT NULL,
  gym_address VARCHAR(255) NOT NULL
);

CREATE TABLE facility (
  facility_id INT AUTO_INCREMENT PRIMARY KEY,
  facility_name VARCHAR(255) NOT NULL,
  gym_id INT,
  FOREIGN KEY (gym_id) REFERENCES gym(gym_id)
);

CREATE TABLE user (
  user_id VARCHAR(255) PRIMARY KEY,
  user_name VARCHAR(255) NOT NULL,
  user_email VARCHAR(255) NOT NULL,
  user_phone VARCHAR(255) NOT NULL,
  user_password VARCHAR(255) NOT NULL,
  user_type ENUM('admin', 'user') DEFAULT 'user'
);

CREATE TABLE reservation (
  reservation_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(255),
  facility_id INT,
  schedule_date DATE NOT NULL,
  schedule_time VARCHAR(255) NOT NULL,
  reservation_date DATE NOT NULL,
  status INT NOT NULL DEFAULT 1,
  FOREIGN KEY (user_id) REFERENCES user(user_id),
  FOREIGN KEY (facility_id) REFERENCES facility(facility_id)
);

CREATE TABLE time_slot (
    time_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    facility_id INT NOT NULL,
    FOREIGN KEY (facility_id) REFERENCES facility(facility_id)
);

-- 插入一个管理员，可以按需修改 -- 
INSERT INTO user (user_id, user_name, user_password, user_email, user_phone, user_type) 
VALUES ('2050267', 'Quentin', 'Ab123456','2315902845@qq.com', '13816643095', 'admin');

-- 插入一个普通用户，可以按需修改 -- 
INSERT INTO user (user_id, user_name, user_email, user_phone, user_password) 
VALUES ('1234567', '水果榨汁', '2315902845@qq.com', '13816643095', 'Ab123456');
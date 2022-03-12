CREATE DATABASE IF NOT EXISTS `pythonlogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pythonlogin`;

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS `users`;
SET foreign_key_checks = 1;
CREATE TABLE IF NOT EXISTS `users` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
	`birth_date` DATE,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `uc_user` UNIQUE (`id`, `username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `users` (`id`, `username`, `password`, `email`) VALUES (1, 'test', 'test', 'test@test.com');
INSERT INTO `users` (`username`, `password`, `email`) VALUES ('jason', 'password', 'jasonjzhang17@gmail.com');

CREATE TABLE IF NOT EXISTS `user_metrics` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`user_id` int(11) NOT NULL,
	`weight` FLOAT,
	`squat` FLOAT,
	`bench` FLOAT,
	`deadlift` FLOAT,
  	`date` DATE DEFAULT (CURRENT_DATE),
    PRIMARY KEY (`id`),
    CONSTRAINT fk_user
    FOREIGN KEY (`user_id`) 
    REFERENCES users(`id`)
        ON UPDATE CASCADE
        ON DELETE CASCADE  
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
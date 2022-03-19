CREATE DATABASE IF NOT EXISTS `pythonlogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pythonlogin`;

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS `users`;
SET foreign_key_checks = 1;
CREATE TABLE IF NOT EXISTS `users` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
	`sex` TINYINT(1) NOT NULL,
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

SET SQL_SAFE_UPDATES = 0;
DELETE FROM user_metrics;
SET SQL_SAFE_UPDATES = 1;
ALTER TABLE `user_metrics` AUTO_INCREMENT = 1;
INSERT INTO `user_metrics` (`user_id`, `weight`, `squat`, `bench`, `deadlift`, `date`) VALUES (1, 1, 400, 1, 1, '2022-3-12');
INSERT INTO `user_metrics` (`user_id`, `weight`, `squat`, `bench`, `deadlift`, `date`) VALUES (1, 2, 200, 1, 1, '2022-3-11');
INSERT INTO `user_metrics` (`user_id`, `weight`, `squat`, `bench`, `deadlift`, `date`) VALUES (1, 3, 123, 1, 1, '2022-3-10');
INSERT INTO `user_metrics` (`user_id`, `weight`, `squat`, `bench`, `deadlift`, `date`) VALUES (1, 4, 120, 1, 1, '2022-3-9');
INSERT INTO `user_metrics` (`user_id`, `weight`, `squat`, `bench`, `deadlift`, `date`) VALUES (1, 1, 100, 1, 1, '2022-3-8');
INSERT INTO `user_metrics` (`user_id`, `weight`, `squat`, `bench`, `deadlift`, `date`) VALUES (1, 2, 111, 1, 1, '2022-3-7');
INSERT INTO `user_metrics` (`user_id`, `weight`, `squat`, `bench`, `deadlift`, `date`) VALUES (1, 3, 110, 1, 1, '2022-3-6');
INSERT INTO `user_metrics` (`user_id`, `weight`, `squat`, `bench`, `deadlift`, `date`) VALUES (1, 4, 105, 1, 1, '2022-3-5');
INSERT INTO `user_metrics` (`user_id`, `weight`, `squat`, `bench`, `deadlift`, `date`) VALUES (1, 4, 100, 1, 1, '2022-3-4');
INSERT INTO `user_metrics` (`user_id`, `weight`, `squat`, `bench`, `deadlift`, `date`) VALUES (1, 1, 20, 1, 1, '2022-3-3');
INSERT INTO `user_metrics` (`user_id`, `weight`, `squat`, `bench`, `deadlift`, `date`) VALUES (1, 2, 5, 1, 1, '2022-3-2');
INSERT INTO `user_metrics` (`user_id`, `weight`, `squat`, `bench`, `deadlift`, `date`) VALUES (1, 3, 1, 1, 1, '2022-3-1');

ALTER TABLE `user_metrics` ADD INDEX `idx_user_id` (`user_id`);
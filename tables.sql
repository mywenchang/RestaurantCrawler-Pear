CREATE TABLE IF NOT EXISTS `restaurant`(
	`id` INT(11) UNSIGNED AUTO_INCREMENT,
	`restaurant_id` INT(11) UNSIGNED,
	`name` VARCHAR(50) NOT NULL,
	`source` TINYINT,
	`sales` INT(11)	UNSIGNED,
	`arrive_time` INT(4) UNSIGNED,
	`start_fee` FLOAT UNSIGNED,
	`send_fee` FLOAT UNSIGNED,
	`score` FLOAT UNSIGNED,
	`latitude` VARCHAR(20),
	`longitude` VARCHAR(20),
	PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
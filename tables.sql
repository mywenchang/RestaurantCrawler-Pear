DROP TABLE IF EXISTS `restaurant`;
CREATE TABLE `restaurant` (
	`id` INT(11) UNSIGNED AUTO_INCREMENT,
	`restaurant_id` INT(11) UNSIGNED,
	`name` VARCHAR(50) DEFAULT NULL,
	`source` TINYINT,
	`sales` INT(11) UNSIGNED,
	`arrive_time` INT(4) UNSIGNED,
	`start_fee` FLOAT UNSIGNED DEFAULT 0,
	`send_fee` FLOAT UNSIGNED DEFAULT 0,
	`score` FLOAT UNSIGNED DEFAULT 0,
	`latitude` VARCHAR(20),
	`longitude` VARCHAR(20),
	PRIMARY KEY (`id`),
	KEY `idx_restaurant_id` (`restaurant_id`)
) ENGINE = InnoDB CHARSET = utf8;

DROP TABLE IF EXISTS `dish`;
CREATE TABLE `dish` (
	`id` INT(11) UNSIGNED AUTO_INCREMENT,
	`restaurant_id` INT(11) UNSIGNED,
	`name` VARCHAR(50)  DEFAULT NULL,
	`rating` FLOAT UNSIGNED  DEFAULT 0,
	`moth_sales` INT(11) UNSIGNED DEFAULT 0,
	`rating_count` INT(11) UNSIGNED  DEFAULT 0,
	PRIMARY KEY (`id`),
	KEY `idx_restaurant_id` (`restaurant_id`)
) ENGINE = InnoDB CHARSET = utf8;

DROP TABLE IF EXISTS `crawler`;
CREATE TABLE `crawler` (
	`id` INT(11) UNSIGNED AUTO_INCREMENT,
	`status` TINYINT DEFAULT 0,
	`created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	`finished` TIMESTAMP NULL DEFAULT NULL,
	`args` TEXT,
	`info` TEXT,
	`extras` TEXT,
	`data_count` INT(11) UNSIGNED DEFAULT 0,
	`total` INT(11) UNSIGNED DEFAULT 0,
	PRIMARY KEY (`id`)
) ENGINE = InnoDB CHARSET = utf8;
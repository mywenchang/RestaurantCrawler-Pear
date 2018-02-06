DROP TABLE IF EXISTS `restaurant`;
CREATE TABLE `restaurant` (
	`id` INT(11) UNSIGNED AUTO_INCREMENT,
	`restaurant_id` INT(11) UNSIGNED COMMENT '商家id，来自数据源',
	`name` VARCHAR(100) DEFAULT NULL COMMENT '商家名称',
	`source` TINYINT(1) COMMENT '数据来源',
	`sales` INT(11) UNSIGNED COMMENT '销量',
	`arrive_time` INT(4) UNSIGNED COMMENT '平均到达时间',
	`start_fee` FLOAT UNSIGNED DEFAULT 0 COMMENT '起送费',
	`send_fee` FLOAT UNSIGNED DEFAULT 0 COMMENT '配送费',
	`score` FLOAT UNSIGNED DEFAULT 0 COMMENT '评分',
	`latitude` VARCHAR(20),
	`longitude` VARCHAR(20),
	PRIMARY KEY (`id`),
	KEY `idx_restaurant_id` (`restaurant_id`)
) ENGINE = InnoDB CHARSET = utf8;

DROP TABLE IF EXISTS `dish`;
CREATE TABLE `dish` (
	`id` INT(11) UNSIGNED AUTO_INCREMENT,
	`restaurant_id` INT(11) UNSIGNED COMMENT 'restaurant 表中的 id',
	`name` VARCHAR(100)  DEFAULT NULL COMMENT '菜品名称',
	`rating` FLOAT UNSIGNED  DEFAULT 0 COMMENT '评价',
	`moth_sales` INT(11) UNSIGNED DEFAULT 0 COMMENT '月销量',
	`rating_count` INT(11) UNSIGNED  DEFAULT 0 COMMENT '评价数',
	PRIMARY KEY (`id`),
	KEY `idx_restaurant_id` (`restaurant_id`)
) ENGINE = InnoDB CHARSET = utf8;

DROP TABLE IF EXISTS `crawler`;
CREATE TABLE `crawler` (
	`id` INT(11) UNSIGNED AUTO_INCREMENT,
	`status` TINYINT(1) DEFAULT 0 COMMENT '任务执行的状态',
	`created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	`finished` TIMESTAMP NULL DEFAULT NULL,
	`args` TEXT COMMENT '任务的参数',
	`info` TEXT,
	`extras` TEXT,
	`data_count` INT(11) UNSIGNED DEFAULT 0 COMMENT '当前获取到的数据量',
	`total` INT(11) UNSIGNED DEFAULT 0 COMMENT '总数据量',
	PRIMARY KEY (`id`)
) ENGINE = InnoDB CHARSET = utf8;
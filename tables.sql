CREATE TABLE IF NOT EXISTS `restaurant` (
  `id`            INT(11) UNSIGNED AUTO_INCREMENT,
  `restaurant_id` INT(11) UNSIGNED,
  `name`          VARCHAR(50) NOT NULL,
  `source`        TINYINT,
  `sales`         INT(11) UNSIGNED,
  `arrive_time`   INT(4) UNSIGNED,
  `start_fee`     FLOAT UNSIGNED,
  `send_fee`      FLOAT UNSIGNED,
  `score`         FLOAT UNSIGNED,
  `latitude`      VARCHAR(20),
  `longitude`     VARCHAR(20),
  PRIMARY KEY (`id`),
  KEY `idx_restaurant_id` (`restaurant_id`)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE IF NOT EXISTS `dish` (
  `id`            INT(11) UNSIGNED AUTO_INCREMENT,
  `restaurant_id` INT(11) UNSIGNED,
  `name`          VARCHAR(50) NOT NULL,
  `rating`        FLOAT UNSIGNED,
  `moth_sales`    INT(11) UNSIGNED,
  `rating_count`  INT(11) UNSIGNED,
  PRIMARY KEY (`id`),
  KEY `idx_restaurant_id` (`restaurant_id`)
)ENGINE = InnoDB DEFAULT CHARSET = utf8;
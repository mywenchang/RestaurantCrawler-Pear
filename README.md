# 项目结构

http服务:handlers
爬虫服务:crawlers

* GET（SELECT）：从服务器取出资源（一项或多项）。
* POST（CREATE）：在服务器新建一个资源。
* PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
* PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
* DELETE（DELETE）：从服务器删除资源。
* HEAD：获取资源的元数据。
* OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。

## 各方法例子
* GET /zoos：列出所有动物园
* POST /zoos：新建一个动物园
* GET /zoos/ID：获取某个指定动物园的信息
* PUT /zoos/ID：更新某个指定动物园的信息（提供该动物园的全部信息）
* PATCH /zoos/ID：更新某个指定动物园的信息（提供该动物园的部分信息）
* DELETE /zoos/ID：删除某个动物园
* GET /zoos/ID/animals：列出某个指定动物园的所有动物
* DELETE /zoos/ID/animals/ID：删除某个指定动物园的指定动物

## 商家表
```sql
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
```

## 菜品表
```sql
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
```

### 爬虫表
```sql
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
```

## API

```json
//爬取饿了么成都大学附近的商家信息
{
  "action": "create",
  "type": "restaurant",
  "source": "ele",
  "extras": {
    "latitude": "35.12412",
    "longitude": "104.129401"
   }
}
```

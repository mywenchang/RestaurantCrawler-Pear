[![Build Status](https://travis-ci.org/jiyangg/Pear.svg?branch=master)](https://travis-ci.org/jiyangg/Pear)

[前端展示 http://spider.youcute.cn](http://spider.youcute.cn)

# 项目结构
|模块名|文件目录|说明|
|:---:|:---:|:---:|
|http服务|web|包含API接口具体实现，基于 Flask Web框架|
|爬虫实现|crawlers|爬虫的具体实现|
|爬虫任务执行|jobs|基于消息队列(beanstalkd)的任务调度|
|数据操作|models|对数据库的 CRUD 操作实现, 基于 Sqlalchemy |

# HTTP 方法说明

* GET（SELECT）：从服务器取出资源（一项或多项）。
* POST（CREATE）：在服务器新建一个资源。
* PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
* PATCH（UPDATE）：在服务器局部更新资源（客户端提供改变的属性）。
* DELETE（DELETE）：从服务器删除资源。
* HEAD：获取资源的元数据。
* OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。

# 接口实现

- [x] 登录注册 `/auth/login` `auth/signup`
- [x] 需要登录的接口，使用装饰器添加验证
- [x] 登录饿了么
- [x] 饿了么商家爬虫
- [x] 饿了么商家菜品爬虫
- [x] 饿了么商家评论爬虫
- [x] 饿了么数据分析
- [ ] 美团外卖数据爬取


# Api

- 登录注册 `auth/login` `auth/signup` POST

----

- 获取饿了么登录短信验证码 `config_ele_crawler/sms_code` GET
- 登录饿了么 `config_ele_crawler/login_ele` GET
- 搜索饿了么地点 `config_ele_crawler/search_address` GET
- 获取饿了么商家 `config_ele_crawler/get_restaurants` GET

---

- 提交爬虫任务 `crawler/task` POST
- 获取所有爬虫任务 `crawler/task` GET
- 获取单条爬虫任务 `crawler/task/<int:crawler_id>` GET
- 删除任务 `crawler/task/<int:crawler_id>` DELETE
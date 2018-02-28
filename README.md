# 环境要求

* python 2.X
* 系统依赖
    * zc.buildout
    * beanstalkd
    * mysql

# 项目结构
|模块名|文件目录|说明|
|:---:|:---:|:---:|
|http服务|web|包含API接口具体实现，基于 Flask Web框架|
|爬虫实现|crawlers|爬虫的具体实现|
|爬虫任务执行|jobs|基于消息队列(beanstalkd)的任务调度|
|数据操作|models|对数据库的 CRUD 操作实现, 基于 Sqlalchemy |

# HTTP 接口说明

* GET（SELECT）：从服务器取出资源（一项或多项）。
* POST（CREATE）：在服务器新建一个资源。
* PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
* PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
* DELETE（DELETE）：从服务器删除资源。
* HEAD：获取资源的元数据。
* OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。

## 详细接口

### 爬虫

#### 获取可用爬虫

GET `crawlers/configs`

> 返回所有可用的爬虫配置信息

```json
{
    "data": [
        {
            "args": [
                "headers",
                "cookies"
            ],
            "type": "restaurant",
            "name": "饿了么商家",
            "source": "ele"
        },
        {
            "args": [
                "headers",
                "cookies"
            ],
            "type": "dish",
            "name": "饿了么商家菜品",
            "source": "ele"
        },
        {
            "args": [
                "headers",
                "cookies"
            ],
            "type": "restaurant",
            "name": "美团商家",
            "source": "meituan"
        }
    ],
    "total": 3
}
```
#### 执行一个爬虫任务

POST `/crawlers`

参数:

|参数名|类型|说明|必须|
|:-:|:-:|:-:|:-:|
|source|String|`crawlers/configs`接口返回|是|
|type|String|`crawlers/configs`接口返回|是|
|args|String|常用 HTTP 头信息, headers、cookies 等|否|

#### 修改一个爬虫任务

PATCH `crawlers/<crawler_id>`

参数:

|参数名|类型|说明|必须|
|:-:|:-:|:-:|:-:|

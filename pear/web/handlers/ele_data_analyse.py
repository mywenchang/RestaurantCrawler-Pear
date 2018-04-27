# coding=utf-8
from flask import Blueprint, jsonify, url_for, request

from pear.models.crawler import CrawlerDao
from pear.models.dish import EleDishDao
from pear.models.rate import EleRateDao
from pear.models.restaurant import EleRestaurantDao
from pear.utils.split_words import generator_cloud

data_router = Blueprint('analyse', __name__, url_prefix='/analyse')

__RestaurantDaoS = {
    1: EleRestaurantDao
}


@data_router.route('/compare_all')
def compare_all():
    u_id = request.cookies.get('u_id')
    crawlers, _ = CrawlerDao.batch_get_by_status(u_id, page=-1)
    data = {}
    for item in crawlers:
        restaurant = item['restaurant']
        if not restaurant:
            continue
        data.setdefault(restaurant['name'], {})
        data[restaurant['name']] = {
            'sales': restaurant['sales'],
            'score': restaurant['score'],
            'send_fee': restaurant['send_fee'],
            'arrive_time': restaurant['arrive_time'],
            'dish_total': len(item['dishes'])
        }

    return jsonify(data)


# 获取店铺
@data_router.route('/restaurant/<int:source>/<int:restaurant_id>')
def get_restaurant(source, restaurant_id):
    Dao = __RestaurantDaoS.get(source)
    restaurant = None
    if Dao:
        restaurant = Dao.get_by_restaurant_id(restaurant_id)
    return jsonify(restaurant)


# 分布
@data_router.route('/dish_distribution/<int:crawler_id>')
def sale_distribution(crawler_id):
    dish, _ = EleDishDao.get_by_crawler_id(crawler_id, page=-1)

    def render_item(k):
        return sorted([
            {
                'food_id': item['food_id'],
                'food_name': item['name'],
                'value': item[k]
            }
            for item in dish],
            key=lambda d: d['value'],
            reverse=True)

    # 销量分布
    sales = render_item('moth_sales')
    # 评分分布
    rate_dis = render_item('rating')
    # 销量随价格的分布
    price_dis = {}
    for item in dish:
        price = item['price']
        price_dis.setdefault(price, 0)
        sale = item['moth_sales']
        price_dis[price] += sale
    price_dis = sorted([{'name': k, 'value': v} for k, v in price_dis.items()], key=lambda d: d['name'])

    # 店铺评论数随时间分布
    rate, _ = EleRateDao.get_by_crawler_id(crawler_id, page=-1)
    rate_date_dis = {}
    for item in rate:
        rate_at = item['rated_at']
        rate_date_dis.setdefault(rate_at, 0)
        rate_date_dis[rate_at] += 1

    return jsonify({
        'sales_dis': sales,
        'rate_dis': rate_dis,
        'price_dis': price_dis,
        'rate_date_dis': rate_date_dis
    })


# 词云
@data_router.route('/rating_word_cloud/<int:crawler_id>')
def rating_cloud(crawler_id):
    rate, _ = EleRateDao.get_by_crawler_id(crawler_id, page=-1)
    food_rates = {}
    restaurant_id = 0
    for item in rate:
        restaurant_id = item['restaurant_id']
        food_id = item['food_id']
        food_rate = item['food_rate']
        food_rates.setdefault(food_id, [])
        food_rates[food_id].append(food_rate)
        # 所有评论的词云
    texts = ''.join([''.join(v) for v in food_rates.values()])
    total_image = generator_cloud(texts, '{}-{}'.format(crawler_id, restaurant_id))
    return jsonify({
        'total_image': url_for('static', filename=total_image)
    })


@data_router.route('/compare/<int:crawler_one>/<int:crawler_two>')
def compare(crawler_one, crawler_two):
    u_id = request.cookies.get('u_id')
    dish_1, _ = EleDishDao.get_by_crawler_id(crawler_one, page=-1)
    dish_2, _ = EleDishDao.get_by_crawler_id(crawler_two, page=-1)
    crawler_1 = CrawlerDao.get_by_id(crawler_one, u_id)
    crawler_2 = CrawlerDao.get_by_id(crawler_two, u_id)
    # 同价位商品销量比较
    sales_compare_with_same_price = {}
    # 同价位商品评价比较
    rate_compare_with_same_price = {}
    price_set = set()
    max_sale = 0
    for item in dish_1:
        price = item['price']
        price_set.add(price)
    for item in dish_2:
        price = item['price']
        price_set.add(price)

    for item in dish_1:
        price = item['price']
        sale = item['moth_sales']
        rate = item['rating']
        if sale > max_sale:
            max_sale = sale
        sales_compare_with_same_price.setdefault('a', {})
        sales_compare_with_same_price['a'][price] = sale
        rate_compare_with_same_price.setdefault('a', {})
        rate_compare_with_same_price['a'][price] = rate

    for item in dish_2:
        price = item['price']
        sale = item['moth_sales']
        rate = item['rating']
        if sale > max_sale:
            max_sale = sale
        sales_compare_with_same_price.setdefault('b', {})
        sales_compare_with_same_price['b'][price] = sale
        rate_compare_with_same_price.setdefault('b', {})
        rate_compare_with_same_price['b'][price] = rate

    for p in price_set:
        sales_compare_with_same_price['a'].setdefault(p, 0)
        sales_compare_with_same_price['b'].setdefault(p, 0)
        rate_compare_with_same_price['a'].setdefault(p, 0)
        rate_compare_with_same_price['b'].setdefault(p, 0)

    def sort_price(items):
        return sorted([{'price': k, 'value': v} for k, v in items.iteritems()], key=lambda d: d['price'])

    a_sales = sort_price(sales_compare_with_same_price['a'])
    b_sales = sort_price(sales_compare_with_same_price['b'])

    a_rate = sort_price(rate_compare_with_same_price['a'])
    b_rate = sort_price(rate_compare_with_same_price['b'])

    return jsonify({
        'crawler_1': crawler_1,
        'crawler_2': crawler_2,
        'sales_compare_with_same_price': {
            'a': a_sales,
            'b': b_sales,
            'max': max_sale
        },
        'rate_compare_with_same_price': {
            'a': a_rate,
            'b': b_rate
        },
        'other': []
    })

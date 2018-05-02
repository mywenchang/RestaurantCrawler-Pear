# coding=utf-8
import json

from flask import Blueprint, jsonify, url_for, request

from pear.models.analyse_task import AnalyseTaskDao
from pear.models.crawler import CrawlerDao
from pear.models.rate import RateDao
from pear.models.user_log import UserLogDao
from pear.utils.const import AnalyTaskType
from pear.utils.split_words import generator_cloud
from pear.web.controllers import analy_task_controller
from pear.web.utils.authorize import authorize

data_router = Blueprint('analyse', __name__, url_prefix='/analyse')


# 获取店铺数据分布
@data_router.route('/dish_distribution/<int:crawler_id>')
@authorize
def sale_distribution(crawler_id):
    u_id = request.cookies.get('u_id')
    data = AnalyseTaskDao.get_by_u_id(u_id, crawler_one=crawler_id, _type=AnalyTaskType.SINGLE)
    if data:
        return jsonify(data['data'])
    UserLogDao.create(u_id, u'获取店铺商品数据分布')
    crawler = CrawlerDao.get_by_id(crawler_id, u_id)
    dishes = crawler['dishes']

    def render_item(k):
        return sorted([
            {
                'food_id': item['food_id'],
                'food_name': item['name'],
                'value': item[k]
            }
            for item in dishes],
            key=lambda d: d['value'],
            reverse=True)

    # 销量分布
    sales = render_item('moth_sales')
    # 评分分布
    rate_dis = render_item('rating')
    # 销量随价格的分布
    price_dis = {}
    for item in dishes:
        price = item['price']
        price_dis.setdefault(price, 0)
        sale = item['moth_sales']
        price_dis[price] += sale
    price_dis = sorted([{'name': k, 'value': v} for k, v in price_dis.items()], key=lambda d: d['name'])

    # 店铺评论数随时间分布
    rate, _ = RateDao.get_by_crawler_id(crawler_id, page=-1)
    rate_date_dis = {}
    for item in rate:
        rate_at = item['rated_at']
        rate_date_dis.setdefault(rate_at, 0)
        rate_date_dis[rate_at] += 1
    data = {
        'restaurant': crawler['restaurant'],
        'sales_dis': sales,
        'rate_dis': rate_dis,
        'price_dis': price_dis,
        'rate_date_dis': rate_date_dis
    }
    analy_task_controller.save_analyse_data.put(u_id=u_id, data=json.dumps(data), crawler_one=crawler_id,
                                                _type=AnalyTaskType.SINGLE)
    return jsonify(data)


# 词云
@data_router.route('/rating_word_cloud/<int:crawler_id>')
@authorize
def rating_cloud(crawler_id):
    rate, _ = RateDao.get_by_crawler_id(crawler_id, page=-1)
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
    return jsonify({'total_image': url_for('static', filename=total_image, _external=True) if total_image else None})


# 比较两家店
@data_router.route('/compare/<int:crawler_one>/<int:crawler_two>')
@authorize
def compare(crawler_one, crawler_two):
    u_id = request.cookies.get('u_id')
    data = AnalyseTaskDao.get_by_u_id(u_id, crawler_one=crawler_one, crawler_two=crawler_two, _type=AnalyTaskType.MULTI)
    if data:
        return jsonify(data['data'])
    crawler_1 = CrawlerDao.get_by_id(crawler_one, u_id)
    crawler_2 = CrawlerDao.get_by_id(crawler_two, u_id)
    if not crawler_1 or not crawler_2:
        return jsonify({'message': u'爬虫不存在'}), 401
    UserLogDao.create(u_id, action_name=u'比较两家店',
                      action_args=u'{} vs {}'.format(crawler_1['restaurant']['name'], crawler_2['restaurant']['name']))
    dish_1 = crawler_1['dishes']
    dish_2 = crawler_2['dishes']
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
    data = {
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
    }
    analy_task_controller.save_analyse_data.put(u_id=u_id, data=json.dumps(data), crawler_one=crawler_one,
                                                crawler_two=crawler_two, _type=AnalyTaskType.MULTI)
    return jsonify(data)


# 获取用户历史数据分析
@data_router.route('/history')
@data_router.route('/history/<int:analyse_type>')
@authorize
def history(analyse_type=None):
    u_id = request.cookies.get('u_id')
    data, _ = AnalyseTaskDao.batch_get_by_u_id(u_id, _type=analyse_type)
    return jsonify({
        'data': data
    })

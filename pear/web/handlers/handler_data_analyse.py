# coding=utf-8
from flask import Blueprint
from flask import jsonify
from flask.app import request

from pear.models.dish import EleDishDao
from pear.models.rate import EleRateDao

data_router = Blueprint('analyse', __name__, url_prefix='/analyse')


# 店铺单品分布
@data_router.route('/dish_distribution/<int:crawler_id>/<int:restaurant_id>')
def sale_distribution(crawler_id, restaurant_id):
    dish, total = EleDishDao.get_by_crawler_id(crawler_id, page=-1)

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
    rate = render_item('rating')
    # 评价数分布
    rate_count = render_item('rating_count')
    # 价格分布
    price_dis = render_item('price')
    return jsonify({
        'sales_dis': sales,
        'rate_dis': rate,
        'rate_count_dis': rate_count,
        'price_dis': price_dis
    })


# 店铺评论数时间分布
@data_router.route('/rating_distribution/<int:crawler_id>/<int:restaurant_id>')
def restaurant_rating_distribution(crawler_id, restaurant_id):
    rate, total = EleRateDao.get_by_restaurant_id(crawler_id, restaurant_id, page=-1)
    data = {}
    for item in rate:
        rate_at = item['rated_at']
        data.setdefault(rate_at, 0)
        data[rate_at] += 1
    return jsonify(data)


# 店铺评论得分分布
@data_router.route('/rating_score_distribution/<int:crawler_id>/<int:restaurant_id>')
def rating_score_distribution(crawler_id, restaurant_id):
    rate, total = EleRateDao.get_by_restaurant_id(crawler_id, restaurant_id, page=-1)
    data = {}
    for item in rate:
        rate = item['food_star']
        data.setdefault(rate, 0)
        data[rate] += 1
    return jsonify(data)

# coding=utf-8
from flask import Blueprint
from flask import jsonify
from flask.app import request

from pear.models.dish import DishDao
from pear.models.rate import RateDao

data_router = Blueprint('analyse', __name__, url_prefix='/analyse')


# 店铺单品分布
@data_router.route('/dish_distribution/<int:crawler_id>')
def sale_distribution(crawler_id):
    dish, total = DishDao.get_by_crawler_id(crawler_id, page=-1)

    def render_item(k):
        return sorted([
            {
                'food_id': item['food_id'],
                'food_name': item['name'],
                'value': item[k]
            }
            for item in dish], key=lambda d: d['value'])

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


# 店铺总评论分布
@data_router.route('/rating_distribution')
def restaurant_rating_distribution():
    restaurant_id = request.args.get('restaurant_id')
    crawler_id = request.args.get('crawler_id')
    rate = RateDao.get_by_restaurant_id(crawler_id, restaurant_id, page=-1)
    return jsonify(data=rate)

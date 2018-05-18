# coding=utf-8
from flask import jsonify

from pear.crawlers import CRAWLER_TYPES
from pear.crawlers.crawler_ele import CrawlEleDishes
from pear.jobs.job_queue import JobQueue
from pear.models.restaurant import RestaurantDao


@JobQueue.task('crawlers')
def save_ele_restaurants(restaurant_id, name, source, sales=0, arrive_time=0, send_fee=0, score=0, latitude=None,
                         longitude=None, image=None):
    restaurant = RestaurantDao.get_by_restaurant_id(restaurant_id)
    if restaurant:
        RestaurantDao.update_by_restaurant_id(restaurant_id, name=name, source=source, sales=sales,
                                              arrive_time=arrive_time, send_fee=send_fee, score=score,
                                              latitude=latitude, longitude=longitude, image=image)
    else:
        RestaurantDao.create(restaurant_id, name, source, sales, arrive_time, send_fee, score, latitude, longitude,
                             image)


@JobQueue.task('crawlers')
def commit_ele_crawler_task(cookies, args):
    crawler = CrawlEleDishes(CRAWLER_TYPES['ele_crawler'], cookies, args)
    crawler.crawl()


def __create_ele(request):
    try:
        cookies = request.cookies
        data_list = request.json
        for data in data_list:
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            if not data.get('restaurant') or not latitude or not longitude:
                return jsonify(success=False), 404
            args = {
                'restaurant': {
                    'id': data.get('restaurant').get('id'),
                    'latitude': data.get('restaurant').get('latitude'),
                    'longitude': data.get('restaurant').get('longitude'),
                },
                'latitude': latitude,
                'longitude': longitude
            }
            commit_ele_crawler_task.put(cookies=cookies, args=args)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=e.message.__str__()), 500


create_crawler_funcs = {
    'ele': __create_ele
}

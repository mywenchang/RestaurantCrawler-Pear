# coding=utf-8

import os

import jieba
import jieba.posseg as posseg
import matplotlib.pyplot as plt
import time
from wordcloud import WordCloud

from pear.utils.logger import logger

NOT_WANT_CHAR = [',', '.', '?', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', ';', ':', '"', '[', ']', '{',
                 '}', '`', u'，', u'。', u'？', '\\', '|']

PATH = 'pear/web/static'


def generator_cloud(text, name=int(time.time())):
    """
    :param name: 文件名
    :param text: 目标生成词云的文本
    :return:
    """
    name = 'word_cloud_images/{}.png'.format(name)
    path = os.path.join(os.path.abspath(PATH), name)
    if os.path.exists(path):
        return name
    # 分词
    word_list_after_jieba = jieba.cut(text)
    # 去重
    wl_space_split = " ".join(word_list_after_jieba)
    if not wl_space_split:
        return None
    # 生成词云
    try:
        my_word_cloud = WordCloud(font_path='etc/font.ttf',
                                  width=800,
                                  height=600,
                                  max_words=2000,
                                  background_color='white',
                                  margin=5).generate(wl_space_split)
        plt.imshow(my_word_cloud)
        plt.imshow(my_word_cloud)
        plt.axis("off")
        plt.savefig(path, dpi=200)
    except Exception as e:
        logger.error('name:{} text:{}'.format(name, text))
        logger.error(e, exc_info=True)
    finally:
        return name

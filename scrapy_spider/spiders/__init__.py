# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy

from scrapy_spider import settings
from selenium import webdriver


def mk_ping_pong_request(callback):
    return scrapy.Request(url='http://www.baidu.com', callback=callback)


def mk_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('lang=zh-CN.UTF-8')
    options.add_argument(f'user-agent={settings.USER_AGENT}')
    prefs = {
        'profile.managed_default_content_settings.images': 2,
        'profile.managed_default_content_settings.notifications': 2,
        'intl.accept_languages': 'zh-CN,zh;q=0.9,en;q=0.5',
    }
    options.add_experimental_option('prefs', prefs)
    return options


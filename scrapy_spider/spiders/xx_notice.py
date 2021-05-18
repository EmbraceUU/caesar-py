import hashlib
import urllib.parse
import scrapy
import datetime
from selenium import webdriver
from lxml import etree
from scrapy_spider.spiders import mk_ping_pong_request, mk_chrome_options

DATA_SOURCE = "ExchangeName"
ALLOW_DOMAINS = "https://xx.zendesk.com"
BASEURL = "https://xx.zendesk.com/hc/zh-cn/categories/"
NAME = "xx_notice"


class NoticeSpider(scrapy.Spider):
    # spider name
    name = NAME

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowd_domains = ALLOW_DOMAINS
        self.options = mk_chrome_options()
        self.browser = webdriver.Chrome(chrome_options=self.options)

    def start_requests(self):
        yield mk_ping_pong_request(self.parse_ping_pong)

    def parse_ping_pong(self, response):
        base_url = BASEURL
        self.browser.get(base_url)
        content = self.browser.page_source
        content = etree.HTML(content)

        try:
            result = content.xpath("//div[@id='main-content']/section/ul")[0]
            re2 = result.xpath('./li')
            article_list = []
            for item in re2:
                article_url = urllib.parse.urljoin(self.allowd_domains, item.xpath('./a/@href')[0])
                article_title = item.xpath("./a/text()")[0]

                hash_id = str(hashlib.sha1((article_title + article_url).encode("gbk")).hexdigest())
                print(article_url, article_title, hash_id)

                article_list.append({
                    'url': article_url,
                    'title': article_title,
                    'hash': hash_id
                })
        except BaseException:
            raise BaseException
        finally:
            self.close2()

        for item in article_list:
            yield self.article_detail(item.get('url'), item.get('hash'))

    def article_detail(self, article_url, hash_id):
        self.browser = webdriver.Chrome(chrome_options=self.options)
        self.browser.get(article_url)
        article_data = etree.HTML(self.browser.page_source)

        try:
            title = article_data.xpath("//h1[@class='article-title']/text()")[0]
            author = article_data.xpath("//div[@class='article-meta']/text()")[0]
            content = article_data.xpath("//div[@class='article-content']")[0]
            content2 = etree.tostring(content, method='xml', encoding="utf-8").decode("utf-8")
            release_time = datetime.datetime.strptime(
                article_data.xpath("//li[@class='meta-data']/time/@datetime")[0], "%Y-%m-%dT%H:%M:%SZ")
            author = author.replace('\n', '').strip(' ')
            title = title.replace('\n', '').strip(' ')
            content2 = content2.replace("src=\"", "src=\"{}".format(self.allowd_domains))

            print({
                'url': article_url,
                'author': author,
                'content': content2,
                'release_time': release_time,
                'title': title,
                'plate': '公告',
                'source': DATA_SOURCE,
                'tags': '',
                'hash_id': hash_id
            })
        except BaseException:
            raise BaseException
        finally:
            self.close2()

    def close(self, reason):
        pass

    def close2(self):
        self.browser.stop_client()
        self.browser.close()
        self.browser.quit()


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl(NoticeSpider)
    process.start()

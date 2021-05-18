import scrapy
import datetime
import hashlib
import urllib.parse

from scrapy_spider.items import SpiderItem


class PublicSpider(scrapy.Spider):
    name = "public_notice"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, response):
        pass

    def start_requests(self):
        url = 'https://xxx.zendesk.com/hc/zh-cn/categories'
        allowed_domains = 'https://xxx.zendesk.com'
        small_plate = ''
        source = ''

        yield scrapy.Request(url=url, callback=self.parse_plate_all,
                             meta={"allowed_domains": allowed_domains, "small_plate": small_plate,
                                   "source": source}, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/68.0"})

    def parse_plate_all(self, response):
        result = response.xpath("//section[@class='section']") if response.meta[
                                                                      "small_plate"] in "all" else response.xpath(
            "//section[position()<={}]".format(response.meta["small_plate"]))

        for i in result:
            plate_name = i.xpath("./h3/a/text()").extract_first()
            for z in i.xpath("./ul/li"):
                article_url = urllib.parse.urljoin(response.meta["allowed_domains"],
                                                   z.xpath("./a/@href").extract_first())
                hash = hashlib.sha1((article_url + plate_name).encode("gbk"))
                hash_id = str(hash.hexdigest())
                hash_ids = 0
                if hash_ids == 0:
                    yield scrapy.Request(url=article_url, meta={"allowed_domains": response.meta["allowed_domains"],
                                                                'plate_name': plate_name, 'article_url': article_url,
                                                                'hash_id': hash_id, "source": response.meta["source"]},
                                         callback=self.article_detail, dont_filter=True, headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/68.0"})

    def article_detail(self, response):

        title = response.xpath("normalize-space(//header/h1)").extract_first()
        author = response.xpath(
            "normalize-space(//div[@class='article-meta']/a/text())").extract_first() if response.xpath(
            "normalize-space(//div[@class='article-meta']/text())").extract_first() in '' else response.xpath(
            "normalize-space(//div[@class='article-meta']/text())").extract_first()
        author = author.replace("\n", "")
        release_time = datetime.datetime.strptime(response.xpath("//time/@title").extract_first(), "%Y-%m-%dT%H:%M:%SZ")
        content = response.xpath("//div[@class='article-content']/div").extract_first().replace("'", "").replace(
            "src=\"", "src=\"{}".format(response.meta["allowed_domains"])).replace("data-src=\"",
                                                                                   "data-src=\"{}".format(response.meta[
                                                                                                              "allowed_domains"]))

        yield SpiderItem({
            'url': urllib.parse.unquote(response.meta['article_url']),
            'author': author,
            'content': content,
            'release_time': release_time,
            'title': title,
            'plate': response.meta['plate_name'],
            'source': response.meta['source'],
            'tags': '',
            'hash_id': response.meta['hash_id']
        })


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl(PublicSpider)
    process.start()

import scrapy


class StandingsSpider(scrapy.Spider):
    name = "standings"
    allowed_domains = ["www.espn.ph"]
    start_urls = ["https://www.espn.ph/"]

    def parse(self, response):
        pass

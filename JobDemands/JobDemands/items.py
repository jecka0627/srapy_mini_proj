# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    employment_type = scrapy.Field()
    category = scrapy.Field()
    job_category = scrapy.Field()
    office_address = scrapy.Field()
    industry = scrapy.Field()
    vacancy = scrapy.Field()
    company_site = scrapy.Field()
    # spider_source = scrapy.Field()
    
import scrapy
from JobDemands.items import JobsItem


def classify_job(title: str) -> str:
    if not title:
        return "Unknown"

    title = title.lower()

    it_keywords = [
        "developer", "ui/ux", "programmer", "software", "support", "engineer"
        "data", "it", "cyber", "security", "network", "qa", "graphic"
        "full stack", "frontend", "backend", "web", "designer",
        "python", "java", "sql", "cloud", "devops", "system",
        "mobile", "android", "ios", "analyst", "machine learning"
    ]

    return "IT" if any(word in title for word in it_keywords) else "NON-IT"


class JobscloudSpider(scrapy.Spider):
    name = "jobscloud"
    allowed_domains = ["jobscloud.net"]
    start_urls = ["https://www.jobscloud.net/"]
    

    def parse(self, response):
        jobs = response.css("tr.rowmodal")

        for job in jobs:
            job_url = job.css("td[data-title='Title'] a::attr(href)").get()

            if job_url:
                job_url = response.urljoin(job_url)

                yield scrapy.Request(
                    job_url,
                    callback=self.parse_job
                )


    def parse_job(self, response):
        item = JobsItem()

    
        item["title"] = response.css("td h3::text").get()
        item["company"] = response.xpath("//td[b[text()='Company Information']]/following-sibling::td//b/text()").get()

        location_parts = response.xpath("//td[b[text()='Job Location']]/following-sibling::td//text()").getall()
        item["location"] = " ".join([x.strip() for x in location_parts if x.strip()])

        item["employment_type"] = response.xpath( "//td[b[text()='Job Type']]/following-sibling::td//span/text()").get()
        item["category"] = response.xpath("//td[b[text()='Job Industry']]/following-sibling::td//span/text()").get()
        item["job_category"] = classify_job(item["title"])
        
        address_parts = response.xpath("//td[b[text()='Job Location']]/following-sibling::td//text()").getall()
        item["office_address"] = " ".join([x.strip() for x in address_parts if x.strip()])
        
        item["industry"] = response.xpath("//td[b[text()='Job Industry']]/following-sibling::td//span/text()").get()
        
        vacancy_parts = response.xpath("//td[b[normalize-space()='Number of Job Opening']]/following-sibling::td[1]//text()").getall()
        item["vacancy"] = " ".join([x.strip() for x in vacancy_parts if x.strip()]) or None
        
        item["company_site"] = None #not available

        yield item
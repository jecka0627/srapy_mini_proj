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


class KalibrrSpider(scrapy.Spider):
    name = "kalibrr"
    allowed_domains = ["kalibrr.com"]

    start_urls = ["https://www.kalibrr.com/kjs/job_board/search?limit=15&offset=0"]

    def parse(self, response):
        data = response.json()
        for job in data.get("jobs", []):
            yield self.parse_job(job)

        # pagination - for the load more button
        if data.get("jobs"):
            current_offset = int(response.url.split("offset=")[-1])
            next_url = f"https://www.kalibrr.com/kjs/job_board/search?limit=15&offset={current_offset + 15}"
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_job(self, job):
        company = job.get("company") or {}
        company_info = job.get("company_info") or {}
        location = job.get("google_location", {}).get("address_components", {})

        item = JobsItem()
        item["title"] = job.get("name")
        item["company"] = job.get("company_name") or company.get("name")
        item["location"] = location.get("city") or location.get("region")
        item["employment_type"] = job.get("tenure")
        item["category"] = job.get("function")
        item["job_category"] = classify_job(item["title"])
        item["office_address"] = self.full_address(location)
        item["industry"] = company.get("industry") or company_info.get("industry")
        item["vacancy"] = self.vacancy(job)
        item["company_site"] = company_info.get("url")

        return item

    def full_address(self, location):
        parts = [
            location.get("address_line_1"),
            location.get("city"),
            location.get("region"),
            location.get("country"),
        ]
        return ", ".join(part for part in parts if part) or None

    def vacancy(self, job):
        openings = job.get("number_of_openings")
        if openings is not None:
            return openings
        return None

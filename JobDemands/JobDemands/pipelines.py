# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector



class MySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@Jedidah0627!'
        )

        self.cur = self.conn.cursor()
        self.cur.execute("CREATE DATABASE IF NOT EXISTS job_demands")
        self.conn.database = 'job_demands'

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs(
            id int NOT NULL auto_increment,
            title text,
            company VARCHAR(255),
            location text,
            employment_type VARCHAR(50),
            category VARCHAR(100),
            job_category VARCHAR(100),
            office_address text,
            industry VARCHAR(100),
            vacancy VARCHAR(50),
            company_site VARCHAR(255),
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.cur.execute("""INSERT INTO jobs(
            title, company, location, employment_type, category, job_category, office_address, industry, vacancy, company_site) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                    adapter.get("title"),
                    adapter.get("company"),
                    adapter.get("location"),
                    adapter.get("employment_type"),
                    adapter.get("category"),
                    adapter.get("job_category"),
                    adapter.get("office_address"),
                    adapter.get("industry"),
                    adapter.get("vacancy"),
                    adapter.get("company_site")
                ))
        
        
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
                
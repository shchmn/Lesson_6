# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongobase = client.vacancy1804

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salaryhh(item['salary'])
            del item['salary']
            pass
        else:
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salarysj(item['salary'])
            del item['salary']
            pass
        return item

        collection = self.mongobase[spider.name]
        collection.insert_one(item)

    def process_salaryhh(self, salary):
        if salary is None:
            min_salary = None
            max_salary = None
            currency = None
        elif 'от ' in salary[0] and 'до ' in salary[2]:
            min_salary = int(salary[1].replace('\xa0', '').replace('\u202f', ''))
            max_salary = int(salary[3].replace('\xa0', '').replace('\u202f', ''))
            currency = salary[5]
        elif 'от ' in salary[0]:
            min_salary = int(salary[1].replace('\xa0', '').replace('\u202f', ''))
            max_salary = None
            currency = salary[3]
        elif 'до ' in salary[0]:
            min_salary = None
            max_salary = int(salary[1].replace('\xa0', '').replace('\u202f', ''))
            currency = salary[3]

        return min_salary, max_salary, currency

    def process_salarysj(self, salary):
        if salary is None:
            min_salary = None
            max_salary = None
            currency = None
        elif 'от' and 'до' not in salary:
            min_salary = None
            max_salary = None
            currency = None
        elif 'от' in salary and 'до' in salary:
            min_salary = int(salary[1].replace('\xa0', '').replace('\u202f', ''))
            max_salary = int(salary[3].replace('\xa0', '').replace('\u202f', ''))
            currency = salary[5]
        elif 'от' in salary and 'до' not in salary:
            min_salary = int(salary[1].replace('\xa0', '').replace('\u202f', ''))
            max_salary = None
            currency = salary[3]
        elif 'до' in salary and 'от' not in salary:
            min_salary = None
            max_salary = int(salary[1].replace('\xa0', '').replace('\u202f', ''))
            currency = salary[3]

        return min_salary, max_salary, currency

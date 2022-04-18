import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/rabota-v-hr.html?geo%5Bt%5D%5B0%5D=4',
                  'https://spb.superjob.ru/vakansii/rabota-v-hr.html']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class,'f-test-button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[contains(@class,'f-test-vacancy-item')]//@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//span[@class='_2eYAG -gENC _1TcZY dAWx1']//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)


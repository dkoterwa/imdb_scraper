import scrapy
from imdb_scraper.items import ImdbScraperItem
import json, re, requests
import time

class ImdbSpider(scrapy.Spider):
    name = "imdbSpider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/"]

    def convertDurationToMinute(self, duration):
        duration = str(duration)[2:]
        duration_split = re.split("[HM]", duration)
        return (int(duration_split[0]) * 60) + int(duration_split[1])

    def parse_movie_details(self, response):
        item = response.meta["item"]
        data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())
        item["genre"] = data["genre"][0]
        item["date_published"] = data["datePublished"]
        item["duration"] = self.convertDurationToMinute(data["duration"])
        return item

    def parse(self, response):
        start_time = time.time()
        movies = response.xpath("//tbody[@class='lister-list']/tr")
        data_count = 250
        i = 0

        for movie in movies:
            item = ImdbScraperItem()
            if i == data_count:
                break
            i = i + 1
            movie_link = movie.xpath(".//td[@class='titleColumn']/a/@href").get()
            movie_url = response.urljoin(movie_link)
            final_item =  scrapy.Request(movie_url, callback=self.parse_movie_details, meta={"item": item}, priority=data_count-i)
            item["no"] = i
            item["title"] = movie.xpath(".//td[@class='titleColumn']/a/text()").get()
            item["rating"] = movie.xpath(".//td[@class='ratingColumn imdbRating']/strong/text()").get()

            yield final_item



        finish_time = time.time()
        execution_time = finish_time - start_time
        print(f"Execution time: {execution_time} seconds")



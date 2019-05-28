import scrapy


class QuotesSpider(scrapy.Spider):
    name = "FDATA"

    def start_requests(self):
        urls = [
            'https://www.flipkart.com/search?q=mobiles&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_0_0&otracker1=AS_Query_TrendingAutoSuggest_0_0&as-pos=0&as-type=HISTORY&as-backfill=on&page=2',
            'https://www.flipkart.com/search?q=mobiles&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_0_0&otracker1=AS_Query_TrendingAutoSuggest_0_0&as-pos=0&as-type=HISTORY&as-backfill=on&page=3',
            'https://www.flipkart.com/search?q=mobiles&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_0_0&otracker1=AS_Query_TrendingAutoSuggest_0_0&as-pos=0&as-type=HISTORY&as-backfill=on&page=5',
            'https://www.flipkart.com/search?q=mobiles&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_0_0&otracker1=AS_Query_TrendingAutoSuggest_0_0&as-pos=0&as-type=HISTORY&as-backfill=on&page=10',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)
    def parse(self, response):
        page = response.url.split("/")[-2]
        
        quotes=response.css("div._1UoZlX")

        for quote in quotes: 
            MODEL_NO = quote.css("div._3wU53n ::text").get()
            RATING =quote.css("span._38sUEc ::text").get(),
            PRICE =quote.css("div._1uv9Cb ::text").getall()

            yield {
                "MODEL_NO":MODEL_NO,
                "RATING":RATING,
                "PRICE":PRICE,
            }
            next_page_id = response.css("a._3fVaIS ::attr(href)").get()
            if next_page_id is not None:
                next_page = response.urljoin(next_page_id)
                yield scrapy.Request(next_page,callback=self.parse)
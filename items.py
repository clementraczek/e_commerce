# books_scraper/items.py

import scrapy

class BookItem(scrapy.Item):
    upc = scrapy.Field() 
    url = scrapy.Field()

    title = scrapy.Field()
    price = scrapy.Field()          
    price_float = scrapy.Field()    
    review_rating = scrapy.Field()  
    description = scrapy.Field()
    category = scrapy.Field()
    number_of_reviews = scrapy.Field()
    availability = scrapy.Field()

   
    image_url = scrapy.Field()
    image_paths = scrapy.Field()


class CategoryItem(scrapy.Item):

    category_name = scrapy.Field()
    book_count = scrapy.Field() 
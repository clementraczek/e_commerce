# books_scraper/spiders/books_spider.py

import scrapy
import re
from urllib.parse import urljoin
from ..items import BookItem, CategoryItem

class ECommerceSpider(scrapy.Spider): 
    name = 'e_commerce'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    
    
    MAX_PAGES = 2 # On prend seulement un nombre limité de pages, ici 2

    def parse(self, response):
        """ Niveau 1 : Limite le traitement à la PREMIÈRE catégorie trouvée. """
        
        category_links = response.css('div.side_categories ul li ul li a')
        
        # On prend seulement un nombre limité de catégorie, ici 3
        if category_links:
            a = category_links[3] 
            
            href = a.attrib.get('href')
            category_name = a.xpath('text()').get().strip()
            
            url = response.urljoin(href) 
            
            yield scrapy.Request(
                url,
                callback=self.parse_category,
           
                meta={'category': category_name, 'page': 1, 'base_url': url}
            )

    def parse_category(self, response):
        category = response.meta['category']
        page = response.meta['page']
        base_url = response.meta['base_url']

  
        if page == 1:
            yield CategoryItem(category_name=category)

        for book in response.css('article.product_pod'):
            rel = book.css('h3 a::attr(href)').get()
            yield response.follow(
                rel, 
                callback=self.parse_book, 
                meta={'category': category}
            )

        if page < self.MAX_PAGES:
            next_page_link = response.css('li.next a::attr(href)').get()
            
            if next_page_link:
                yield response.follow(
                    next_page_link,
                    callback=self.parse_category,
                    # Incrémentation de la page cruciale pour l'arrêt
                    meta={'category': category, 'page': page + 1, 'base_url': base_url}
                )

    def parse_book(self, response):
        item = BookItem()
        item['url'] = response.url
        
        RATING_MAP = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating_class = response.css('p.star-rating').attrib.get('class', '')
        
        m = re.search(r'star-rating\s+(\w+)', rating_class)
        rating_text = m.group(1) if m else ''
        item['review_rating'] = RATING_MAP.get(rating_text, 0)
        
        item['title'] = response.css('div.product_main h1::text').get().strip()
        item['price'] = response.css('p.price_color::text').get().strip()
        item['category'] = response.meta['category']
        
        desc = response.xpath('//div[@id="product_description"]/following-sibling::p[1]/text()').get()
        item['description'] = desc.strip() if desc else ''
    
        rows = response.css('table.table.table-striped tr')
        upc = None
        reviews = None
        
        for row in rows:
            header = row.css('th::text').get()
            data = row.css('td::text').get()

            if header and 'UPC' in header:
                upc = data.strip() if data else None
            
            if header and 'Number of reviews' in header:
                reviews = data.strip() if data else None
        
        item['upc'] = upc # Clé pour le dédoublonnage
        item['number_of_reviews'] = int(reviews) if reviews and reviews.isdigit() else 0
        
     
        availability_text = response.css('.product_main .instock::text').getall()
        item['availability'] = availability_text[-1].strip() if availability_text else 'N/A'

        image_rel = response.css('div.item.active img::attr(src)').get()
        if image_rel:
            item['image_url'] = response.urljoin(image_rel)
            
        yield item
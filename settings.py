

BOT_NAME = "e_commerce"
SPIDER_MODULES = ["e_commerce.spiders"]
NEWSPIDER_MODULE = "e_commerce.spiders"

USER_AGENT = 'MonScraperBooksToScrape (contact@votreadresse.com)' 


ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1              
CONCURRENT_REQUESTS_PER_DOMAIN = 1 

ITEM_PIPELINES = {

    'e_commerce.pipelines.PriceCleaningPipeline': 300, 
    

    'e_commerce.pipelines.DuplicatesAndCategoryCounterPipeline': 500,
    

    'e_commerce.pipelines.MultiFormatExportPipeline': 800,
}


FEED_EXPORT_ENCODING = "utf-8"


FEEDS = {}
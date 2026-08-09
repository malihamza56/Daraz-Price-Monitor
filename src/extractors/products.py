from src.config.logger import logger
from src.config.selectors import (
    PRODUCT_CARD,
    PRODUCT_TITLE,
    PRODUCT_PRICE,
    PRODUCT_LINK,
    PRODUCT_PIC_SRC,
    PRODUCT_RATING
)


class Extractor:
    
    def __init__(self , page):
        self.page = page
        
        logger.info(f'Extractor Constructor Called ')
        
    def extract_basic_details(self):
        
        products = []
        
        try:
            
            logger.info('Extracting Basic Details of Product')
            
            self.page.wait_for_load_state("load")
            
            productCards = self.page.locator(PRODUCT_CARD)
            
            count = productCards.count()
            logger.info(f'Product found | {count}')
            
            for i in range(count):
                
                productCard = productCards.nth(i)
                
                title = productCard.locator(PRODUCT_TITLE).text_content().strip()
            
                price = productCard.locator(PRODUCT_PRICE).text_content().strip()
            
                srcLink = productCard.locator(PRODUCT_LINK).get_attribute('href')
                
                image = productCard.locator(PRODUCT_PIC_SRC)

                imgSrc = image.get_attribute("src")
                
                dataSrc = image.get_attribute("data-src")
                
                lazyLoad = image.get_attribute("data-ks-lazyload")
                    
                rating = productCard.locator(PRODUCT_RATING).count()
                
                products.append({
                    
                'sr' : i+1,
                'title':title,
                'price':price,
                'currency': 'PKR' if "Rs" in price else 'none',
                'rating':rating,
                'productLink': srcLink,
                'imgSrc':imgSrc,
                'dataSrc' : dataSrc,
                'lazyLoad':lazyLoad
                
            })
                
            logger.info("Successfully Extracted Details of Product")
            
            return products
            
        except Exception as e:
            logger.error(f'Failed to Extract details | {e}')
            raise
        
            
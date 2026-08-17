from src.config.logger import logger
from src.core.navigator import Navigation
from src.config.config  import MAX_PAGES
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
        
        all_products = []
        
        try:
            
            logger.info('Extracting Basic Details of Product')
            
            self.page.wait_for_load_state("load")
            current_page = 1
            sr = 1
            
            while current_page <= MAX_PAGES:
                
                navigator = Navigation(page=self.page)
                productCards = self.page.locator(PRODUCT_CARD)
                
                count = productCards.count()
                logger.info(f'Product found | {count}')
                
                for i in range(count):
                    
                    productCard = productCards.nth(i)
                    
                    title = productCard.locator(PRODUCT_TITLE).text_content().strip()
                
                    price = productCard.locator(PRODUCT_PRICE).text_content().strip()
                
                    srcLink = productCard.locator(PRODUCT_LINK).get_attribute('href')
                    
                    images = productCard.locator(PRODUCT_PIC_SRC)

                    imgSrc = None
                    dataSrc = None
                    lazyLoad = None

                    for j in range(images.count()):

                        image = images.nth(j)

                        src = image.get_attribute("src")
                        data_src = image.get_attribute("data-src")
                        lazy_load = image.get_attribute("data-ks-lazyload")

                        # Actual image
                        if src and not src.startswith("data:"):
                            imgSrc = src
                            break

                        if data_src and not data_src.startswith("data:"):
                            dataSrc = data_src

                        if lazy_load and not lazy_load.startswith("data:"):
                            lazyLoad = lazy_load
                        
                    rating = productCard.locator(PRODUCT_RATING).count()
                    
                    all_products.append({
                        
                    'sr' : sr,
                    'title':title,
                    'price':price,
                    'currency': 'PKR' if "Rs" in price else 'none',
                    'rating':rating,
                    'productLink': srcLink,
                    'imgSrc':imgSrc,
                    'dataSrc' : dataSrc,
                    'lazyLoad':lazyLoad
                    
                })
                sr+=1 
                current_page+=1
                
                if current_page >= MAX_PAGES:
                        
                    logger.info(f"Pages limit Reached |{current_page}")
                    break    
                
                navigator.next_page()  
                logger.info("Successfully Extracted Details of Product")
                
            return all_products
            
        except Exception as e:
            logger.error(f'Failed to Extract details | {e}')
            raise
        
            
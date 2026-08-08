from src.config.logger import logger
from src.config.selectors import (
    PRODUCT_CARD,
    PRODUCT_TITLE,
    PRODUCT_PRICE,
    PRODUCT_LINK,
    PRODUCT_PIC_SRC
)
from src.config.config import LOAD_STATE



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

                if imgSrc.startswith("data:image"):

                    imgSrc = (
                        image.get_attribute("data-src")
                        or image.get_attribute("data-ks-lazyload")
                        or imgSrc
                    )
                    
                rating = productCard.locator("i._9-ogB").count()
                
                products.append({
                    
                'sr' : i,
                'title':title,
                'price':price,
                'currency': 'PKR' if "Rs" in price else 'none',
                'productLink': "https:" + srcLink if srcLink.startswith("//") else srcLink,
                'imgSrc':imgSrc,
                'rating':rating
                
            })
                
            logger.info("Successfully Extracted Details of Product")
            
            return products
            
        except Exception as e:
            logger.error(f'Failed to Extract details | {e}')
            raise
        
            
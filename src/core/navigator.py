from src.config.logger import logger
from src.config.selectors import (
    SEARCH_BOX,
    SEARCH_BUTTON,
)
from src.config.config import(
    BASE_URL,
    LOAD_STATE,
    PRODUCT
)

class Navigation:
    
    def __init__(self,page):
        self.page = page
        logger.info("Navigation Constructor Called !")
        
        
    def page_goto(self):
        
        
        try:
            
            logger.info(f"Navigating to Url {BASE_URL}")
            self.page.wait_for_load_state("load")
            self.page.goto(BASE_URL)
            
            logger.info("Page navigated !")
            
            return self.page
        
        except Exception as e:
            logger.error(f'Page Navigation failed | {e}')
            raise


    def search_product(self,page):
        
        
        try:
            
            page.wait_for_load_state("load")
            
            logger.info("Searching Products...")
            
            box = page.locator(SEARCH_BOX)
            
            box.wait_for(state='visible')
        
            box.press_sequentially(PRODUCT)
            
            SEARCH_BUTTON(page=page).click()
            
            logger.info(f"{PRODUCT} products page found !")
            
        except Exception as e:
            logger.error(f'Failed to search products | {e}')
            raise
        
    
from src.config.logger import logger
from src.config.selectors import (
    SEARCH_BOX,
    SEARCH_BUTTON,
    NEXT_PAGE
)
from src.config.config import BASE_URL

class Navigation:
    
    def __init__(self,page):
        self.page = page
        logger.info("Navigation Constructor Called !")
        
        
    def page_goto(self):
        
        
        try:
            
            logger.info(f"Navigating to Url {BASE_URL}")
            self.page.goto(BASE_URL)
            
            self.page.wait_for_load_state("load")
            logger.info("Page navigated !")
            
            return self.page
        
        except Exception as e:
            logger.error(f'Page Navigation failed | {e}')
            raise


    def search_product(self, product_name):

        try:

            logger.info("Searching Products...")

            # Wait until current page is loaded
            self.page.wait_for_load_state("load")

            logger.info(
                f"Current URL before search | {self.page.url}"
            )

            logger.info(
                f"Page title before search | {self.page.title()}"
            )

            # Search box
            box = self.page.locator(SEARCH_BOX)

            # Wait for search box to become visible
            box.wait_for(
                state="visible",
                timeout=30000
            )

            logger.info(
                "Search box found successfully!"
            )

            # Enter product name
            box.press_sequentially(
                product_name,
                delay=50
            )

            logger.info(
                f"Product name entered | {product_name}"
            )

            # Search button
            search_button = SEARCH_BUTTON(
                page=self.page
            )

            search_button.wait_for(
                state="visible",
                timeout=10000
            )

            search_button.click()

            logger.info(
                f"{product_name} products page found!"
            )

        except Exception as e:

            logger.error(
                f"Failed to search products | {e}"
            )

            # Debug information
            logger.error(
                f"Current URL | {self.page.url}"
            )

            logger.error(
                f"Page title | {self.page.title()}"
            )

            # Save screenshot for debugging
            self.page.screenshot(
                path="headless_search_error.png",
                full_page=True
            )

            raise
            
    
    def next_page(self):
        
        try:
            
            logger.info("Cheking pagination")
            
            next_page_button = self.page.locator(NEXT_PAGE)
            
            next_page_button.click()
            
            logger.info("Next Page Found !")
            
            self.page.wait_for_load_state("load")
        
        except Exception as e:
            logger.error(f'Falied for pagination process | {e}')
            raise
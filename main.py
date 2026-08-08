from src.config.logger import logger
from src.config.config import RAW_JSON
from src.core.browser import Browser
from src.core.navigator import Navigation
from src.extractors.products import Extractor
from src.services.cleaner import Cleaner
from src.services.json_services import Json
from playwright.sync_api import sync_playwright



def main():
    
    try:
        
        logger.info('Main module Calling')
        
        with sync_playwright() as playwright:
            
            BROWSER = Browser(playwright=playwright)  #*browser object
            
            browser,context,Page =  BROWSER.launch_browser()  #* launching....
            
            PAGE = Navigation(page=Page)   #* Page 
            
            Page = PAGE.page_goto()        #* Page Navigation
            
            PAGE.search_product(page=Page)   #*Searching Product
            
            extractor = Extractor(page=Page)   #* Extracting product
            
            products = extractor.extract_basic_details()       #* detailsExtraction
                    
            CLEANER = Cleaner(products=products)
            
            data = CLEANER._cleanPrice()
            
            JSON = Json(products=data)
            
            JSON.dump(path=RAW_JSON)
            
            BROWSER.close_browser(browser=browser)
            
    except Exception as e:
        logger.error(f"Scraper Failed | {e}")
        
    

if __name__ == "__main__":
    main()
            
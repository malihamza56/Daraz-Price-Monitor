from playwright.sync_api import sync_playwright
import pandas as pd
from src.config.logger import logger
from src.config.config import (
    JSON_PATH,
    RAW_JSON,
    FILTERED_JSON,
    PREVIOUS_FILTERED_JSON
)
from src.exporters.serializer import Exporter
from src.core.browser import Browser
from src.core.navigator import Navigation
from src.services.price_tracker import Tracker
from src.extractors.products import Extractor
from src.notifications.mailer import Mailer
from src.services.cleaner import Cleaner
from src.services.json_services import Json
from src.services.filter_products import Filter
import json

def main():

    try:

        logger.info("Main module Calling")
        
        name = input("Enter Name of the product to search :").lower().strip()
        brand = input(f"Enter Target Brand of {name}: ").lower()
        price = int(input("Enter Target Price: "))

        with sync_playwright() as playwright:

            # Browser
            browser_manager = Browser(playwright=playwright)

            browser,page = browser_manager.launch_browser()

            # Navigation
            navigation = Navigation(page=page)

            page = navigation.page_goto()

            # Search
            navigation.search_product(product_name=name)

            # Extraction
            extractor = Extractor(page=page)

            products = extractor.extract_basic_details()

            # Save RAW data
            raw_json = Json(products=products)

            raw_json.dump(path=RAW_JSON)
            
            
            # Cleaning
            cleaner = Cleaner(products=products)

            cleaned_products = cleaner._cleaned_products()

            # Save CLEAN data from serializer
            df = pd.DataFrame(cleaned_products)
            clean_json = Exporter(dataFrame=df)

            clean_json._jsonExport(path=JSON_PATH)
            
            # Filtering
            filter_products = Filter(
                products=cleaned_products,
                brand=brand,
                price=price
            )
            
            
            filtered_products = filter_products._filteredProducts()

            # Save FILTERED data
            filtered_json = Json(products=filtered_products)

            filtered_json.dump(
                path=FILTERED_JSON
            )
            
            
            #Previous Json Snapshot
            snapshot_json = Json(products=filtered_products)
            
            if not snapshot_json.exists(path=PREVIOUS_FILTERED_JSON):
                
                logger.info("First Run detected ! No previous Data present")
                df = pd.DataFrame(filtered_products)
                
                snapshot_Exporter = Exporter(dataFrame=df)
                
                snapshot_Exporter._jsonExport(path=PREVIOUS_FILTERED_JSON)
                
            else:
                
                logger.info("Previous Filtered Data Found !")

                old_products = snapshot_json.load(path=PREVIOUS_FILTERED_JSON)
                new_products = filtered_products
                
                tracker = Tracker(
                    old=old_products,
                    new=new_products
                )
                
                tracked_products = tracker._priceTracker()
                
                logger.info(f"{len(tracked_products)} Dropped price products found !")

                if tracked_products:
                    mailer = Mailer(tracked_products)
                    mailer._send_email()
                    
                    
                df = pd.DataFrame(new_products)
                
                snapshot_Exporter = Exporter(dataFrame=df)
                snapshot_Exporter._jsonExport(path=PREVIOUS_FILTERED_JSON)
                
            # Close Browser
            browser_manager.close_browser(browser=browser)

            logger.info("Scraper completed successfully!")
            print("Scraper Completed !")
            
    except Exception as e:

        logger.error(f"Scraper Failed | {e}")
        raise


if __name__ == "__main__":
    main()
from playwright.sync_api import sync_playwright

from src.config.logger import logger
from src.config.config import RAW_JSON, JSON_PATH

from src.core.browser import Browser
from src.core.navigator import Navigation

from src.extractors.products import Extractor

from src.services.cleaner import Cleaner
from src.services.json_services import Json
from src.services.filter_products import Filter


def main():

    try:

        logger.info("Main module Calling")

        brand = input("Enter Target Brand of Laptop: ").lower()
        price = int(input("Enter Target Price: "))

        with sync_playwright() as playwright:

            # Browser
            browser_manager = Browser(playwright=playwright)

            browser, context, page = browser_manager.launch_browser()

            # Navigation
            navigation = Navigation(page=page)

            page = navigation.page_goto()

            # Search
            navigation.search_product(page=page)

            # Extraction
            extractor = Extractor(page=page)

            products = extractor.extract_basic_details()

            # Cleaning
            cleaner = Cleaner(products=products)

            cleaned_products = cleaner._cleaned_products()

            # Save RAW data
            raw_json = Json(products=products)

            raw_json.dump(path=RAW_JSON)

            # Save CLEAN data
            clean_json = Json(products=cleaned_products)

            clean_json.dump(path=JSON_PATH)

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
                path="data/processed/filtered_products.json"
            )

            # Close Browser
            browser_manager.close_browser(browser=browser)

            logger.info("Scraper completed successfully!")

    except Exception as e:

        logger.error(f"Scraper Failed | {e}")
        raise


if __name__ == "__main__":
    main()
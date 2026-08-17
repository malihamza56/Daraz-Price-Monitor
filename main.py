import pandas as pd

from playwright.sync_api import sync_playwright

from src.config.logger import logger

from src.config.config import (
    JSON_PATH,
    RAW_JSON,
    FILTERED_JSON,
    PREVIOUS_FILTERED_JSON,
    PREVIOUS_FILTERED_EXCEL,
)

from src.exporters.serializer import Exporter

from src.core.browser import Browser
from src.core.navigator import Navigation

from src.extractors.products import Extractor

from src.services.cleaner import Cleaner
from src.services.json_services import Json
from src.services.filter_products import Filter
from src.services.price_tracker import Tracker

from src.notifications.mailer import Mailer


# ============================================================
# SEARCH WORKFLOW
# ============================================================

def run_search(
    product_name,
    target_price,
    condition,
    brand,
):
    """
    Complete scraping workflow.

    UI
      ↓
    Search
      ↓
    Pagination
      ↓
    Extraction
      ↓
    Cleaning
      ↓
    Brand + Price Filtering
      ↓
    JSON / Excel data
    """

    browser_manager = None
    browser = None

    try:

        logger.info("Search workflow started")

        # ----------------------------------------------------
        # INPUT CLEANING
        # ----------------------------------------------------

        product_name = (
            product_name
            .strip()
            .lower()
        )

        brand = (
            brand
            .strip()
            .lower()
        )

        target_price = int(
            target_price
        )

        # ----------------------------------------------------
        # PLAYWRIGHT
        # ----------------------------------------------------

        with sync_playwright() as playwright:

            # =================================================
            # BROWSER
            # =================================================

            browser_manager = Browser(
                playwright=playwright
            )

            browser, page = (
                browser_manager.launch_browser()
            )

            # =================================================
            # NAVIGATION
            # =================================================

            navigation = Navigation(
                page=page
            )

            page = navigation.page_goto()

            # =================================================
            # SEARCH
            # =================================================

            navigation.search_product(
                product_name=product_name
            )

            # =================================================
            # EXTRACTION
            # =================================================

            extractor = Extractor(
                page=page
            )

            # IMPORTANT:
            # Extractor now handles pagination internally.

            products = (
                extractor.extract_basic_details()
            )

            logger.info(
                f"Total products extracted | "
                f"{len(products)}"
            )

            # =================================================
            # RAW DATA
            # =================================================

            raw_json = Json(
                products=products
            )

            raw_json.dump(
                path=RAW_JSON
            )

            # =================================================
            # CLEANING
            # =================================================

            cleaner = Cleaner(
                products=products
            )

            cleaned_products = (
                cleaner._cleaned_products()
            )

            # =================================================
            # CLEAN DATA EXPORT
            # =================================================

            clean_df = pd.DataFrame(
                cleaned_products
            )

            clean_exporter = Exporter(
                dataFrame=clean_df
            )

            clean_exporter._jsonExport(
                path=JSON_PATH
            )

            # =================================================
            # FILTERING
            # =================================================

            filter_service = Filter(
                products=cleaned_products,
                brand=brand,
                
            )

            filtered_products = (
                filter_service._filteredProducts()
            )

            # =================================================
            # CONDITION FILTER
            # =================================================

            if condition == "Below Target Price":

                filtered_products = [
                    product
                    for product in filtered_products
                    if product.get("price", 0)
                    <= target_price
                ]

            elif condition == "Above Target Price":

                filtered_products = [
                    product
                    for product in filtered_products
                    if product.get("price", 0)
                    >= target_price
                ]

            logger.info(
                f"Filtered products | "
                f"{len(filtered_products)}"
            )

            # =================================================
            # FILTERED JSON
            # =================================================

            filtered_json = Json(
                products=filtered_products
            )

            filtered_json.dump(
                path=FILTERED_JSON
            )

            # =================================================
            # CLOSE BROWSER
            # =================================================

            browser_manager.close_browser(
                browser=browser
            )

            browser = None

            logger.info(
                "Search workflow completed successfully"
            )

            # =================================================
            # RETURN TO UI
            # =================================================

            return {
                "status": "success",

                "products_found": len(
                    products
                ),

                "filtered_count": len(
                    filtered_products
                ),

                "products": filtered_products,
            }

    except Exception as e:

        logger.error(
            f"Search workflow failed | {e}"
        )

        raise

    finally:

        # Safety cleanup
        if browser is not None:

            try:

                browser_manager.close_browser(
                    browser=browser
                )

            except Exception as cleanup_error:

                logger.error(
                    f"Browser cleanup failed | "
                    f"{cleanup_error}"
                )


# ============================================================
# PRICE TRACKING
# ============================================================

def track_price(
    filtered_products,
):
    """
    Compare current filtered products
    with previous snapshot.
    """

    try:

        logger.info(
            "Price tracking workflow started"
        )

        # ----------------------------------------------------
        # NONE / EMPTY CONDITION
        # ----------------------------------------------------

        if not filtered_products:

            logger.info(
                "No filtered products available"
            )

            return {
                "status": "empty",

                "price_drops": [],

                "price_drop_count": 0,

                "message":
                    "No products available for tracking.",
            }

        # ----------------------------------------------------
        # SNAPSHOT
        # ----------------------------------------------------

        snapshot_json = Json(products=filtered_products)

        # ====================================================
        # FIRST RUN
        # ====================================================

        if not snapshot_json.exists(
            path=PREVIOUS_FILTERED_JSON
        ):

            logger.info(
                "First tracking run detected"
            )

            df = pd.DataFrame(
                filtered_products
            )

            exporter = Exporter(
                dataFrame=df
            )

            exporter._jsonExport(
                path=PREVIOUS_FILTERED_JSON
            )

            exporter._excelExport(
                path=PREVIOUS_FILTERED_EXCEL
            )

            return {
                "status": "first_run",

                "price_drops": [],

                "price_drop_count": 0,

                "message":
                    "Initial price snapshot created.",
            }

        # ====================================================
        # PREVIOUS DATA FOUND
        # ====================================================

        logger.info(
            "Previous filtered data found"
        )

        old_products = snapshot_json.load(
            path=PREVIOUS_FILTERED_JSON
        )

        new_products = filtered_products

        # ----------------------------------------------------
        # TRACKER
        # ----------------------------------------------------

        tracker = Tracker(
            old=old_products,
            new=new_products,
        )

        tracked_products = (
            tracker._priceTracker()
        )

        logger.info(
            f"Price drops found | "
            f"{len(tracked_products)}"
        )

        # ----------------------------------------------------
        # UPDATE SNAPSHOT
        # ----------------------------------------------------

        df = pd.DataFrame(
            new_products
        )

        exporter = Exporter(
            dataFrame=df
        )

        exporter._jsonExport(
            path=PREVIOUS_FILTERED_JSON
        )

        exporter._excelExport(
            path=PREVIOUS_FILTERED_EXCEL
        )

        # ====================================================
        # RESULT
        # ====================================================

        if tracked_products:

            return {
                "status": "price_drop",

                "price_drops":
                    tracked_products,

                "price_drop_count":
                    len(tracked_products),

                "message":
                    f"{len(tracked_products)} "
                    "price drop(s) detected.",
            }

        return {
            "status": "no_drop",

            "price_drops": [],

            "price_drop_count": 0,

            "message":
                "No price drop detected.",
        }

    except Exception as e:

        logger.error(
            f"Price tracking failed | {e}"
        )

        raise


# ============================================================
# EMAIL
# ============================================================

def send_price_email(
    tracked_products,
    target_email
):
    """
    Send price-drop email.
    """

    try:

        if not tracked_products:

            return {
                "status": "empty",

                "message":
                    "No price drops available.",
            }

        mailer = Mailer(
            tracked_products,
            target_email=target_email
        )

        mailer._send_email()

        logger.info(
            "Price drop email sent successfully"
        )

        return {
            "status": "sent",

            "message":
                "Email sent successfully.",
        }

    except Exception as e:

        logger.error(
            f"Email sending failed | {e}"
        )

        raise


# ============================================================
# CLI TEST
# ============================================================

def main():

    """
    Temporary CLI testing.
    Streamlit will use run_search(),
    track_price() and send_price_email().
    """

    product_name = input(
        "Enter product name: "
    ).strip()

    brand = ""
        
    

    target_price = int(
        input(
            "Enter target price: "
        )
    )

    condition = input(
        "Enter condition "
        "(Below Target Price / Above Target Price): "
    ).strip()

    result = run_search(
        product_name=product_name,
        target_price=target_price,
        condition=condition,
        brand=brand,
    )

    print(
        f"\nProducts found: "
        f"{result['products_found']}"
    )

    print(
        f"Filtered products: "
        f"{result['filtered_count']}"
    )

    tracking = track_price(
        filtered_products=result["products"]
    )

    print(
        tracking["message"]
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
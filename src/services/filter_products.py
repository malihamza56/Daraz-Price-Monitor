
from src.config.logger import logger


class Filter:
    
    def __init__(self,products,brand):
        self.cleanedProducts = products
    
        self.targetBrand = brand
        
        logger.info(f"{len(self.cleanedProducts)} No of products found - Target Brand : {self.targetBrand}")
        
    def _filteredProducts(self):

        filtered_products = []

        try:

            logger.info(
                f"Filtering products by brand: "
                f"{self.targetBrand}"
            )

            for product in self.cleanedProducts:

                title = product.get("title", "").lower()

                # Brand is OPTIONAL
                if self.targetBrand:

                    if self.targetBrand.lower() not in title:
                        continue

                filtered_products.append(product)

            logger.info(
                f"Brand filtering completed | "
                f"{len(filtered_products)} products found"
            )

            return filtered_products

        except Exception as e:

            logger.error(
                f"Failed to filter products | {e}"
            )

            raise
            
        
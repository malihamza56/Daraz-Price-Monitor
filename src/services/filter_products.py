
from src.config.logger import logger
from src.config.config import TARGET_PRICE

class Filter:
    
    def __init__(self,products,price,brand):
        self.cleanedProducts = products
        self.targetPrice = price
        self.targetBrand = brand
        
    
    def _filteredProducts(self):
        
        filtered_products = []
        
        try:
            logger.info(f"Filtering products according to {TARGET_PRICE} target price...")
            
            for product in self.cleanedProducts:
                
                price = product.get('price')
                title = product.get('title')
                
                if  self.targetBrand in title.lower(): 
                    if price and price <= self.targetPrice:
                        
                        filtered_products.append(
                            product
                        )
                        
        
            logger.info('Products filtered successfully !')
            
            return filtered_products
        
        except Exception as e:
            logger.error(f'Failed to filtered products | {e}')
            raise
        
    
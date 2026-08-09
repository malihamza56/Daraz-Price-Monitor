
from src.config.logger import logger


class Filter:
    
    def __init__(self,products,price,brand):
        self.cleanedProducts = products
        self.targetPrice = price
        self.targetBrand = brand
        
    
    def _filteredProducts(self):
        
        filtered_products = []
        
        try:
            logger.info(f"Filtering {self.targetBrand} products according to {self.targetPrice} target price...")
            
            if self.targetBrand or self.targetPrice:    
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
        
    
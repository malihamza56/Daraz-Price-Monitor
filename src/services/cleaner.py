from src.config.logger import logger



class Cleaner:
    
    def __init__(self,products):
        
        self.products = products
        
    
    def _cleanPrice(self):
        
        try:
            
            logger.info("Cleaning Price of Products...")
            
            for product in self.products:
                
                price = product['price']
                price = price.replace("Rs. ","").replace(",","").strip()
                
                product['price'] = int(price)
                
            return self.products
        
        except Exception as e:
            logger.error(f"Failed to clean price | {e}")
            raise
        
        



from src.config.logger import logger


class Tracker:
    
    def __init__(self,old,new):
        self.oldProducts = old
        self.newProducts = new
        
        
    def _priceTracker(self):
        
      
        droped_products = []
        
        try:
            
            logger.info('Comparing Prices of Old & New Products...')
            
            for old in self.oldProducts:
                for new in self.newProducts:
                    
                    linkA = old.get("productLink")
                    linkB = new.get("productLink")

                    old_price = old.get('price')
                    new_price = new.get('price')
                    
                    if linkA == linkB:
                        if new_price < old_price :
                            
                            droped_products.append(
                                {
                                'title':new.get('title'),
                                'oldPrice':old_price,
                                'newPrice':new_price,
                                'productLink':new.get('productLink')
                                }
                            )
            
            logger.info('Price compared | Dropped Products Stored')
            
            return droped_products
        
        except Exception as e:
            logger.error(f'Failed to compare prices | {e}')
            raise
        
        
                            
        
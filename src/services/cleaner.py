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
        
        


    def _clean_imgSrc(self):

        try:

            logger.info("Cleaning Product Image URLs...")

            for product in self.products:

                imgSrc = product.get("imgSrc")

                if imgSrc and not imgSrc.startswith("data:"):
                    product["imgSrc"] = imgSrc
                    continue

                data_src = product.get("dataSrc")

                if data_src and not data_src.startswith("data:"):
                    product["imgSrc"] = data_src
                    continue

                lazy_load = product.get("lazyLoad")

                if lazy_load and not lazy_load.startswith("data:"):
                    product["imgSrc"] = lazy_load
                    continue

                product["imgSrc"] = None

            logger.info("Product Image URLs Cleaned Successfully")

            return self.products

        except Exception as e:

            logger.error(f"Failed to clean image URLs | {e}")
            raise
        
        
    def _clean_productLink(self):
            
            
            try:
                
                logger.info("products url cleaning...")
                
                for product in self.products:
                    link = product.get('productLink')
                    
                    if link.startswith("//"):
                        product['srclink'] = 'https:'+link
                        
                logger.info('Product links cleaned')
                
            except Exception as e:
                logger.error(f'failed to clean links | {e}')
                raise
            
    
    def _cleaned_products(self):
        
        try:
            
            self._cleanPrice()
            self._clean_imgSrc()
            self._clean_productLink()

            return self.products
        
        except Exception as e:
            logger.error(f'Failed to clean products | {e}')
            raise
        
    
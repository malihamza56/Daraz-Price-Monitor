import json
from src.config.logger import logger
from src.config.config import RAW_JSON
from pathlib import Path

class Json:
    
    def __init__(self , products):
        self.products = products
      
      
    # <DUMP JSON/>   
    def dump(self,path):
        
        try:
            
            logger.info("Exporting to raw json..")
            
            with open(
                path,
                'w',
                encoding="utf-8"
            ) as file:
                
                
                json.dump(
                    self.products,
                    file,
                    indent=4
                )
            
            logger.info("Raw Json Exported !")
            
        except Exception as e:
            logger.error(f"Failed to export Raw Json | {e}")
            raise
        
        
        
        #<LOAD JSON/>
    def load(self,path):
            
        try:
            
            logger.info('Loading Raw Json...')
            
            with open(
                path,
                'r',
                encoding="utf-8"
            ) as file:
                
                
                data = json.load(file)
                
            logger.info("Json Data Loaded !")
            
            return data
        
        except Exception as e:
            logger.error(f"Failed to load Json Data | {e}")
            raise
                
    def exists(self, path):

        return Path(path).exists()
                
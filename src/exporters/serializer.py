
from src.config.logger import logger
import pandas as pd

class Exporter:
    
    def __init__(self,dataFrame):
        self.df = dataFrame
        
    def _jsonExport(self,path):
        
        try:
            
            logger.info('Exporting Json...')
            
            self.df.to_json(
               path,
               indent=4,
               index=False,
               orient='records'
            )
        
            logger.info("Json Saved Successfully...")
            
        except Exception as e:
            logger.error(f'Failed to Export JSon data | {e}')
            raise
        
    
    def _excelExport(self,path):
        
        try:
            
            logger.info('Exporting Data to Excel')
            
            self.df.to_excel(
                path,
                index =False
            )
            
            logger.info('Excel Ouput Done')
            
        except Exception as e:
            logger.error(f'Failed to Export to excel | {e}')
            raise
        
    def _csvExport(self,path):
        
        try:
            
            logger.info('Exporting Data to Csv')
            
            self.df.to_csv(
                path,
                index =False
            )
            
            logger.info('Csv Ouput Done')
            
        except Exception as e:
            logger.error(f'Failed to Export to csv | {e}')
            raise
        
        
    
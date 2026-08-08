"""
^BROWSER: BROSWER MODULE CONTROL THE LAUNCHING AND CLOSING OF BROWSER
"""


from src.config.logger import logger
from src.config.config import HEADLESS




class Browser:
    
    def __init__(self,playwright):
        self.playwright = playwright
        
        
    def launch_browser(
        self
    ):
        
        try:
            
            logger.info("launching Broswser...")
            browser = self.playwright.chromium.launch(headless = HEADLESS)
            
            logger.info("Launching context...")
            context = browser.new_context()
            
            logger.info("Launching Page...")
            page = context.new_page()
            
            logger.info("Broswer Launched successfully")
            return browser,context,page
        
        
        except Exception as e:
            logger.error(f"Failed to launch Browser | {e}")
            raise


    def close_browser(
        self,browser
    ):
        
        try:
            
            logger.info("Closing Broswer...")
            
            if browser:
                browser.close()
                
            logger.info("Browser closed successfully !")
            
        except Exception as e:
            logger.error(f"Failed to close broswer | {e}")
            raise
        
        
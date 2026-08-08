"""
^</logger module: Provides a logger instance to log whole modules of project/>
"""

import logging

#* basic Configuration
logging.basicConfig(
    level=logging.INFO,
    filename="logs/scraper.logs",
    filemode='w',
    format="%(asctime)s | %(levelname)s | %(filename)s | %(message)s"
)


#* Logger Instance
logger = logging.getLogger(__name__)

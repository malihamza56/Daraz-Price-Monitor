
"""
! PROJECT CONFIGURATION;
!Stores all the global configuration setup used throught the project
"""


#-------------------------------------------
#!        BROWSER CONFIGS
#-------------------------------------------

HEADLESS = False
SLOW_MO = 500
LOAD_STATE = "networkidle"

#-------------------------------------------
#!        WEBSITE
#-------------------------------------------


BASE_URL = "https://www.daraz.pk/"


#-------------------------------------------
#!        EXPORTER PATHS
#-------------------------------------------

RAW_JSON = "data/raw/raw_products.json"
JSON_PATH = "data/processed/products.json"
CSV_PATH = "data/processed/products.csv"
EXCEL_PATH = "data/processed/products.xlsx"



#!-------------------------------------------
#!        PRODUCT
#!-------------------------------------------

PRODUCT = 'Laptop'
TARGET_PRICE = 50000



#!-------------------------------------------
#!        SNAPSHOTS
#!-------------------------------------------

SNAP_PATH = "snapshots/product.png"

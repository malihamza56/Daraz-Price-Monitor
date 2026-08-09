
"""
! PROJECT CONFIGURATION;
!Stores all the global configuration setup used throught the project
"""
import os
from dotenv import load_dotenv
from pathlib import Path

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



#!------------------------------------------
#!      MAILER CONFIGURATION
#!------------------------------------------


BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

TARGET_EMAIL = os.getenv("TARGET_EMAIL")
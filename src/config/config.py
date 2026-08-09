
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

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_JSON = BASE_DIR / "data/raw/raw_products.json"
JSON_PATH = BASE_DIR / "data/processed/clean_products.json"
FILTERED_JSON = BASE_DIR / "data/processed/filtered_products.json"
PREVIOUS_FILTERED_JSON = BASE_DIR / "data/processed/previous_filtered_products.json"



#!-------------------------------------------
#!        SNAPSHOTS
#!-------------------------------------------

SNAP_PATH = BASE_DIR / "snapshots/product.png"



#!------------------------------------------
#!      MAILER CONFIGURATION
#!------------------------------------------


ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

TARGET_EMAIL = os.getenv("TARGET_EMAIL")
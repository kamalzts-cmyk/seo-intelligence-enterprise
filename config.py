import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "SEO Intelligence Pro Enterprise V3"
USER_AGENT = "SEOIntelligenceProEnterpriseBot/3.0"
REQUEST_TIMEOUT = 15
DEFAULT_MAX_PAGES = int(os.getenv("MAX_CRAWL_PAGES", "100"))

DATAFORSEO_LOGIN = os.getenv("DATAFORSEO_LOGIN", "")
DATAFORSEO_PASSWORD = os.getenv("DATAFORSEO_PASSWORD", "")
PAGESPEED_API_KEY = os.getenv("PAGESPEED_API_KEY", "")

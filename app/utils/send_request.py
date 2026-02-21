import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:7860"

def classify_headline():
    for headline in ["Stock market rises", "Stock market crashes"]:
        response = requests.post(
                f"{BASE_URL}/classify",
                json={"headline": headline},
            )
            
        logger.info(f"Status: {response.status_code}")
        logger.info(f"Response: {response.json()}")
    
    return None

classify_headline()
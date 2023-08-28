import logging

import httpx
from .func_utils import INSTAGRAM_BASE_URL, ACCESS_TOKEN

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def instagram_search_keyword(keyword: str):

    instagram_req_url = f"{INSTAGRAM_BASE_URL}tag/{keyword}/posts?access_token={ACCESS_TOKEN}&lang=fr,en&order_by=date_desc&max_page_size=50"

    try:
        with httpx.Client() as client:
            response = client.get(instagram_req_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logger.error(f"La requête a échoué avec le code d'état: {response.status_code})")
    except (httpx.RequestError, ValueError) as err:
        logger.error(f"Request error: {err})")


def instagram_stats():

    instagram_req_url = f"{INSTAGRAM_BASE_URL}stats?access_token={ACCESS_TOKEN}"

    try:
        with httpx.Client() as client:
            response = client.get(instagram_req_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logger.error(f"La requête a échoué avec le code d'état: {response.status_code})")
    except (httpx.RequestError, ValueError) as err:
        logger.error(f"Request error: {err})")


def instagram_list_created_tasks(item_type: str):

    instagram_req_url = f"{INSTAGRAM_BASE_URL}{item_type}/tasks/?access_token={ACCESS_TOKEN}"

    try:
        with httpx.Client() as client:
            response = client.get(instagram_req_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logger.error(f"La requête a échoué avec le code d'état: {response.status_code})")
    except (httpx.RequestError, ValueError) as err:
        logger.error(f"Request error: {err})")

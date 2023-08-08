import logging

import httpx
from flask import current_app

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = current_app._get_current_object()
api_base_url = app.config["API_BASE_URL"]
api_access_token = app.config['API_ACCESS_TOKEN']


def instagram_search_keywords(keyword: str):

    request_url = f"{api_base_url}instagram/tag/{keyword}/posts?access_token={api_access_token}&lang=fr,en&order_by=date_desc&max_page_size=50"

    try:
        with httpx.Client() as client:
            response = client.get(request_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logger.error(f"La requête a échoué avec le code d'état: {response.status_code})")
    except (httpx.RequestError, ValueError) as err:
        logger.error(f"Request error: {err})")


def instagram_stats():

    request_url = f"{api_base_url}instagram/stats?access_token={api_access_token}"

    try:
        with httpx.Client() as client:
            response = client.get(request_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logger.error(f"La requête a échoué avec le code d'état: {response.status_code})")
    except (httpx.RequestError, ValueError) as err:
        logger.error(f"Request error: {err})")


def instagram_list_created_tasks(item_type: str):

    """
    List of the created tasks
    """

    request_url = f"{api_base_url}instagram/{item_type}/tasks/?access_token={api_access_token}"

    try:
        with httpx.Client() as client:
            response = client.get(request_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logger.error(f"La requête a échoué avec le code d'état: {response.status_code})")
    except (httpx.RequestError, ValueError) as err:
        logger.error(f"Request error: {err})")

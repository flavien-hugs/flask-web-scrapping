import logging

import httpx

from .func_utils import ACCESS_TOKEN
from .func_utils import FACEBOOK_BASE_URL


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def facebook_search_keyword(keyword: str):
    facebook_req_url = f"{FACEBOOK_BASE_URL}search/{keyword}/posts/latest/posts?access_token={ACCESS_TOKEN}&lang=fr,en&order_by=date_desc&max_page_size=50"

    try:
        with httpx.Client() as client:
            response = client.get(facebook_req_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logger.error(
                    f"La requête a échoué avec le code d'état: {response.status_code})"
                )
    except (httpx.RequestError, ValueError) as err:
        logger.error(f"Request error: {err})")


def faceebook_post_by_id(post_id: str):
    facebook_req_url = f"{FACEBOOK_BASE_URL}post/{post_id}?access_token={ACCESS_TOKEN}"

    try:
        with httpx.Client() as client:
            response = client.get(facebook_req_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logger.error(
                    f"La requête a échoué avec le code d'état: {response.status_code})"
                )
    except (httpx.RequestError, ValueError) as err:
        logger.error(f"Request error: {err})")


def faceebook_post_comment(post_id: str):
    facebook_req_url = (
        f"{FACEBOOK_BASE_URL}post/{post_id}/comments?access_token={ACCESS_TOKEN}"
    )

    try:
        with httpx.Client() as client:
            response = client.get(facebook_req_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logger.error(
                    f"La requête a échoué avec le code d'état: {response.status_code})"
                )
    except (httpx.RequestError, ValueError) as err:
        logger.error(f"Request error: {err})")

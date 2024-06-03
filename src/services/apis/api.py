import logging

import httpx

from .func_utils import ACCESS_TOKEN
from .func_utils import HASHTAGS, COMMENTS


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def search_keyword(keyword: str):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    url = f"{HASHTAGS}/recommend?keyword={keyword}"

    try:
        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    f"La requête a échoué avec le code d'état: {response.status_code})"
                )
    except (httpx.RequestError, ValueError) as err:
        logger.error(f"Request error: {err})")


def search_comments(keyword: str):
    payload = {
        "id": f"{keyword}",
        "platforms": [
            "tiktok",
            "twitter",
            "youtube",
        ],
    }
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    url = f"{COMMENTS}"

    try:
        with httpx.Client() as client:
            response = client.get(url, data=payload, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    f"La requête a échoué avec le code d'état: {response.status_code})"
                )
    except (httpx.RequestError, ValueError) as err:
        logger.error(f"Request error: {err})")

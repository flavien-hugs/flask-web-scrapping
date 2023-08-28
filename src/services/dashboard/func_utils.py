import logging

from itertools import chain
from flask_login import current_user

from src.services.account import Project
from src.services.apis import instagram, facebook

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def collection_data():

    facebook_data = []
    instagram_data = []
    projects = Project.all(current_user)

    for project in projects:

        if not project:
            continue

        instagram_items = instagram.instagram_search_keyword(project.name)
        if instagram_items and 'data' in instagram_items and 'items' in instagram_items['data']:
            instagram_data.extend(instagram_items['data']['items'])

        facebook_items = facebook.facebook_search_keyword(project.name)
        if facebook_items and 'data' in facebook_items and 'items' in facebook_items['data']:
            facebook_data.extend(facebook_items['data']['items'])

    combined_data = list(chain(instagram_data, facebook_data))

    return combined_data


def collection_statistic():
    data = collection_data()
    shares_counts = [d.get('shares_count', 0) for d in data]
    total_shares = sum(count for count in shares_counts if count is not None)

    comments_counts = [d.get('comments_count', 0) for d in data]
    total_comments = sum(count for count in comments_counts if count is not None)

    reactions_counts = [d.get('reactions_total_count', 0) for d in data]
    total_reactions = sum(count for count in comments_counts if count is not None)

    return total_reactions, total_comments, total_shares


def collection_data_detail(project_name):
    facebook_data = []
    instagram_data = []
    instagram_items = instagram.instagram_search_keyword(project_name)
    if instagram_items and 'data' in instagram_items and 'items' in instagram_items['data']:
        instagram_data.extend(instagram_items['data']['items'])

    facebook_items = facebook.facebook_search_keyword(project_name)
    if facebook_items and 'data' in facebook_items and 'items' in facebook_items['data']:
        facebook_data.extend(facebook_items['data']['items'])

    combined_data = list(chain(instagram_data, facebook_data))

    return combined_data


def collection_statistic_detail(project_name):
    data = collection_data_detail(project_name)
    shares_counts = [d.get('shares_count', 0) for d in data]
    total_shares = sum(count for count in shares_counts if count is not None)

    comments_counts = [d.get('comments_count', 0) for d in data]
    total_comments = sum(count for count in comments_counts if count is not None)

    reactions_counts = [d.get('reactions_total_count', 0) for d in data]
    total_reactions = sum(count for count in comments_counts if count is not None)

    return total_reactions, total_comments, total_shares

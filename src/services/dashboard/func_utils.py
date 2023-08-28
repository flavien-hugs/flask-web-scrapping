import logging

from itertools import chain
from flask_login import current_user

from src.services.account import Project
from src.services.apis import instagram, facebook

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Facebook:

    def __init__(self, current_user):
        self.current_user = current_user
        self.data = []

    def facebook_data(self):
        projects = Project.all(self.current_user)

        for project in projects:
            if not project:
                continue

            facebook_items = facebook.facebook_search_keyword(project.name)
            if facebook_items and 'data' in facebook_items and 'items' in facebook_items['data']:
                self.data.extend(facebook_items['data']['items'])

    def get_data(self):
        self.facebook_data()
        return self.data

    def get_detail(self, project_name):
        facebook_data = []
        facebook_items = facebook.facebook_search_keyword(project_name)
        if facebook_items and 'data' in facebook_items and 'items' in facebook_items['data']:
            facebook_data.extend(facebook_items['data']['items'])
        return facebook_data

    def get_statistic(self, project_name):
        data = self.get_detail(project_name)
        shares_counts = [d.get('shares_count', 0) for d in data]
        total_shares = sum(count for count in shares_counts if count is not None)

        comments_counts = [d.get('comments_count', 0) for d in data]
        total_comments = sum(count for count in comments_counts if count is not None)

        reactions_counts = [d.get('reactions_total_count', 0) for d in data]
        total_reactions = sum(count for count in comments_counts if count is not None)

        return total_reactions, total_comments, total_shares


class Instagram:

    def __init__(self, current_user):
        self.current_user = current_user
        self.data = []

    def collect_data(self):
        projects = Project.all(self.current_user)

        for project in projects:
            if not project:
                continue

            instagram_items = instagram.instagram_search_keyword(project.name)
            if instagram_items and 'data' in instagram_items and 'items' in instagram_items['data']:
                self.data.extend(instagram_items['data']['items'])

    def get_data(self):
        self.collect_data()
        return self.data

    def get_detail(self, project_name):
        instagram_data = []
        instagram_items = instagram.instagram_search_keyword(project_name)
        if instagram_items and 'data' in instagram_items and 'items' in instagram_items['data']:
            instagram_data.extend(instagram_items['data']['items'])
        return instagram_data

    def get_statistic(self, project_name):
        data = self.get_detail(project_name)
        shares_counts = [d.get('shares_count', 0) for d in data]
        total_shares = sum(count for count in shares_counts if count is not None)

        comments_counts = [d.get('comments_count', 0) for d in data]
        total_comments = sum(count for count in comments_counts if count is not None)

        reactions_counts = [d.get('reactions_total_count', 0) for d in data]
        total_reactions = sum(count for count in comments_counts if count is not None)

        return total_reactions, total_comments, total_shares


class CombinedData:

    def __init__(self, current_user):
        self.current_user = current_user
        self.facebook_collector = Facebook(self.current_user)
        self.instagram_collector = Instagram(self.current_user)

    def get_combined_data(self):
        facebook_data = self.facebook_collector.get_data()
        instagram_data = self.instagram_collector.get_data()
        return list(chain(instagram_data, facebook_data))

    def get_detail(self, project_name):
        instagram_data = []
        facebook_data = []

        instagram_items = instagram.instagram_search_keyword(project_name)
        if instagram_items and 'data' in instagram_items and 'items' in instagram_items['data']:
            instagram_data.extend(instagram_items['data']['items'])

        facebook_items = facebook.facebook_search_keyword(project_name)
        if facebook_items and 'data' in facebook_items and 'items' in facebook_items['data']:
            facebook_data.extend(facebook_items['data']['items'])

        combined_data = list(chain(instagram_data, facebook_data))
        return combined_data

    def get_stat_facebook(self):
        data = self.facebook_collector.get_data()

        shares_counts = [d.get('shares_count', 0) for d in data]
        total_shares = sum(count for count in shares_counts if count is not None)

        comments_counts = [d.get('comments_count', 0) for d in data]
        total_comments = sum(count for count in comments_counts if count is not None)

        reactions_counts = [d.get('reactions_total_count', 0) for d in data]
        total_reactions = sum(count for count in reactions_counts if count is not None)

        return total_reactions, total_comments, total_shares

    def get_stat_instagram(self):
        data = self.instagram_collector.get_data()

        shares_counts = [d.get('shares_count', 0) for d in data]
        total_shares = sum(count for count in shares_counts if count is not None)

        comments_counts = [d.get('comments_count', 0) for d in data]
        total_comments = sum(count for count in comments_counts if count is not None)

        reactions_counts = [d.get('reactions_total_count', 0) for d in data]
        total_reactions = sum(count for count in reactions_counts if count is not None)

        return total_reactions, total_comments, total_shares

    def get_statistics(self):
        data = self.get_combined_data()

        shares_counts = [d.get('shares_count', 0) for d in data]
        total_shares = sum(count for count in shares_counts if count is not None)

        comments_counts = [d.get('comments_count', 0) for d in data]
        total_comments = sum(count for count in comments_counts if count is not None)

        reactions_counts = [d.get('reactions_total_count', 0) for d in data]
        total_reactions = sum(count for count in reactions_counts if count is not None)

        return total_reactions, total_comments, total_shares

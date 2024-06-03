import logging
from itertools import chain

from src.services.account import Project
from src.services.apis import api

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Hashtags:
    def __init__(self, current_user):
        self.current_user = current_user
        self.hashtag_data = []

    def hashtags_data(self):
        projects = Project.all(self.current_user)

        for project in projects:
            if not project:
                continue

            items = api.search_keyword(project.name)
            if items and "keyword" in items and "recommendations" in items:
                self.hashtag_data.extend(items["recommendations"])

    def get_hashtag_data(self):
        self.hashtags_data()
        return self.hashtag_data


class Comments:
    def __init__(self, current_user):
        self.current_user = current_user
        self.comment_data = []

    def comments_data(self):
        projects = Project.all(self.current_user)

        for project in projects:
            if not project:
                continue

            items = api.search_comments(project.name)
            print("items -->", items)
            self.comment_data.extend(items)

    def get_comments_data(self):
        self.comments_data()
        return self.comment_data

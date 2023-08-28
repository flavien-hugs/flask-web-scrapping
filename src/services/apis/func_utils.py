from flask import current_app


app = current_app._get_current_object()

api_base_url = app.config["API_BASE_URL"]
ACCESS_TOKEN = app.config["API_ACCESS_TOKEN"]

INSTAGRAM_BASE_URL = f"{api_base_url}instagram/"
FACEBOOK_BASE_URL = f"{api_base_url}facebook/"

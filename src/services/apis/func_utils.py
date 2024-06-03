from flask import current_app


app = current_app._get_current_object()

api_base_url = app.config["API_BASE_URL"]
ACCESS_TOKEN = app.config["API_ACCESS_TOKEN"]

HASHTAGS = f"{api_base_url}/hashtags"
COMMENTS = f"{api_base_url}/comments"

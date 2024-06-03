from http import HTTPStatus

from flask import abort
from src.services.account import Project
from src.services.account import User


def abort_if_user_doesnt_exist(public_id: str):
    user = User.find_by_public_id(public_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, f"Could not find user with ID {public_id}")
    return user


def abort_if_project_doesnt_exist(public_id: str):
    project = Project.find_by_public_id(public_id)
    if not project:
        abort(HTTPStatus.NOT_FOUND, f"Could not find project with ID {public_id}")
    return project

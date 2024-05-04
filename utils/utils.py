from . import constants as constants

import requests

# TODO: make these api calls resistant to failures/unexpected key types

def api_get_question_info(title_slug):
    return requests.get(f"{constants.API_BASE_LINK}/select?titleSlug={title_slug}")

def api_get_user_contest_info(user_name):
    return requests.get(f"{constants.API_BASE_LINK}/{user_name}/contest")
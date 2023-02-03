# -*- coding: utf-8 -*-

from mastodon import Mastodon
from mastodon import MastodonError

import logging

from config_mastodon_auth import ACCESS_TOKEN, BASE_URL

_FIRST_TOOT_ID = 1
_SERVER_TIMEOUT = 30


def mastodon_connect():
    return Mastodon(access_token=ACCESS_TOKEN, api_base_url=BASE_URL, request_timeout=_SERVER_TIMEOUT)


def get_user_id(mastodon_client, user_name):

    if mastodon_client is None:
        return None

    try:
        user_account = mastodon_client.account_lookup(user_name)
    except MastodonError as e:
        logging.error("Mastodon get user API error: {}".format(e))
        return None

    return user_account['id']


def get_user_status(mastodon_client, user_id, last_id=_FIRST_TOOT_ID):

    max_statuses_at_time = 6

    if mastodon_client is None or user_id is None:
        return None

    try:
        user_statuses = mastodon_client.account_statuses(user_id,
                                                         since_id=last_id,
                                                         limit=max_statuses_at_time,
                                                         local=True,
                                                         exclude_replies=True,
                                                         exclude_reblogs=True)

        toots_count = len(user_statuses)

        if toots_count <= 0:
            logging.debug("No statuses return from id:{:s}".format(user_id))
            return None

    except MastodonError as e:
        logging.error("Mastodon get status API error: {}".format(e))
        return None

    toots = list(map(lambda status: {'id': status['id'], 'text': status['content'],
                                     'url': status['media_attachments']['url']
                                     if len(status['media_attachments']) else None},
                     user_statuses))

    if max_statuses_at_time < toots_count:
        logging.debug("Too much statuses return from id:{:s}".format(user_id))
        toots = (toots[0],)

    return toots

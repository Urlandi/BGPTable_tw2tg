# -*- coding: utf-8 -*-

from birdy.twitter import UserClient
from birdy.twitter import BirdyException

import logging

from config_twitter_auth import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

_FIRST_TWEET_ID = 1


def twitter_connect():
    return UserClient(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def get_user_status(birdy_client, user_screen_name, last_id=_FIRST_TWEET_ID):

    only_last_tweet = 1

    try:
        user_status = birdy_client.api.statuses.user_timeline
        user_status_last = user_status.get(screen_name=user_screen_name,
                                           count=only_last_tweet,
                                           since_id=last_id,
                                           trim_user="true",
                                           tweet_mode="extended")

        if len(user_status_last.data) != 1:
            logging.debug("No status return from @{:s}".format(user_screen_name))
            return None, None

    except BirdyException as e:
        logging.error("Birdy twitter API error: {}".format(e))
        return None, None

    tweet = user_status_last.data[0]
    return tweet.id, tweet.full_text

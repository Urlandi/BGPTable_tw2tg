# -*- coding: utf-8 -*-

from birdy.twitter import UserClient
from birdy.twitter import BirdyException

import logging

from config_twitter_auth import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

_FIRST_TWEET_ID = 1


def twitter_connect():
    return UserClient(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def get_user_status(birdy_client, user_screen_name, last_id=_FIRST_TWEET_ID):

    max_statuses_at_time = 6

    try:
        user_status = birdy_client.api.statuses.user_timeline
        user_status_last = user_status.get(screen_name=user_screen_name,
                                           count=max_statuses_at_time,
                                           since_id=last_id,
                                           trim_user="true",
                                           tweet_mode="extended")

        tweets = user_status_last.data
        tweets_count = len(tweets)

        if tweets_count <= 0:
            logging.debug("No statuses return from @{:s}".format(user_screen_name))
            return None

    except BirdyException as e:
        logging.error("Birdy twitter API error: {}".format(e))
        return None

    if max_statuses_at_time < tweets_count:
        logging.debug("Too much statuses return from @{:s}".format(user_screen_name))
        tweets = (tweets[0],)

    return tweets

# -*- coding: utf-8 -*-
from threading import Timer
from datetime import datetime

from twitter_api import get_user_status, twitter_connect
from subscribers_db import save_bgp_table_status, subscriber_v4_add, subscriber_v6_add, subscribers_flush

from telegram_bot import telegram_connect
from telegram_bot_handlers import update_status_all_v4, update_status_all_v6


from db_api import db_connect, db_close, load_bgp_table_status, load_subscribers, base_dirname

import logging

repost_task = None


def scheduler(db,  bot,
              bgp4_last_tweet, bgp6_last_tweet,
              bgp4_next_update=True, bgp6_next_update=True,
              repeated=0):

    birdy_client = twitter_connect()

    bgp4_table_name = "bgp4_table"
    bgp4_current_tweet = bgp4_last_tweet
    tweet4_fetch_error = False

    if bgp4_next_update:
        bgp4_tweets = get_user_status(birdy_client, bgp4_table_name, bgp4_last_tweet['id'])
        if bgp4_tweets is None:
            tweet4_fetch_error = True
        else:
            for bgp4_tweet in reversed(bgp4_tweets):
                bgp4_current_tweet['id'] = bgp4_tweet.id
                bgp4_current_tweet['text'] = bgp4_tweet.full_text
                update_status_all_v4(bot, bgp4_current_tweet)

    bgp6_table_name = "bgp6_table"
    bgp6_current_tweet = bgp6_last_tweet
    tweet6_fetch_error = False

    if bgp6_next_update:
        bgp6_tweets = get_user_status(birdy_client, bgp6_table_name, bgp6_last_tweet['id'])
        if bgp6_tweets is None:
            tweet6_fetch_error = True
        else:
            for bgp6_tweet in reversed(bgp6_tweets):
                bgp6_current_tweet['id'] = bgp6_tweet.id
                bgp6_current_tweet['text'] = bgp6_tweet.full_text
                update_status_all_v6(bot, bgp6_current_tweet)

    in_5_min = 300
    in_a_half = 1800

    max_fetch_repeat = 1

    next_start_in = in_a_half

    repeat_count = 0
    bgp4_need_update = True
    bgp6_need_update = True

    if max_fetch_repeat <= repeated:
        next_start_in = in_a_half
    elif tweet4_fetch_error or tweet6_fetch_error:
        next_start_in = in_5_min
        repeat_count = repeated + 1
        bgp4_need_update = tweet4_fetch_error
        bgp6_need_update = tweet6_fetch_error

    save_bgp_table_status(bgp4_current_tweet, bgp6_current_tweet, db)

    internet_wait = 30
    timenow = round(datetime.now().timestamp())
    timer_start_at = (timenow // next_start_in + 1) * next_start_in - timenow + internet_wait

    global repost_task
    repost_task = Timer(timer_start_at, scheduler, (db, bot,
                                                    bgp4_current_tweet, bgp6_current_tweet,
                                                    bgp4_need_update, bgp6_need_update,
                                                    repeat_count))
    repost_task.start()

    return 0


DONE = 0
STOP_AND_EXIT = 1


def main():

    exit_status_code = DONE

    _logging_file_name = base_dirname + "bgptable_tw2tg.log"
    logging.basicConfig(filename=_logging_file_name,
                        level=logging.INFO,
                        format="'%(asctime)s: %(name)s-%(levelname)s: %(message)s'")

    logging.debug("Database opening")
    subscribers_database = db_connect()
    if subscribers_database is None:
        exit_status_code = STOP_AND_EXIT
        return exit_status_code
    logging.debug("Database opened")

    logging.debug("Database status loading")
    bgp4_last_status, bgp6_last_status = load_bgp_table_status(subscribers_database)
    if bgp4_last_status is None or bgp6_last_status is None:
        exit_status_code = STOP_AND_EXIT
        return exit_status_code
    logging.debug("Database status loaded")

    logging.debug("Database subscribers loading")
    subscribers_v4 = load_subscribers("IPV4", subscribers_database)
    subscribers_v6 = load_subscribers("IPV6", subscribers_database)

    if subscribers_v4 is None:
        logging.info("Empty v4 subscribers database have been loaded")
    else:
        for subscriber_v4_id in subscribers_v4:
            subscriber_v4_add(subscriber_v4_id)

    if subscribers_v6 is None:
        logging.info("Empty v6 subscribers database have been loaded")
    else:
        for subscriber_v6_id in subscribers_v6:
            subscriber_v6_add(subscriber_v6_id)

    logging.debug("Database subscribers loaded")

    logging.debug("Telegram connecting")
    telegram_job = telegram_connect()
    if telegram_job is None:
        exit_status_code = STOP_AND_EXIT
        return exit_status_code
    logging.debug("Telegram bot started")

    logging.debug("Scheduler job starting")
    if scheduler(subscribers_database, telegram_job.bot, bgp4_last_status, bgp6_last_status) != DONE:
        exit_status_code = STOP_AND_EXIT
        return exit_status_code
    logging.debug("Scheduler job run")

    telegram_job.idle()

    global repost_task
    if repost_task.is_alive():
        repost_task.cancel()

    subscribers_flush(subscribers_database)
    db_close(subscribers_database)

    return exit_status_code


if __name__ == '__main__':
    exit(main())

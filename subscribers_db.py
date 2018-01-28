# -*- coding: utf-8 -*-

import db_api

_bgp4table_status = 1
_bgp6table_status = 1

_subscribers_v4 = set()
_subscribers_v6 = set()

tablev4_selector_checked = "v4_checked"
tablev6_selector_checked = "v6_checked"

tablev4_selector_unchecked = "v4_unchecked"
tablev6_selector_unchecked = "v6_unchecked"


def subscriber_v4_add(subscriber_id):
    global _subscribers_v4

    _subscribers_v4.add(subscriber_id)


def subscriber_v6_add(subscriber_id):
    global _subscribers_v6

    _subscribers_v6.add(subscriber_id)


def _subscribers_rem(subscriber_id, subscribers):

    if 0 < len(subscribers) and _is_subscriber(subscriber_id, subscribers):
        subscribers.remove(subscriber_id)


def subscriber_v4_rem(subscriber_id):
    global _subscribers_v4

    _subscribers_rem(subscriber_id, _subscribers_v4)


def subscriber_v6_rem(subscriber_id):
    global _subscribers_v6

    _subscribers_rem(subscriber_id, _subscribers_v6)


def subscriber_start(subscriber_id):
    global _subscribers_v4
    global _subscribers_v6

    subscriber_v4_add(subscriber_id)
    subscriber_v6_add(subscriber_id)
    db_api.save_subscriber(is_subscriber_v4(subscriber_id),
                           is_subscriber_v6(subscriber_id),
                           subscriber_id)


def subscriber_stop(subscriber_id):
    global _subscribers_v4
    global _subscribers_v6

    subscriber_v4_rem(subscriber_id)
    subscriber_v6_rem(subscriber_id)
    db_api.delete_subscriber(subscriber_id)


def _is_subscriber(subscriber_id, subscribers):
    subscription = subscriber_id in subscribers
    return subscription


def is_subscriber_v4(subscriber_id):
    global _subscribers_v4

    return _is_subscriber(subscriber_id, _subscribers_v4)


def is_subscriber_v6(subscriber_id):
    global _subscribers_v6

    return _is_subscriber(subscriber_id, _subscribers_v6)


def save_bgp_table_status(bgp4_status, bgp6_status, db):
    global _bgp4table_status
    global _bgp6table_status

    _bgp4table_status = bgp4_status
    _bgp6table_status = bgp6_status

    db_api.save_bgp_table_status(bgp4_status, bgp6_status, db)


def get_bgp_table_status():
    global _bgp4table_status
    global _bgp6table_status

    return _bgp4table_status, _bgp6table_status


def get_subscribers_v4():
    global _subscribers_v4

    return _subscribers_v4


def get_subscribers_v6():
    global _subscribers_v6

    return _subscribers_v6


def subscriber_update(query, subscriber_id):
    global _subscribers_v4
    global _subscribers_v6

    if query == tablev4_selector_checked:
        subscriber_v4_add(subscriber_id)
    elif query == tablev6_selector_checked:
        subscriber_v6_add(subscriber_id)
    elif query == tablev4_selector_unchecked:
        subscriber_v4_rem(subscriber_id)
    elif query == tablev6_selector_unchecked:
        subscriber_v6_rem(subscriber_id)

    db_api.save_subscriber(is_subscriber_v4(subscriber_id),
                           is_subscriber_v6(subscriber_id),
                           subscriber_id)


def subscribers_flush(db):
    global _bgp4table_status
    global _bgp6table_status

    db_api.save_subscribers(_subscribers_v4, _subscribers_v6, db)
    db_api.save_bgp_table_status(_bgp4table_status, _bgp6table_status, db)

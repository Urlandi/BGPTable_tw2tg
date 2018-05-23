# -*- coding: utf-8 -*-

import sqlite3 as db_api
import logging

import os
from sys import argv

SUBSCRIBERS_DATABASE_NAME = "subscribers.sqlite3"

ERROR_STATE = None
SUCCESS_STATE = 0

base_dirname = os.path.abspath(os.path.dirname(argv[0])) + "/"

_database_global_handler = None


def db_connect(db_name=base_dirname+SUBSCRIBERS_DATABASE_NAME):

    db = None

    try:
        db = db_api.connect(db_name, check_same_thread=False)
    except db_api.DatabaseError as e:
        logging.critical("Database open error - {}".format(e))
        return None

    global _database_global_handler
    _database_global_handler = db

    return _database_global_handler


def save_bgp_table_status(bgp4table_status, bgp6table_status, subscribers_db=None):

    if subscribers_db is None:
        if _database_global_handler is None:
            return ERROR_STATE
        else:
            db = _database_global_handler
    else:
        db = subscribers_db

    db_query = "UPDATE status SET IPV4 = {:d}, IPV6 = {:d}, IPV4_TEXT = '{:s}', IPV6_TEXT = '{:s}'".format(
        bgp4table_status['id'], bgp6table_status['id'],
        bgp4table_status['text'], bgp6table_status['text'],
    )

    try:
        db_cursor = db.cursor()
        db_cursor.execute(db_query)
        db.commit()

    except db_api.DatabaseError as e:
        db.rollback()
        logging.critical("Database update error - {}".format(e))
        return ERROR_STATE

    return SUCCESS_STATE


def load_bgp_table_status(subscribers_db=None):

    if subscribers_db is None:
        if _database_global_handler is None:
            return ERROR_STATE
        else:
            db = _database_global_handler
    else:
        db = subscribers_db

    statuses_fields = ("status.IPV4", "status.IPV6", "status.IPV4_TEXT", "status.IPV6_TEXT")

    db_query = "SELECT {} FROM status LIMIT 1".format(",".join(statuses_fields))

    try:
        db_cursor = db.cursor()
        db_cursor.execute(db_query)

        statuses = db_cursor.fetchone()

    except db_api.DatabaseError as e:
        logging.critical("Database select error - {}".format(e))
        return ERROR_STATE, ERROR_STATE

    if statuses is None or len(statuses) == 0:
        logging.critical("Database BGP statuses returned empty data")
        return ERROR_STATE, ERROR_STATE

    bgp4_status = dict()
    bgp6_status = dict()

    bgp4_status['id'] = statuses[0]
    bgp4_status['text'] = statuses[2]

    bgp6_status['id'] = statuses[1]
    bgp6_status['text'] = statuses[3]

    return bgp4_status, bgp6_status


def save_subscriber(is_subscriber_v4, is_subscriber_v6, subscriber_id, subscribers_db=None):

    if subscribers_db is None:
        if _database_global_handler is None:
            return ERROR_STATE
        else:
            db = _database_global_handler
    else:
        db = subscribers_db

    db_query_insert = "INSERT INTO subscribers(subscriber_id, IPV4, IPV6) VALUES({:d},{:d},{:d})".format(
        subscriber_id,
        is_subscriber_v4,
        is_subscriber_v6)

    db_query = "UPDATE subscribers SET subscriber_id = {0:d}, IPV4 = {1:d}, IPV6 = {2:d} \
    WHERE subscriber_id={0:d}" .format(
        subscriber_id,
        is_subscriber_v4,
        is_subscriber_v6)

    subscriber_exist = False

    db_cursor = db.cursor()

    try:
        db_cursor.execute(db_query_insert)
        db.commit()
    except db_api.IntegrityError as e:
        db.rollback()
        subscriber_exist = True
    except db_api.DatabaseError as e:
        db.rollback()
        logging.critical("Database insert error - {}".format(e))
        return ERROR_STATE

    if subscriber_exist:
        try:
            db_cursor.execute(db_query)
            db.commit()
        except db_api.DatabaseError as e:
            db.rollback()
            logging.critical("Database update error - {}".format(e))
            return ERROR_STATE

    return SUCCESS_STATE


def delete_subscriber(subscriber_id, subscribers_db=None):

    if subscribers_db is None:
        if _database_global_handler is None:
            return ERROR_STATE
        else:
            db = _database_global_handler
    else:
        db = subscribers_db

    db_query = "DELETE FROM subscribers WHERE subscriber_id={:d}" .format(subscriber_id)

    try:
        db_cursor = db.cursor()
        db_cursor.execute(db_query)
        db.commit()
    except db_api.DatabaseError as e:
        db.rollback()
        logging.critical("Database subscriber delete error - {}".format(e))
        return ERROR_STATE

    return SUCCESS_STATE


def save_subscribers(subscribers_v4, subscribers_v6, subscribers_db=None):

    if subscribers_db is None:
        if _database_global_handler is None:
            return ERROR_STATE
        else:
            db = _database_global_handler
    else:
        db = subscribers_db

    save_complete_status = SUCCESS_STATE
    subscribers = set().union(subscribers_v4, subscribers_v6)

    for subscriber_id in subscribers:
        is_subscriber_v4 = subscriber_id in subscribers_v4
        is_subscriber_v6 = subscriber_id in subscribers_v4

        if save_subscriber(is_subscriber_v4,
                           is_subscriber_v6,
                           subscriber_id, db) != SUCCESS_STATE:
            save_complete_status = ERROR_STATE

    return save_complete_status


def load_subscribers(table_type, subscribers_db=None):

    if subscribers_db is None:
        if _database_global_handler is None:
            return ERROR_STATE
        else:
            db = _database_global_handler
    else:
        db = subscribers_db

    subscribers = None
    db_query = "SELECT subscribers.subscriber_id FROM subscribers \
WHERE subscribers.{:s} = 1".format(table_type)

    try:
        db_cursor = db.cursor()
        db_cursor.execute(db_query)

        subscribers = db_cursor.fetchall()

    except db_api.DatabaseError as e:
        logging.critical("Database select error - {}".format(e))
        return ERROR_STATE

    if subscribers is None or len(subscribers) == 0:
        logging.critical("Database subscribers returned empty data")
        return ERROR_STATE

    subscriber_ids, = zip(*subscribers)

    return set(subscriber_ids)


def db_close(subscribers_db):

    if subscribers_db is not None:
        subscribers_db.commit()
        subscribers_db.close()

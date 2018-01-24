# -*- coding: utf-8 -*-

import logging

import telegram
import resources_messages

from subscribers_db import subscriber_start, subscriber_stop
from subscribers_db import subscriber_update, is_subscriber_v4, is_subscriber_v6

from subscribers_db import tablev4_selector_checked, tablev6_selector_checked
from subscribers_db import tablev4_selector_unchecked, tablev6_selector_unchecked
from subscribers_db import get_bgp_table_status, get_subscribers_v4, get_subscribers_v6


def start_cmd(bot, update):

    subscriber_id = update.message.from_user.id
    subscriber_start(subscriber_id)

    main_keyboard = telegram.ReplyKeyboardMarkup(resources_messages.main_keyboard_template,
                                                 resize_keyboard="true", one_time_keyboard="true")

    update.message.reply_text(text=resources_messages.start_msg, reply_markup=main_keyboard,
                              parse_mode=telegram.ParseMode.HTML,
                              disable_web_page_preview=True)


def stop_cmd(bot, update):
    subscriber_id = update.message.from_user.id
    subscriber_stop(subscriber_id)

    update.message.reply_text(text=resources_messages.stop_msg,
                              parse_mode=telegram.ParseMode.HTML,
                              disable_web_page_preview=True)


def help_cmd(bot, update):
    update.message.reply_text(text=resources_messages.help_msg,
                              parse_mode=telegram.ParseMode.HTML,
                              disable_web_page_preview=True)


def switch_keyboard(subscriber_id):
    buttonv4_name = resources_messages.switch_buttonv4_name.format(resources_messages.empty_arrow_left,
                                                                   resources_messages.empty_arrow_right)
    buttonv4_selector = tablev4_selector_checked

    buttonv6_name = resources_messages.switch_buttonv6_name.format(resources_messages.empty_arrow_left,
                                                                   resources_messages.empty_arrow_right)
    buttonv6_selector = tablev6_selector_checked

    if is_subscriber_v4(subscriber_id):
        buttonv4_name = resources_messages.switch_buttonv4_name.format(resources_messages.selected_arrow_left,
                                                                       resources_messages.selected_arrow_right)
        buttonv4_selector = tablev4_selector_unchecked

    if is_subscriber_v6(subscriber_id):
        buttonv6_name = resources_messages.switch_buttonv6_name.format(resources_messages.selected_arrow_left,
                                                                       resources_messages.selected_arrow_right)
        buttonv6_selector = tablev6_selector_unchecked

    buttonv4 = telegram.InlineKeyboardButton(buttonv4_name, callback_data=buttonv4_selector)
    buttonv6 = telegram.InlineKeyboardButton(buttonv6_name, callback_data=buttonv6_selector)

    keyboard_template = ((buttonv4,),
                         (buttonv6,),)

    return telegram.InlineKeyboardMarkup(keyboard_template)


def settings_cmd(bot, update):

    if update.message is not None:
        subscriber_id = update.message.from_user.id
        settings_keyboard = switch_keyboard(subscriber_id)
        update.message.reply_text(text=resources_messages.settings_msg,
                                  reply_markup=settings_keyboard,
                                  parse_mode=telegram.ParseMode.HTML,
                                  disable_web_page_preview=True)
    elif update.callback_query is not None:
        subscriber_id = update.callback_query.from_user.id
        subscriber_update(update.callback_query.data, subscriber_id)
        settings_keyboard = switch_keyboard(subscriber_id)
        update.callback_query.message.edit_reply_markup(reply_markup=settings_keyboard)


def echo_cmd(bot, update):
    update.message.reply_text(text=resources_messages.echo_msg,
                              parse_mode=telegram.ParseMode.HTML,
                              disable_web_page_preview=True)


def send_status(bot, subscriber_id, message, status):

    sent = True
    try:
        if status != 1:
            bot.send_message(chat_id=subscriber_id,
                             text=message.format(status),
                             parse_mode=telegram.ParseMode.HTML)

    except (telegram.error.Unauthorized,
            telegram.error.BadRequest,
            telegram.error.ChatMigrated) as e:

        logging.info("{:d} sending stopped because - {}".format(subscriber_id, e))
        sent = False

    except telegram.error as e:

        logging.error("{:d} sending skipping because - {}".format(subscriber_id, e))

    return sent


def last_status_cmd(bot, update):
    subscriber_id = update.message.from_user.id

    bgp4table_status, bgp6table_status = get_bgp_table_status()

    if is_subscriber_v4(subscriber_id):
        send_status(bot, subscriber_id, resources_messages.bgp4_status_msg, bgp4table_status)
    if is_subscriber_v6(subscriber_id):
        send_status(bot, subscriber_id, resources_messages.bgp6_status_msg, bgp6table_status)

    if not is_subscriber_v4(subscriber_id) and not is_subscriber_v6(subscriber_id):
        update.message.reply_text(resources_messages.subscriptions_empty_msg)


def update_status_all_v4(bot, status):

    subscribers_v4 = get_subscribers_v4()
    subscribers_blocked = set()

    for subscriber_id in subscribers_v4:
        if not send_status(bot, subscriber_id, resources_messages.bgp4_status_msg, status):
            subscribers_blocked.add(subscriber_id)

    for subscriber_id in subscribers_blocked:
        subscriber_stop(subscriber_id)


def update_status_all_v6(bot, status):

    subscribers_v6 = get_subscribers_v6()
    subscribers_blocked = set()

    for subscriber_id in subscribers_v6:
        if not send_status(bot, subscriber_id, resources_messages.bgp6_status_msg, status):
            subscribers_blocked.add(subscriber_id)

    for subscriber_id in subscribers_blocked:
        subscriber_stop(subscriber_id)


def telegram_error(bot, update, error):
    logging.error("{} - {}".format(update, error))
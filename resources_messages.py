# -*- coding: utf-8 -*-

keyboard_buttons_name = {"help_name": "Help",
                         "settings_name": "Settings",
                         "last_status_name": "Last status", }

main_keyboard_template = ((keyboard_buttons_name["help_name"], keyboard_buttons_name["settings_name"],),
                          (keyboard_buttons_name["last_status_name"],))


switch_buttonv4_name = "{:s}IPv4 table status{:s}"
switch_buttonv6_name = "{:s}IPv6 table status{:s}"


selected_arrow_left = "[✓] "
selected_arrow_right = ""

empty_arrow_left = "[    ] "
empty_arrow_right = ""

echo_msg = "Unfortunately, I didn't understand what do you mean. \
If you have any questions or notes, \
please contact my author by <a href=\"https://t.me/UrgentPirate\">Telegram</a> \
or by <a href=\"https://github.com/Urlandi/BGPTable_tw2tg/issues\">GitHub</a>.\n\n\
Also the /help command shows some helpful information about me."


settings_msg = "You may choose from which \
<a href=\"https://noc.social/@bgp4\">@bgp4@noc.social</a>, \
<a href=\"https://noc.social/@bgp6\">@bgp6@noc.social</a> or both you'll receive updates."

help_msg = "Hello, I'm a BGP-Table Telegram bot. I am reading the \
<a href=\"https://noc.social/@bgp4\">@bgp4@noc.social</a> \
and the <a href=\"https://noc.social/@bgp6\">@bgp6@noc.social</a> in Mastodon \
and reposting every toot from there. As result you see some statistics about the Internet BGP table state, \
which is collected by <a href=\"https://mastodon.social/@mellowd\">Darren O'Connor</a>, \
these Mastodon bots creator.\n\n\
Please go to the /settings menu, where you can setup which BGP table state v4 or v6 you would like to see. \
The /start command subscribes you to all updates and the /stop unsubscribes and mutes.\n\n\
Updates are sent to you as fast as they appear in the original Mastodon bots, usually every 6 hours. \
The command /status sends the last posted status to the stream.\n\n\
My author @UrgentPirate open for questions and proposals. \
My code is on <a href=\"https://github.com/Urlandi/BGPTable_tw2tg/issues\">GitHub.</a>"

stop_msg = "Unsubscribed. Try the /start or the /settings for return."

start_msg = "Great, now you have been subscribed for all updates. \
Please read the /help page or make your own customization directly via the /settings, if it needed."

subscriptions_empty_msg = "Oops, you haven't any subscriptions now. Go to the /settings menu to fix this. \
If you don't know what can you do, please read the /help page."

bgp4_status_msg = "{:s}{:s}\n<a href=\"https://noc.social/@bgp4/{:d}\">@bgp4@noc.social</a>"
bgp6_status_msg = "{:s}{:s}\n<a href=\"https://noc.social/@bgp6/{:d}\">@bgp6@noc.social</a>"

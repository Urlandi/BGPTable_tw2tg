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

echo_msg = "Unfortunately, I haven't understood what you mean. \
If you have any questions or comments, \
please contact my author on <a href=\"https://t.me/UrgentPirate\">Telegram</a> \
or on <a href=\"https://github.com/Urlandi/BGPTable_tw2tg/issues\">GitHub</a>.\n\n\
Also /help command could show some helpful information about me."


settings_msg = "You may choose from which \
<a href=\"https://twitter.com/bgp4_table\">@BGP4-Table</a>, \
<a href=\"https://twitter.com/bgp6_table\">@BGP6-Table</a>, or both receive updates."

help_msg = "Hello, I'm BGP-Table Telegram bot. I am reading \
<a href=\"https://twitter.com/bgp4_table\">@BGP4-Table</a> \
and <a href=\"https://twitter.com/bgp6_table\">@BGP6-Table</a> in Twitter \
and reposting every tweet from where. As result, you can see some statistics about BGP \
actual table state on Internet, \
which is collected by <a href=\"https://twitter.com/mellowdrifter\">Darren O'Connor</a>, \
the author of this Twitter bots.\n\n\
Please go to /settings menu, where you may setup from which BGP table you want to see data. \
/start command subscribes you to all updates and /stop unsubscribes and mute.\n\n\
Updates are sent to you as fast as they appear in original Twitter bots, usually every 6 hours. \
Command /status sends last posted status to stream.\n\n\
My author @UrgentPirate open for questions and proposals. \
My code may be found on <a href=\"https://github.com/Urlandi/BGPTable_tw2tg/issues\">GitHub.</a>"

stop_msg = "Unsubscribed. Try /start or /settings for return."

start_msg = "Great! Now, you have subscribed то all updates. \
Please, read the /help page or make your own customization directly via /settings, if needed."

subscriptions_empty_msg = "Oops, you haven't any subscriptions now. Go to /settings menu to fix this. \
If you don't know what could you do, please read /help page."

bgp4_status_msg = "{:s}\n<a href=\"https://twitter.com/bgp4_table/status/{:d}\">@BGP4-Table</a>"
bgp6_status_msg = "{:s}\n<a href=\"https://twitter.com/bgp6_table/status/{:d}\">@BGP6-Table</a>"

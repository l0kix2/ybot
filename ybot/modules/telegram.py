# coding: utf-8
from __future__ import absolute_import
import re
import telegram
from ybot.events import emitter, splitter
from ybot.conf import settings

conf = settings[__name__]     # 'ybot.modules.telegram'
bot = telegram.Bot(token=conf['token'])


@emitter('ybot.telegram.message')
def updates():
    timeout = conf.get('polling_timeout', 60)
    offset = None

    while True:
        updates = bot.getUpdates(offset=offset, timeout=timeout) or []
        for update in updates:
            offset = update.update_id + 1
            if update.message:
                yield update.message


@splitter(['ybot.telegram.message'], ['ybot.telegram.command'])
def command_splitter(name, value):
    bot_name = conf.get('bot_name', r'\w{1,32}')
    pattern = r'^/\w+(:?@{name})?( .*)?$'.format(name=bot_name)

    if re.match(pattern, value.text):
        yield ('ybot.telegram.command', value)

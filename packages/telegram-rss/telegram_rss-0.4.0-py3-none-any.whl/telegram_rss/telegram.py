import logging
from telegram import Bot, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from time import sleep
from typing import List

from telegram_rss.config import Config, FeedConfig
from telegram_rss.feed import Entry, FeedUpdater

logger = logging.getLogger(__name__)


def make_reply_markup(text: str, link: str):
    keyboard = [[InlineKeyboardButton(text=text, url=link)]]
    return InlineKeyboardMarkup(keyboard)


def send_message(
    bot: Bot,
    entry: Entry,
    chat_ids: List[int],
    updater: FeedUpdater,
    config: Config,
    feed_config: FeedConfig,
    message_delay: float,
):
    read_more = feed_config.read_more_button or config.read_more_button
    web_page_preview = feed_config.web_page_preview or config.web_page_preview

    message = str(entry)
    if config.author_text:
        message += f"\n<i>{config.author_text}</i>: {entry.author}"
    if feed_config.footer:
        title = feed_config.footer_name or (
            updater.channel.title if updater.channel else feed_config.name
        )
        if feed_config.footer_link:
            title = f'<a href="{feed_config.footer_link}">{title}</a>'
        message += "\n" + f"<i>{config.channel_text}</i>: {title}"

    if read_more:
        reply_markup = make_reply_markup(read_more, entry.link)
    else:
        reply_markup = None
    for chat_id in chat_ids:
        bot.send_message(
            chat_id,
            text=message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=not web_page_preview,
        )
        sleep(message_delay)


def send_update(bot: Bot, config: Config):
    chat_ids = config.channels + config.users
    for feed_config in config.feeds:
        message_delay = feed_config.message_delay or config.message_delay
        updater = FeedUpdater(feed_config)
        entries = updater.get_new_entries()
        if not entries:
            continue
        entries.reverse()

        for entry in entries:
            send_message(
                bot=bot,
                entry=entry,
                chat_ids=chat_ids,
                updater=updater,
                config=config,
                feed_config=feed_config,
                message_delay=message_delay,
            )
        sleep(message_delay)

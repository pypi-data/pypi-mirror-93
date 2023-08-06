from __future__ import annotations
import logging
from aiogram import Bot, Dispatcher, executor


class Telegram:
    """
    A simple configurable Telegram bot, wrapped Aiogram.
    """
    __bot_token: str
    _bot: Bot
    _dp: Dispatcher

    def __init__(self, bot_token: str):
        self.__bot_token = bot_token
        self.set_logging()
        self._initiate_bot()
        self._initiate_dp()

    def set_logging(self, level: int = logging.INFO):
        """
        Set the logging.
        """
        logging.basicConfig(level=level)
        logging.debug("Initiated logging.")

    def _initiate_bot(self):
        self.bot = Bot(token=self.__bot_token)
        logging.debug("Initiated Telegram bot.")

    def _initiate_dp(self):
        self.dp = Dispatcher(self.bot)
        logging.debug("Initiated the dispatcher of Telegram bot.")

    def get_bot(self) -> Bot:
        """
        Get the instanced bot.
        """
        return self._bot

    def get_dp(self) -> Dispatcher:
        """
        Get the dispatcher of the instanced bot.
        """
        return self._dp

    def polling(self) -> None:
        executor.start_polling(self._dp, skip_updates=True)  # type: ignore

from __future__ import annotations
import asyncio
from asyncio.events import AbstractEventLoop
from asyncio.tasks import Task
import logging
from typing import Any
from aiogram import Bot, Dispatcher


class Telegram:
    """
    A simple configurable Telegram bot, wrapped Aiogram.
    """
    __bot_token: str
    _bot: Bot
    _dp: Dispatcher
    _loop: AbstractEventLoop

    def __init__(self, bot_token: str):
        self.__bot_token = bot_token
        self._loop = asyncio.get_event_loop()
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

    def start_polling(self) -> Task[Any]:
        """
        Start polling. Returns the created task.
        """
        return self._loop.create_task(self._dp.start_polling())  # type: ignore 

    def stop_polling(self) -> None:
        """
        Stop polling.
        """
        self._dp.stop_polling()  # type: ignore
    
    async def stop_bot(self) -> None:
        """
        Stop Bot.
        """
        await self._dp.wait_closed()  # type: ignore 
        await self._bot.close()

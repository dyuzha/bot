# bot/__init__.py

import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from bot.config_handlers import TELEGRAM_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers.deffault import router as deffault_router
from bot.handlers.tickets import router as tickets_router
from bot.handlers.navigation import router as navigation_router
from bot.handlers.universal import router as universal_router
from bot.handlers.one_c_handlers import router as one_c_router
from bot.handlers.final import router as final_router
# from bot.middlewares.navigation import NavigationMiddleware
from bot.middlewares.post_navigation import NavigationMiddleware


logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML))

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрируем middlewares
# dp.update.outer_middleware(NavigationMiddleware())
# tickets_router.message.outer_middleware(MessageNavigationMiddleware())
tickets_router.callback_query.outer_middleware(NavigationMiddleware())


dp.include_router(universal_router)
dp.include_router(navigation_router)
dp.include_router(deffault_router)
dp.include_router(tickets_router)
dp.include_router(one_c_router)
# dp.include_router(final_router)


# Регистрируем обработчики
from .handlers import *

# Регистрируем меню бота
from .menu import set_bot_commands

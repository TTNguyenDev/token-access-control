from aiogram import Dispatcher
from aiogram_newsletter.handlers import AiogramNewsletterHandlers
from aiogram_tonconnect.handlers import AiogramTonConnectHandlers

from . import admin
from . import public
from . import chats
from . import private
from . import errors


def bot_routers_include(dp: Dispatcher) -> None:
    """
    Include bot routers.
    """
    dp.include_routers(
        *[
            admin.command.router,
            private.command.router,
            public.verify.router,
        ],
    )

    AiogramNewsletterHandlers().register(dp)
    AiogramTonConnectHandlers().register(dp)

    dp.include_routers(
        *[
            errors.router,
            admin.callback_query.router,
            private.callback_query.router,
            admin.message.router,
            private.message.router,
            private.my_chat_member.router,
            chats.my_chat_member.router,
        ]
    )


__all__ = [
    "bot_routers_include",
]

from contextlib import suppress
from typing import List

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    BotCommandScopeAllPrivateChats,
    BotCommand,
    BotCommandScopeChat,
)


async def bot_commands_setup(bot: Bot) -> None:
    """
    Setup bot commands.

    :param bot: The Bot object.
    """
    commands = {
        "en": [
            BotCommand(command="start", description="Restart bot"),
            BotCommand(
                command="start_verification",
                description="Start verification process",
            ),
            BotCommand(
                command="complete_verification",
                description="Complete verification process",
            ),
        ],
        "ru": [
            BotCommand(command="start", description="Перезапустить бота"),
            BotCommand(
                command="start_verification",
                description="Start verification process",
            ),
            BotCommand(
                command="complete_verification",
                description="Complete verification process",
            ),
        ],
    }

    # Set commands for all private chats in English language
    await bot.set_my_commands(
        commands=commands["en"],
        scope=BotCommandScopeAllPrivateChats(),
    )
    # Set commands for all private chats in Russian language
    await bot.set_my_commands(
        commands=commands["ru"],
        scope=BotCommandScopeAllPrivateChats(),
        language_code="ru",
    )


async def bot_commands_delete(bot: Bot) -> None:
    """
    Delete bot commands.

    :param bot: The Bot object.
    """

    # Delete commands for all private chats in any language
    await bot.delete_my_commands(
        scope=BotCommandScopeAllPrivateChats(),
    )
    # Delete commands for all private chats in Russian language
    await bot.delete_my_commands(
        scope=BotCommandScopeAllPrivateChats(),
        language_code="ru",
    )


async def bot_admin_commands_setup(bot, admins_ids: List[int]) -> None:
    """
    Setup bot admin commands.

    :param bot: The Bot object.
    :param admins_ids: List of admin IDs.
    """
    admin_commands = {
        "en": [
            BotCommand(command="start", description="Restart bot"),
            BotCommand(command="admin", description="Admin panel"),
        ],
        "ru": [
            BotCommand(command="start", description="Перезапустить бота"),
            BotCommand(command="admin", description="Панель администратора"),
        ],
    }

    # Set commands for all admin chats
    for admin_id in admins_ids:
        with suppress(TelegramBadRequest):
            await bot.set_my_commands(
                commands=admin_commands["en"],
                scope=BotCommandScopeChat(chat_id=admin_id),
            )
        with suppress(TelegramBadRequest):
            await bot.set_my_commands(
                commands=admin_commands["ru"],
                scope=BotCommandScopeChat(chat_id=admin_id),
                language_code="ru",
            )


async def bot_admin_commands_delete(bot, admins_ids: List[int]) -> None:
    """
    Delete bot admin commands.

    :param bot: The Bot object.
    :param admins_ids: List of admin IDs.
    """

    # Delete commands for all admin chats
    for admin_id in admins_ids:
        with suppress(TelegramBadRequest):
            await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=admin_id))
        with suppress(TelegramBadRequest):
            await bot.delete_my_commands(
                scope=BotCommandScopeChat(chat_id=admin_id), language_code="ru"
            )

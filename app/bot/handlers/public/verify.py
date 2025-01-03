from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

import logging
import requests

from ...manager import Manager

router = Router()


@router.message(Command("start_verification"))
async def start_command(message: Message, manager: Manager) -> None:
    sender = message.from_user
    sender_name = sender.full_name

    await message.answer(
        f"Hello {sender_name}, please go to this link to verify: "
        "https://ton-apps.demo.lfg.inc\n"
        "After going to this link, please connect this telegram account and "
        "your ETH wallet, then click `Verify` button, and sign the message.\n"
        "After all, please get back to this bot, and run "
        "`/complete_verification` command to trigger the bot to verify your "
        "NFT ownership.\n"
    )


@router.message(Command("complete_verification"))
async def complete_command(message: Message, manager: Manager) -> None:
    sender = message.from_user
    sender_username = sender.username
    sender_name = sender.full_name

    try:
        response = fetch_membership(sender_username)
        if response.status_code == 200:
            data = response.json()
            if data.get("ownNft", False):
                await message.answer(
                    f"Hi {sender_name}, you have verified your NFT "
                    "ownership successfully."
                )
            else:
                await message.answer(
                    f"Hi {sender_name}, the ETH address "
                    f"{data.get('ethAddress', 'NaN')} you linked does not "
                    "have the NFT yet. Please get the NFT and run this "
                    "command again."
                )
        elif response.status_code == 404:
            await message.answer(
                f"Hi {sender_name}, it seems you have not verified your NFT "
                "ownership yet. Please complete the verification process first."
            )
        else:
            logging.error(
                f"Unexpected Error - Status Code: {response.status_code}, "
                f"Response: {response.text}"
            )
            await message.answer(
                f"Hi {sender_name}, there was an error in the system. "
                "Please try again later."
            )
    except Exception as e:
        logging.exception("An unexpected error occurred while processing the command.")
        await message.answer(
            f"Hi {sender_name}, an unexpected error occurred. "
            f"Please try again later. Error: {e}"
        )


def fetch_membership(username: str) -> requests.Response:
    url = "https://ton-app.lfg.suipass.xyz/api/member"
    params = {
        "telegramUsername": username,
        "refetchOwnership": "true",
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            logging.info("DEBUG Response data: %s", response.json())
        return response
    except requests.RequestException as e:
        logging.error(f"DEBUG Error while making request: {e}")
        raise


# async def command(message: Message, manager: Manager) -> None:
#     sender = message.from_user
#     sender_username = sender.username
#     sender_name = sender.full_name
#
#     response = fetch_membership(sender_username)
#     await message.answer(
#         f"Hi {sender_name}, command received: /verify, REceive REsponse: {response.json()}"
#     )
#
#
# def fetch_membership(username: str) -> any:
#     url = "https://ton-app.lfg.suipass.xyz/api/member"
#     params = {
#         "telegramUsername": username,
#         "refetchOwnership": "true",
#     }
#     response = requests.get(url, params=params)
#
#     if response.status_code == 200:
#         logging.info("DEBUG Response data:", response)
#         return response
#     else:
#         logging.error(f"DEBUG Error: {response.status_code}, {response.text}")
#         return response

import asyncio
import html
import json
import tempfile
import traceback
from pathlib import Path
from uuid import uuid4

import aiohttp
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile

from config import (
    DEV_PASS_DATA,
    ENV,
    HTTP_TIMEOUT_SECONDS,
    MOBIFITNESS_ACCEPT_LANGUAGE,
    MOBIFITNESS_API_BASE,
    MOBIFITNESS_BEARER_TOKEN,
    MOBIFITNESS_EXTERNAL_CLIENT_ID,
    MOBIFITNESS_PASS_PATH,
    MOBIFITNESS_USER_AGENT,
    MOBIFITNESS_X_CUSTOM_BUILD,
    MOBIFITNESS_X_CUSTOM_OS,
    MOBIFITNESS_X_CUSTOM_VERSION,
)
from core import logger


async def get_qr() -> tuple[FSInputFile, int, Path]:
    if ENV == "dev":
        data = DEV_PASS_DATA
    else:
        headers = {
            "Authorization": f"Bearer {MOBIFITNESS_BEARER_TOKEN}",
            "X-CustomOS": MOBIFITNESS_X_CUSTOM_OS,
            "X-CustomVersion": MOBIFITNESS_X_CUSTOM_VERSION,
            "X-CustomBuild": MOBIFITNESS_X_CUSTOM_BUILD,
            "User-Agent": MOBIFITNESS_USER_AGENT,
            "Accept-Language": MOBIFITNESS_ACCEPT_LANGUAGE,
            "X-CustomData": json.dumps({"externalClientId": MOBIFITNESS_EXTERNAL_CLIENT_ID}),
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
        }

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=HTTP_TIMEOUT_SECONDS)
        ) as session:
            async with session.get(
                f"{MOBIFITNESS_API_BASE.rstrip('/')}/{MOBIFITNESS_PASS_PATH.lstrip('/')}",
                headers=headers,
            ) as response:
                response.raise_for_status()
                data = await response.json(content_type=None)

    qr_path = Path(tempfile.gettempdir()) / f"gym-pass-{uuid4().hex}.png"
    process = await asyncio.create_subprocess_exec(
        "qrencode",
        "-o", str(qr_path),
        "-s", "20",

        str(data["code"]),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(stderr.decode("utf-8", errors="ignore").strip() or "qrencode failed")
    if not qr_path.exists():
        raise FileNotFoundError(f"qrencode did not create file: {qr_path}")

    return FSInputFile(qr_path), int(data["validTime"]), qr_path


async def send_error(bot, chat_id: int, error: Exception) -> None:
    logger.error("Bot flow error", exc_info=(type(error), error, error.__traceback__))
    trace = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    await bot.send_message(
        chat_id,
        f"Ошибка:\n<pre>{html.escape(trace[-3500:])}</pre>",
        parse_mode=ParseMode.HTML,
    )

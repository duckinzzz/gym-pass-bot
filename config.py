import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID_RAW = os.getenv("ADMIN_ID")
ENV = os.getenv("ENV", "prod").lower()
MOBIFITNESS_API_BASE = os.getenv("MOBIFITNESS_API_BASE")
MOBIFITNESS_PASS_PATH = os.getenv("MOBIFITNESS_PASS_PATH")
MOBIFITNESS_BEARER_TOKEN = os.getenv("MOBIFITNESS_BEARER_TOKEN")
MOBIFITNESS_EXTERNAL_CLIENT_ID = os.getenv("MOBIFITNESS_EXTERNAL_CLIENT_ID")
MOBIFITNESS_X_CUSTOM_OS = os.getenv("MOBIFITNESS_X_CUSTOM_OS")
MOBIFITNESS_X_CUSTOM_VERSION = os.getenv("MOBIFITNESS_X_CUSTOM_VERSION")
MOBIFITNESS_X_CUSTOM_BUILD = os.getenv("MOBIFITNESS_X_CUSTOM_BUILD")
MOBIFITNESS_USER_AGENT = os.getenv("MOBIFITNESS_USER_AGENT")
MOBIFITNESS_ACCEPT_LANGUAGE = os.getenv("MOBIFITNESS_ACCEPT_LANGUAGE")

HTTP_TIMEOUT_SECONDS = 15.0
START_MESSAGE_TEXT = "ㅤ"
QR_EXPIRED_TEXT = "КОД ИСТЕК"
REFRESH_BUTTON_TEXT = "Обновить QR-код"
DEV_PASS_DATA = {
    "code": "aboba",
    "type": "default",
    "validTime": 5,
    "validThru": "2026-03-19T17:43:21+10:00",
}

if not BOT_TOKEN or BOT_TOKEN == "NO_TOKEN":
    raise ValueError("BOT_TOKEN not found")

if not ADMIN_ID_RAW:
    raise ValueError("ADMIN_ID not found")

if ENV not in {"dev", "prod"}:
    raise ValueError("ENV must be 'dev' or 'prod'")

ADMIN_ID = int(ADMIN_ID_RAW)

_required_values = {
    "MOBIFITNESS_API_BASE": MOBIFITNESS_API_BASE,
    "MOBIFITNESS_PASS_PATH": MOBIFITNESS_PASS_PATH,
    "MOBIFITNESS_BEARER_TOKEN": MOBIFITNESS_BEARER_TOKEN,
    "MOBIFITNESS_EXTERNAL_CLIENT_ID": MOBIFITNESS_EXTERNAL_CLIENT_ID,
    "MOBIFITNESS_X_CUSTOM_OS": MOBIFITNESS_X_CUSTOM_OS,
    "MOBIFITNESS_X_CUSTOM_VERSION": MOBIFITNESS_X_CUSTOM_VERSION,
    "MOBIFITNESS_X_CUSTOM_BUILD": MOBIFITNESS_X_CUSTOM_BUILD,
    "MOBIFITNESS_USER_AGENT": MOBIFITNESS_USER_AGENT,
    "MOBIFITNESS_ACCEPT_LANGUAGE": MOBIFITNESS_ACCEPT_LANGUAGE,
}

_missing_values = [name for name, value in _required_values.items() if not value]
if ENV == "prod" and _missing_values:
    raise ValueError(f"Missing required .env values: {', '.join(_missing_values)}")

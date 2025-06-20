import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))
BASVURU_KANAL_ID = int(os.getenv("BASVURU_KANAL_ID"))

ADMIN_IDS = [1374472023199318077, 1105511285132636161]

DATA_FILE = "data/bot_data.json"
ORDERS_FILE = "data/siparisler.json"
STATE_FILE = "data/state.json"

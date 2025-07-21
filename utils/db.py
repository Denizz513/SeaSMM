import json
import os
import discord
from config import DATA_FILE, ONAY_KANAL_ID

user_credits = {}
pending_requests = {}
products = {}
orders = {}
bakim_modu = False  # 🧩 Bakım modu buraya eklendi
ADMIN_IDS = [1374472023199318077]

def load_data():
    global user_credits, pending_requests, products, orders, bakim_modu
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            user_credits = {int(k): v for k, v in data.get("user_credits", {}).items()}
            pending_requests = {int(k): v for k, v in data.get("pending_requests", {}).items()}
            products = data.get("products", {})
            orders = {int(k): v for k, v in data.get("orders", {}).items()}
            bakim_modu = data.get("bakim_modu", False)
    else:
        user_credits = {}
        pending_requests = {}
        products = {}
        orders = {}
        bakim_modu = False

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "user_credits": user_credits,
            "pending_requests": pending_requests,
            "products": products,
            "orders": orders,
            "bakim_modu": bakim_modu  # 💾 Bakım modu dosyaya yazılıyor
        }, f, ensure_ascii=False, indent=4)

def log_order(user_id, order_data):
    if user_id not in orders:
        orders[user_id] = []
    orders[user_id].append(order_data)
    save_data()

def get_orders(user_id):
    return orders.get(user_id, [])

# --- Yeni eklenen fonksiyon ---

async def log_odeme_onayi(bot, user: discord.User, miktar: float):
    kanal = bot.get_channel(ONAY_KANAL_ID)
    if kanal:
        await kanal.send(f"✅ {user.mention} adlı kullanıcının **{miktar}** kredilik ödemesi onaylandı.")
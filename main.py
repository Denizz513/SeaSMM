import discord
from discord.ext import commands
from config import TOKEN
from utils import db

# Slash komutlarını desteklemek için tanımlama
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Slash komutlarını senkronize et
@bot.event
async def on_ready():
    print(f"✅ Bot aktif: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"📡 {len(synced)} slash komutu senkronize edildi.")
    except Exception as e:
        print(f"❌ Komut senkronizasyon hatası: {e}")

# Komut dosyalarını yükle
async def load_extensions():
    extensions = [
        "commands.kredi",
        "commands.urun",
        "commands.siparis",
        "commands.siparislerim",
        "commands.yenidenbaslat",
        "commands.urun_kaldir",
        "commands.bakim",
        "commands.urunler",
    ]
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ {ext} yüklendi.")
        except Exception as e:
            print(f"❌ {ext} yüklenemedi: {e}")

# Botu başlat
async def main():
    db.load_data()
    await load_extensions()
    await bot.start(TOKEN)

# Python 3.7+ destekli ana giriş
import asyncio
asyncio.run(main())



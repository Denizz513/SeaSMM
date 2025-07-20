import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import asyncio
from dotenv import load_dotenv

# Load env variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN_IDS = [1374472023199318077, 1105511285132636161]
DATA_FILE = "data/bot_data.json"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="datajson", description="Botun bot_data.json dosyasını DM olarak yollar (sadece adminler)")
    async def datajson(self, interaction: discord.Interaction):
        if interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("⛔ Bu komutu sadece adminler kullanabilir.", ephemeral=True)
            return

        try:
            if not os.path.exists(DATA_FILE):
                await interaction.response.send_message("❌ bot_data.json bulunamadı.", ephemeral=True)
                return

            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            data_str = json.dumps(data, indent=2)
            chunks = [data_str[i:i+1900] for i in range(0, len(data_str), 1900)]

            await interaction.response.send_message("📩 bot_data.json içeriği DM'den gönderildi.", ephemeral=True)

            for chunk in chunks:
                await interaction.user.send(f"```json\n{chunk}\n```")

        except Exception as e:
            await interaction.response.send_message(f"❌ Hata oluştu: {e}", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot aktif: {bot.user}")
    bot.add_cog(AdminCommands(bot))

async def main():
    await bot.start(TOKEN)

asyncio.run(main())
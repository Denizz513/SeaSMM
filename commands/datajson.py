import discord
from discord.ext import commands
from discord import app_commands
import json
import os

from config import ADMIN_IDS, DATA_FILE

class DataJSON(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="datajson", description="Botun içindeki data dosyasını DM ile yollar (admin-only)")
    async def datajson(self, interaction: discord.Interaction):
        if interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("⛔ Bu komutu sadece adminler kullanabilir.", ephemeral=True)
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            data_str = json.dumps(data, indent=2)
            chunks = [data_str[i:i+1900] for i in range(0, len(data_str), 1900)]

            await interaction.response.send_message("📩 Data dosyası DM'den gönderiliyor...", ephemeral=True)

            for chunk in chunks:
                await interaction.user.send(f"```json\n{chunk}\n```")

        except Exception as e:
            await interaction.response.send_message(f"❌ Hata oluştu: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DataJSON(bot))
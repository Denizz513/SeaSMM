import discord
from discord.ext import commands
from discord import app_commands
import json
from config import STATE_FILE, ADMIN_IDS

class BakimDurum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bakim-durum", description="Bakım modunun açık mı kapalı mı olduğunu gösterir.")
    async def bakim_durum(self, interaction: discord.Interaction):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)

        durum = "✅ **Kapalı**" if not state.get("bakim_modu") else "⚠️ **Açık**"
        await interaction.response.send_message(f"🔧 Bakım modu durumu: {durum}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BakimDurum(bot))
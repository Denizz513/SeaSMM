import discord
from discord.ext import commands
from discord import app_commands
from helpers.state import get_bakim_modu
from config import ADMIN_IDS

class BakimDurum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bakim-durum", description="Botun bakımda olup olmadığını gösterir.")
    async def bakim_durum(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        durum = "✅ Kapalı" if not get_bakim_modu() else "⚠️ Açık"
        await interaction.followup.send(f"🔧 Bakım modu durumu: {durum}")

async def setup(bot):
    await bot.add_cog(BakimDurum(bot))
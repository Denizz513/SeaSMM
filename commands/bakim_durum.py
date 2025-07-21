import discord
from discord.ext import commands
from discord import app_commands
from utils import db

class BakimDurum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bakim-durum", description="Bakım modunun açık mı kapalı mı olduğunu gösterir.")
    async def bakim_durum(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        durum = "✅ Kapalı" if not db.bakim_modu else "⚠️ Açık"
        await interaction.followup.send(f"🔧 Bakım modu durumu: {durum}")

async def setup(bot):
    await bot.add_cog(BakimDurum(bot))
import discord
from discord.ext import commands
from discord import app_commands
from utils import db

class BakimDurum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bakim-durum", description="Botun bakım modunda olup olmadığını gösterir.")
    async def bakim_durum(self, interaction: discord.Interaction):
        # ❗ Discord 3 saniye bekler, bu yüzden hemen yanıt ver
        await interaction.response.send_message(
            f"🔧 Bakım modu durumu: {'⚠️ Açık' if db.bakim_modu else '✅ Kapalı'}",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(BakimDurum(bot))
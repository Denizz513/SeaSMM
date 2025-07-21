import discord
from discord.ext import commands
from discord import app_commands
from helpers.state import get_bakim_modu  # ← Dosyanın adı state.py ise bu şekilde import et
from config import ADMIN_IDS

class BakimDurum(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bakim-durum", description="Bakım modunun açık mı kapalı mı olduğunu gösterir.")
    async def bakim_durum(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        try:
            durum_bool = get_bakim_modu()
            durum = "✅ **Kapalı**" if not durum_bool else "⚠️ **Açık**"
            await interaction.followup.send(f"🔧 Bakım modu durumu: {durum}")
        except Exception as e:
            await interaction.followup.send(f"❌ Bir hata oluştu: {e}")

async def setup(bot):
    await bot.add_cog(BakimDurum(bot))
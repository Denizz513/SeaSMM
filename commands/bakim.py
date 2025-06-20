import discord
from discord import app_commands
from discord.ext import commands
from utils import db

class Bakim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bakim_ac", description="Botu bakım moduna alır (Admin)")
    async def bakim_ac(self, interaction: discord.Interaction):
        if interaction.user.id not in db.ADMIN_IDS:
            await interaction.response.send_message("❌ Bu komutu sadece admin kullanabilir.", ephemeral=True)
            return
        db.bakim_modu = True
        await interaction.response.send_message("🛠 Bot artık bakım modunda.")

    @app_commands.command(name="bakim_kapat", description="Bakım modunu kapatır (Admin)")
    async def bakim_kapat(self, interaction: discord.Interaction):
        if interaction.user.id not in db.ADMIN_IDS:
            await interaction.response.send_message("❌ Bu komutu sadece admin kullanabilir.", ephemeral=True)
            return
        db.bakim_modu = False
        await interaction.response.send_message("✅ Bot artık aktif durumda.")

async def setup(bot):
    await bot.add_cog(Bakim(bot))


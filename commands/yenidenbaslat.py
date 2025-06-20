import discord
from discord import app_commands
from discord.ext import commands
from config import ADMIN_IDS
import os
import sys

class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="yenidenbaslat", description="Botu yeniden başlatır (Admin)")
    async def yeniden_baslat(self, interaction: discord.Interaction):
        if interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("<a:iptal:1384601834806706238> Bu komutu kullanmaya yetkin yok.", ephemeral=True)
            return

        await interaction.response.send_message("<a:yukleniyor:1384606847142461490> Bot yeniden başlatılıyor...")

        python = sys.executable
        os.execl(python, python, *sys.argv)

async def setup(bot):
    await bot.add_cog(Restart(bot))

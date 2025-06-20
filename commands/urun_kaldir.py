import discord
from discord import app_commands
from discord.ext import commands
from config import ADMIN_IDS
from utils import db

class UrunKaldir(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if db.bakim_modu and interaction.user.id not in db.ADMIN_IDS:
            await interaction.response.send_message("<a:bakimda:1384602567169937580> Bot şu anda bakımda. Daha sonra tekrar dene.", ephemeral=True)
            return False
        return True


    @app_commands.command(name="urun_kaldir", description="Bir ürünü sil (Admin)")
    @app_commands.describe(urun_ismi="Silmek istediğiniz ürünün ismi")
    async def urun_kaldir(self, interaction: discord.Interaction, urun_ismi: str):
        if interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("❌ Bu komutu kullanmak için yetkin yok.", ephemeral=True)
            return

        urun_ismi = urun_ismi.lower()

        if urun_ismi not in db.products:
            await interaction.response.send_message("❌ Bu isimde bir ürün bulunamadı.", ephemeral=True)
            return

        del db.products[urun_ismi]
        db.save_data()

        await interaction.response.send_message(f"🗑️ `{urun_ismi}` ürünü başarıyla silindi.")

async def setup(bot):
    await bot.add_cog(UrunKaldir(bot))
    
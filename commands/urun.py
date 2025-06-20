import discord
from discord import app_commands
from discord.ext import commands
from utils import db
from config import ADMIN_IDS

class Urun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if db.bakim_modu and interaction.user.id not in db.ADMIN_IDS:
            await interaction.response.send_message("<a:bakimda:1384602567169937580> Bot şu anda bakımda. Daha sonra tekrar dene.", ephemeral=True)
            return False
        return True


    @app_commands.command(name="urun_ekle", description="Yeni ürün ekle (Admin)")
    @app_commands.describe(isim="Ürün ismi", servis_id="Servis ID", fiyat="1K başına fiyat")
    async def urun_ekle(self, interaction: discord.Interaction, isim: str, servis_id: int, fiyat: float):
        if interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("❌ Yetkin yok.")
            return

        isim = isim.lower()
        if isim in db.products:
            await interaction.response.send_message("❌ Bu ürün zaten var.")
            return

        db.products[isim] = {
            "service_id": servis_id,
            "fiyat": fiyat
        }
        db.save_data()
        await interaction.response.send_message(
            f"✅ Ürün eklendi: {isim} (Servis ID: {servis_id}, Fiyat: {fiyat} kredi/1K)"
        )

async def setup(bot):
    await bot.add_cog(Urun(bot))

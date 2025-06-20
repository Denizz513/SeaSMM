import discord
from discord import app_commands
from discord.ext import commands
from utils import db

class Urunler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if db.bakim_modu and interaction.user.id not in db.ADMIN_IDS:
            await interaction.response.send_message("<a:bakimda:1384602567169937580> Bot şu anda bakımda. Daha sonra tekrar dene.", ephemeral=True)
            return False
        return True

    @app_commands.command(name="urunler", description="Tüm mevcut ürünleri listeler.")
    async def urunler(self, interaction: discord.Interaction):
        if not db.products:
            await interaction.response.send_message("📭 Hiç ürün bulunamadı.", ephemeral=True)
            return

        embed = discord.Embed(title="<:kutu:1384607327013048394> Mevcut Ürünler", color=0x3498db)
        for isim, detay in db.products.items():
            embed.add_field(
                name=isim,
                value=f"<:siparis:1384635022044299406> Servis ID: {detay['service_id']}\n<:para:1384606293968294029> Fiyat: {detay['fiyat']} kredi / 1000 adet",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Urunler(bot))

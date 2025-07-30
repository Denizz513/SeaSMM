import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import os
import json

class UrunTanit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("API_KEY")  # Render environment variable
        self.data_file = "data/bot_data.json"  # JSON ürün fiyat dosyası
        # Adminlerin discord ID'si, sadece bunlar kullanabilir
        self.admin_ids = {1374472023199318077}  # Kendine göre düzenle

    async def fetch_lunasmm_product(self, service_id):
        url = f"https://lunasmm.net/api/v2/service/{service_id}?api_key={self.api_key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                if data.get("status") != "success":
                    return None
                return data.get("data")

    def get_local_price(self, product_id):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data["products"].get(product_id, {}).get("fiyat")
        except Exception:
            return None

    @app_commands.command(name="uruntanit", description="Ürün ID ile LunaSMM ürünü tanıt")
    @app_commands.describe(urunid="Örnek: i1570 veya t764 gibi ID")
    async def uruntanit(self, interaction: discord.Interaction, urunid: str):
        if interaction.user.id not in self.admin_ids:
            await interaction.response.send_message("❌ Bu komutu kullanmak için yetkin yok.", ephemeral=True)
            return
        
        await interaction.response.defer()  # Komutu işliyor olarak göster
        
        # LunaSMM id'den sadece rakamları alalım (ör: i1570 -> 1570)
        service_id = ''.join(filter(str.isdigit, urunid))
        if not service_id:
            await interaction.followup.send("❌ Geçerli bir ürün ID'si gir.")
            return

        luna_data = await self.fetch_lunasmm_product(service_id)
        if luna_data is None:
            await interaction.followup.send("❌ Ürün bilgileri LunaSMM'den çekilemedi.")
            return

        local_price = self.get_local_price(urunid)
        if local_price is None:
            await interaction.followup.send("❌ Ürün fiyatı yerel veritabanında bulunamadı.")
            return

        embed = discord.Embed(
            title=luna_data.get("name", "Ürün Adı Bulunamadı"),
            description=luna_data.get("description", "Açıklama yok."),
            color=discord.Color.blurple()
        )
        embed.add_field(name="Min Sipariş", value=luna_data.get("min", "Bilinmiyor"), inline=True)
        embed.add_field(name="Max Sipariş", value=luna_data.get("max", "Bilinmiyor"), inline=True)
        embed.add_field(name="Fiyat (bizim data)", value=f"{local_price:.4f} TL", inline=True)
        embed.add_field(name="Kategori", value=luna_data.get("category", "Bilinmiyor"), inline=True)
        embed.add_field(name="Süre", value=luna_data.get("average_time", "Bilinmiyor"), inline=True)
        embed.set_footer(text="LunaSMM API üzerinden bilgi alındı.")
        
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(UrunTanit(bot))
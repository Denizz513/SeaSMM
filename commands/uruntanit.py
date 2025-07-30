import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import os
import json

class UrunTanit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("API_KEY")
        self.api_url = os.getenv("API_URL") or "https://lunasmm.net/api/v2"

        # JSON dosya yolu
        self.data_path = "data/bot_data.json"
        # JSON verisini yükle
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    async def fetch_product_info(self, service_id):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        url = f"{self.api_url}/services/{service_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return None

    @app_commands.command(name="uruntanit", description="Ürün ID ile LunaSMM'den ürün bilgisi gösterir.")
    @app_commands.describe(id="Ürün ID'si (örn: i1570)")
    async def uruntanit(self, interaction: discord.Interaction, id: str):
        await interaction.response.defer()

        # JSON dosyandaki fiyatları kontrol et
        fiyat = None
        if id in self.data["products"]:
            fiyat = self.data["products"][id].get("fiyat")

        if not id.startswith(("i","t")):
            await interaction.followup.send("Ürün ID'si 'i' veya 't' ile başlamalıdır. Örn: i1570")
            return

        # LunaSMM servis ID al (harfi çıkar)
        try:
            service_id = int(id[1:])
        except:
            await interaction.followup.send("Geçersiz ürün ID formatı.")
            return

        # LunaSMM API'den veri çek
        product_info = await self.fetch_product_info(service_id)
        if not product_info:
            await interaction.followup.send("Ürün bilgisi alınamadı. ID doğru mu kontrol et.")
            return

        # Embed hazırla
        embed = discord.Embed(
            title=product_info.get("name", "Ürün"),
            description=product_info.get("description", "Açıklama yok"),
            color=discord.Color.green()
        )

        # Fiyat JSON dosyadan al, yoksa LunaSMM API fiyatını göster
        api_price = product_info.get("min_amount", "Bilinmiyor")
        embed.add_field(name="Fiyat", value=f"{fiyat if fiyat is not None else api_price} TL", inline=True)

        # Min/Max adet gibi bilgileri LunaSMM API'den ekle
        min_amount = product_info.get("min_amount", "Bilinmiyor")
        max_amount = product_info.get("max_amount", "Bilinmiyor")
        embed.add_field(name="Minimum Sipariş", value=str(min_amount), inline=True)
        embed.add_field(name="Maksimum Sipariş", value=str(max_amount), inline=True)

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UrunTanit(bot))
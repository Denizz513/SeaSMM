import discord
from discord.ext import commands
from discord import app_commands
import json
import aiohttp
import os

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")  # örnek: "https://lunasmm.net/api/v2"
ADMIN_ID = 1374472023199318077  # sadece bu ID komutu kullanabilir

class UrunTanitim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="uruntanit", description="Ürün ID'si ile ürün bilgilerini gösterir.")
    @app_commands.describe(urun_id="Ürünün ID'si (örn: i1570)")
    async def uruntanit(self, interaction: discord.Interaction, urun_id: str):
        if interaction.user.id != ADMIN_ID:
            await interaction.response.send_message("❌ Bu komutu sadece yetkililer kullanabilir.", ephemeral=True)
            return

        # JSON dosyasını oku
        try:
            with open("data/bot_data.json", "r") as f:
                data = json.load(f)
        except Exception:
            await interaction.response.send_message("❌ Ürün veritabanı okunamadı.", ephemeral=True)
            return

        urun = data["products"].get(urun_id)
        if not urun:
            await interaction.response.send_message("❌ Ürün ID bulunamadı.", ephemeral=True)
            return

        service_id = urun["service_id"]
        fiyat = urun["fiyat"]
        aciklama = urun.get("aciklama", "Açıklama girilmemiş.")

        # LunaSMM API'den servis bilgilerini çek
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(API_URL, data={
                    "key": API_KEY,
                    "action": "services"
                }) as response:
                    if response.status != 200:
                        await interaction.response.send_message("❌ LunaSMM API bağlantı hatası.", ephemeral=True)
                        return
                    services = await response.json()
            except Exception:
                await interaction.response.send_message("❌ LunaSMM API verisi alınamadı.", ephemeral=True)
                return

        service_info = next((s for s in services if str(s["service"]) == str(service_id)), None)
        if not service_info:
            await interaction.response.send_message("❌ Ürün bilgileri LunaSMM'den çekilemedi.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"🛒 Ürün Tanıtımı — {urun_id}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="🧾 Ürün Adı", value=service_info["name"], inline=False)
        embed.add_field(name="📝 Açıklama", value=aciklama, inline=False)
        embed.add_field(name="📁 Kategori", value=service_info.get("category", "Kategori bulunamadı"), inline=False)
        embed.add_field(name="🔢 Min - Max", value=f"{service_info['min']} - {service_info['max']}", inline=True)
        embed.add_field(name="💸 Fiyat", value=f"{fiyat:.2f}₺ / 1K", inline=True)
        embed.add_field(
            name="📦 Sipariş Nasıl Verilir?",
            value="> `/siparis <ürün_id> <adet> <link>` şeklinde sipariş oluşturabilirsiniz.",
            inline=False
        )
        embed.set_footer(text="SEA SMM")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(UrunTanitim(bot))
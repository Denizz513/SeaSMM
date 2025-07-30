import discord
from discord import app_commands
from discord.ext import commands
import json
import aiohttp
import os

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")  # örn: https://lunasmm.net/api/v2
ADMIN_ID = 1374472023199318077  # senin ID

class UrunTanit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="uruntanit", description="Ürün ID'sine göre tanıtım yapar.")
    @app_commands.describe(urun_id="Ürün ID'sini giriniz (örn: i1570)")
    async def uruntanit(self, interaction: discord.Interaction, urun_id: str):
        if interaction.user.id != ADMIN_ID:
            await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)
            return

        # Doğru yoldan data/bot_data.json dosyasını oku
        try:
            data_path = os.path.join(os.path.dirname(__file__), "..", "data", "bot_data.json")
            data_path = os.path.abspath(data_path)
            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            await interaction.response.send_message("❌ Data dosyası bulunamadı.", ephemeral=True)
            return

        urun = data.get("products", {}).get(urun_id)
        if not urun:
            await interaction.response.send_message("❌ Ürün ID'si bulunamadı.", ephemeral=True)
            return

        service_id = urun.get("service_id")
        fiyat = urun.get("fiyat")
        urun_adi_local = urun.get("ad", "Ad yok")  # JSON içindeki ürün adı

        # LunaSMM API'den açıklama çek
        headers = {"Authorization": API_KEY}
        payload = {"action": "services"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(API_URL, data=payload, headers=headers) as resp:
                    services = await resp.json()
        except Exception:
            await interaction.response.send_message("❌ LunaSMM API hatası.", ephemeral=True)
            return

        service_data = None
        for s in services:
            if str(s.get("service")) == str(service_id):
                service_data = s
                break

        if not service_data:
            await interaction.response.send_message("❌ LunaSMM'den ürün bilgisi alınamadı.", ephemeral=True)
            return

        aciklama = service_data.get("description", "Açıklama yok")
        min_ = service_data.get("min", "Bilinmiyor")
        max_ = service_data.get("max", "Bilinmiyor")

        embed = discord.Embed(
            title=urun_adi_local,
            description=aciklama,
            color=discord.Color.blue()
        )
        embed.add_field(name="Fiyat", value=f"{fiyat}₺", inline=True)
        embed.add_field(name="Min", value=min_, inline=True)
        embed.add_field(name="Max", value=max_, inline=True)
        embed.add_field(name="Ürün ID", value=urun_id, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(UrunTanit(bot))
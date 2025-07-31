import discord
from discord import app_commands
from discord.ext import commands
from utils import db
from config import ADMIN_IDS
import asyncio
import aiohttp
import os

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL") or "https://lunasmm.net/api/v2"

class Urun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if db.bakim_modu and interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message(
                "<a:bakimda:1384602567169937580> Bot şu anda bakımda. Daha sonra tekrar dene.",
                ephemeral=True
            )
            return False
        return True

    async def get_service_info(self, service_id):
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, data={
                "key": API_KEY,
                "action": "services"
            }) as resp:
                services = await resp.json()
                for s in services:
                    if str(s["service"]) == str(service_id):
                        return s
                return None

    @app_commands.command(name="urun_ekle", description="Yeni ürün ekle (Admin)")
    @app_commands.describe(
        isim="Ürün ismi", 
        servis_id="Servis ID", 
        fiyat="1K başına fiyat"
    )
    async def urun_ekle(
        self, 
        interaction: discord.Interaction, 
        isim: str, 
        servis_id: int, 
        fiyat: float
    ):
        if interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)
            return

        isim = isim.lower()
        if isim in db.products:
            await interaction.response.send_message("❌ Bu ürün zaten var.", ephemeral=True)
            return

        service_info = await self.get_service_info(servis_id)
        if not service_info:
            await interaction.response.send_message("❌ Servis bulunamadı.", ephemeral=True)
            return

        kategori = service_info.get("category", "Bilinmiyor")

        await interaction.response.send_message(
            f"📝 Lütfen ürün açıklamasını bu kanala yazınız. 2 dakika içinde yazmazsanız işlem iptal olur.",
            ephemeral=True
        )

        def check(m):
            return (
                m.author.id == interaction.user.id
                and m.channel.id == interaction.channel.id
            )

        try:
            mesaj = await self.bot.wait_for("message", timeout=120, check=check)
            aciklama = mesaj.content
        except asyncio.TimeoutError:
            await interaction.followup.send("⌛ Açıklama girilmedi, işlem iptal edildi.", ephemeral=True)
            return

        # Verilen fiyatı doğrudan kaydet
        db.products[isim] = {
            "service_id": servis_id,
            "fiyat": fiyat,
            "kategori": kategori,
            "aciklama": aciklama
        }
        db.save_data()

        await interaction.followup.send(
            f"✅ Ürün eklendi: `{isim}`\n"
            f"Kategori: **{kategori}**\n"
            f"Fiyat: **{fiyat}₺ / 1K**\n"
            f"Açıklama: {aciklama}"
        )

    @app_commands.command(name="urun_guncelle", description="Mevcut bir ürünü güncelle (Admin)")
    @app_commands.describe(
        isim="Güncellenecek ürünün ismi", 
        servis_id="Yeni servis ID (isteğe bağlı)", 
        fiyat="Yeni fiyat (isteğe bağlı)", 
        kategori="Yeni kategori (isteğe bağlı)", 
        aciklama="Yeni açıklama (isteğe bağlı)"
    )
    async def urun_guncelle(
        self, 
        interaction: discord.Interaction, 
        isim: str, 
        servis_id: int = None, 
        fiyat: float = None, 
        kategori: str = None, 
        aciklama: str = None
    ):
        if interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)
            return

        isim = isim.lower()
        if isim not in db.products:
            await interaction.response.send_message("❌ Böyle bir ürün yok.", ephemeral=True)
            return

        if servis_id is not None:
            db.products[isim]["service_id"] = servis_id
        if fiyat is not None:
            db.products[isim]["fiyat"] = fiyat
        if kategori is not None:
            db.products[isim]["kategori"] = kategori
        if aciklama is not None:
            db.products[isim]["aciklama"] = aciklama

        db.save_data()

        await interaction.response.send_message(
            f"✅ Ürün güncellendi: `{isim}`\n"
            f"Servis ID: `{db.products[isim].get('service_id')}`\n"
            f"Fiyat: **{db.products[isim].get('fiyat')}₺ / 1K**\n"
            f"Kategori: **{db.products[isim].get('kategori')}**\n"
            f"Açıklama: {db.products[isim].get('aciklama')}"
        )

async def setup(bot):
    await bot.add_cog(Urun(bot))
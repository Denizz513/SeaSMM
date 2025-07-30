import discord
from discord import app_commands
from discord.ext import commands
from utils.db import db
from config import ADMIN_IDS

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

    @app_commands.command(name="urun_ekle", description="Yeni ürün ekle (Admin)")
    @app_commands.describe(
        isim="Ürün ismi",
        servis_id="Servis ID",
        fiyat="1K başına fiyat",
        aciklama="Ürün açıklaması"
    )
    async def urun_ekle(
        self,
        interaction: discord.Interaction,
        isim: str,
        servis_id: int,
        fiyat: float,
        aciklama: str
    ):
        if interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)
            return

        isim = isim.lower()
        if isim in db.products:
            await interaction.response.send_message("❌ Bu ürün zaten var.", ephemeral=True)
            return

        db.products[isim] = {
            "service_id": servis_id,
            "fiyat": fiyat,
            "aciklama": aciklama
        }
        db.save_data()

        await interaction.response.send_message(
            f"✅ Ürün eklendi:\n"
            f"• İsim: `{isim}`\n"
            f"• Servis ID: `{servis_id}`\n"
            f"• Fiyat: `{fiyat}₺`\n"
            f"• Açıklama: {aciklama}"
        )

    @app_commands.command(name="urun_guncelle", description="Bir ürünün açıklamasını veya fiyatını güncelle")
    @app_commands.describe(
        isim="Ürün ismi",
        fiyat="Yeni fiyat (opsiyonel)",
        aciklama="Yeni açıklama (opsiyonel)"
    )
    async def urun_guncelle(
        self,
        interaction: discord.Interaction,
        isim: str,
        fiyat: float = None,
        aciklama: str = None
    ):
        if interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)
            return

        isim = isim.lower()
        if isim not in db.products:
            await interaction.response.send_message("❌ Bu ürün bulunamadı.", ephemeral=True)
            return

        if fiyat is not None:
            db.products[isim]["fiyat"] = fiyat
        if aciklama is not None:
            db.products[isim]["aciklama"] = aciklama

        db.save_data()

        await interaction.response.send_message(
            f"✅ Ürün güncellendi:\n"
            f"• İsim: `{isim}`\n"
            f"• Yeni Fiyat: `{db.products[isim]['fiyat']}₺`\n"
            f"• Yeni Açıklama: {db.products[isim]['aciklama']}"
        )

async def setup(bot):
    await bot.add_cog(Urun(bot))
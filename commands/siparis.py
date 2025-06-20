import discord
from discord import app_commands
from discord.ext import commands
import requests
from config import API_URL, API_KEY, LOG_CHANNEL_ID
from utils import db

class Siparis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if db.bakim_modu and interaction.user.id not in db.ADMIN_IDS:
            await interaction.response.send_message(
                "<a:bakimda:1384602567169937580> Bot şu anda bakımda. Daha sonra tekrar dene.",
                ephemeral=True
            )
            return False
        return True

    @app_commands.command(name="siparis", description="Sipariş oluştur.")
    @app_commands.describe(urun_ismi="Ürün ismi", link="Link Mutlaka http/https li link giriniz", miktar="Kaç adet?")
    async def siparis(self, interaction: discord.Interaction, urun_ismi: str, link: str, miktar: int):
        urun_ismi = urun_ismi.lower()
        if urun_ismi not in db.products:
            await interaction.response.send_message("❌ Böyle bir ürün yok.")
            return

        ürün = db.products[urun_ismi]
        fiyat_1k = ürün["fiyat"]
        toplam_fiyat = (fiyat_1k * miktar) / 1000

        if db.user_credits.get(interaction.user.id, 0) < toplam_fiyat:
            await interaction.response.send_message(
                f"❌ Yeterli kredin yok. Gerekli: *{toplam_fiyat}*, sende var: *{db.user_credits.get(interaction.user.id, 0)}*"
            )
            return

        payload = {
            "key": API_KEY,
            "action": "add",
            "service": ürün["service_id"],
            "link": link,
            "quantity": miktar
        }

        response = requests.post(API_URL, data=payload).json()

        if "order" in response:
            db.user_credits[interaction.user.id] -= toplam_fiyat

            db.log_order(interaction.user.id, {
                "urun": urun_ismi,
                "kullanici": link,
                "adet": miktar,
                "siparis_id": response["order"],
                "fiyat": round(toplam_fiyat, 2)
            })

            db.save_data()

            log_embed = discord.Embed(title="📥 Yeni Sipariş", color=0x3498db)
            log_embed.add_field(name="👤 Kullanıcı", value=f"{interaction.user} ({interaction.user.id})", inline=False)
            log_embed.add_field(name="📦 Ürün", value=urun_ismi, inline=True)
            log_embed.add_field(name="🔗 Link", value=link, inline=True)
            log_embed.add_field(name="🔢 Miktar", value=str(miktar), inline=True)
            log_embed.add_field(name="💳 Harcanan Kredi", value=str(round(toplam_fiyat, 2)), inline=True)
            log_embed.add_field(name="🆔 Sipariş ID", value=str(response['order']), inline=False)

            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=log_embed)

            embed = discord.Embed(title="Sipariş Onaylandı ✅", color=0x00ff00)
            embed.add_field(name="Ürün", value=urun_ismi, inline=True)
            embed.add_field(name="Link", value=link, inline=True)
            embed.add_field(name="Adet", value=str(miktar), inline=True)
            embed.add_field(name="Sipariş ID", value=str(response["order"]), inline=False)
            embed.add_field(name="Kredi Düşülen", value=str(round(toplam_fiyat, 2)), inline=False)
            embed.add_field(name="Kalan Kredi", value=str(round(db.user_credits[interaction.user.id], 2)), inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"❌ Sipariş hatası: {response}")

async def setup(bot):
    await bot.add_cog(Siparis(bot))

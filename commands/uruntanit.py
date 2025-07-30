import discord
from discord.ext import commands
import json
import aiohttp
import os

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
ADMIN_ID = 1374472023199318077  # senin admin ID

class UrunTanit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="uruntanit", description="Belirtilen ürünün tanıtımını yapar.")
    async def uruntanit(self, ctx, urun_id: str):
        if ctx.author.id != ADMIN_ID:
            await ctx.respond("❌ Bu komutu kullanma yetkin yok.", ephemeral=True)
            return

        try:
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            await ctx.respond("❌ data.json dosyası bulunamadı.")
            return

        urun_bilgi = data.get("products", {}).get(urun_id)
        if not urun_bilgi:
            await ctx.respond("❌ Bu ürün ID'si bulunamadı.")
            return

        service_id = urun_bilgi.get("service_id")
        fiyat = urun_bilgi.get("fiyat")

        async with aiohttp.ClientSession() as session:
            try:
                headers = {"Authorization": API_KEY}
                async with session.post(API_URL, data={"action": "services"}, headers=headers) as response:
                    services = await response.json()
            except Exception as e:
                await ctx.respond("❌ LunaSMM API bağlantısında hata oluştu.")
                return

        service_data = next((s for s in services if str(s.get("service")) == str(service_id)), None)
        if not service_data:
            await ctx.respond("❌ Ürün bilgileri çekilemedi.")
            return

        urun_adi = service_data.get("name", "Ürün Adı Bulunamadı")
        aciklama = service_data.get("description", "Açıklama bulunamadı.")
        min_amount = service_data.get("min", "Belirtilmemiş")
        max_amount = service_data.get("max", "Belirtilmemiş")

        embed = discord.Embed(
            title=f"📌 {urun_adi}",
            description=f"📄 {aciklama}",
            color=discord.Color.blue()
        )
        embed.add_field(name="💸 Fiyat", value=f"{fiyat}₺", inline=True)
        embed.add_field(name="🔽 Minimum", value=str(min_amount), inline=True)
        embed.add_field(name="🔼 Maksimum", value=str(max_amount), inline=True)
        embed.add_field(name="🆔 Ürün ID", value=urun_id, inline=False)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(UrunTanit(bot))
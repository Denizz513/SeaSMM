import discord
from discord.ext import commands
import json
import aiohttp
import os

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
ADMIN_ID = 1374472023199318077  # Senin ID

class UrunTanit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="uruntanit", description="Bir ürünün tanıtımını yapar.")
    async def urun_tanit(self, ctx, urun_id: str):
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
                async with session.post(API_URL, data={"action": "services"}, headers=headers) as resp:
                    services = await resp.json()
            except Exception:
                await ctx.respond("❌ Ürün bilgileri LunaSMM'den çekilemedi.")
                return

        servis_detay = next((s for s in services if str(s.get("service")) == str(service_id)), None)
        if not servis_detay:
            await ctx.respond("❌ Ürün bilgileri çekilemedi.")
            return

        urun_adi = servis_detay.get("name", "Bilinmiyor")
        aciklama = servis_detay.get("description", "Açıklama yok.")
        min_amount = servis_detay.get("min", "Bilinmiyor")
        max_amount = servis_detay.get("max", "Bilinmiyor")

        embed = discord.Embed(
            title=f"📌 Ürün: {urun_adi}",
            description=f"📃 {aciklama}",
            color=discord.Color.green()
        )
        embed.add_field(name="🔢 Minimum", value=str(min_amount), inline=True)
        embed.add_field(name="🔝 Maksimum", value=str(max_amount), inline=True)
        embed.add_field(name="💸 Fiyat", value=f"{fiyat:.2f}₺", inline=True)
        embed.add_field(name="🆔 Servis ID", value=urun_id, inline=False)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(UrunTanit(bot))
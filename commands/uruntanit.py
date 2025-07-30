import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import json
import os

class UrunTanit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("API_KEY")
        self.api_url = os.getenv("API_URL")

    async def get_service_info(self, service_id):
        headers = {"Authorization": self.api_key}
        params = {"type": "services"}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url, headers=headers, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for service in data:
                        if service["service"] == service_id:
                            return service
        return None

    @app_commands.command(name="uruntanit", description="Belirtilen ürünün açıklamasını gösterir.")
    async def uruntanit(self, interaction: discord.Interaction, urun_id: str):
        # Sadece admin izni olanlar kullanabilsin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Bu komutu sadece **yöneticiler** kullanabilir.", ephemeral=True)
            return

        try:
            with open("data/bot_data.json", "r") as f:
                data = json.load(f)

            product_data = data["products"].get(urun_id)
            if not product_data:
                await interaction.response.send_message("❌ Geçersiz ürün ID'si.", ephemeral=True)
                return

            service_id = product_data["service_id"]
            service_info = await self.get_service_info(service_id)

            if not service_info:
                await interaction.response.send_message("❌ Ürün bilgileri çekilemedi.", ephemeral=True)
                return

            embed = discord.Embed(
                title=f"{service_info['name']}",
                description=f"**Açıklama:** {service_info.get('description', 'Yok')}\n"
                            f"**Min:** {service_info.get('min', 'Bilinmiyor')} | "
                            f"**Max:** {service_info.get('max', 'Bilinmiyor')}\n"
                            f"**Fiyat:** {product_data['fiyat']}₺",
                color=discord.Color.purple()
            )

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Bir hata oluştu: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(UrunTanit(bot))
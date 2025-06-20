import discord
from discord import app_commands
from discord.ext import commands
from utils import db

class Siparislerim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if db.bakim_modu and interaction.user.id not in db.ADMIN_IDS:
            await interaction.response.send_message("<a:bakimda:1384602567169937580> Bot şu anda bakımda. Daha sonra tekrar dene.", ephemeral=True)
            return False
        return True


    @app_commands.command(name="siparislerim", description="Geçmiş siparişlerini gösterir.")
    async def siparislerim(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        orders = db.get_orders(user_id)

        if not orders:
            await interaction.response.send_message("🕓 Hiç sipariş geçmişin yok.", ephemeral=True)
            return

        # Sayfa başına 3 sipariş
        pages = [orders[i:i+3] for i in range(0, len(orders), 3)]
        current_page = 0

        def create_embed(page_index):
            embed = discord.Embed(title="📦 Sipariş Geçmişin", color=discord.Color.blue())
            for order in pages[page_index]:
                embed.add_field(
                    name=f"🧾 {order['urun']} | {order['kullanici']}",
                    value=(
                        f"• Adet: **{order['adet']}**\n"
                        f"• Sipariş ID: `{order['siparis_id']}`\n"
                        f"• Kredi: **{order['fiyat']}**"
                    ),
                    inline=False
                )
            embed.set_footer(text=f"Sayfa {page_index + 1} / {len(pages)}")
            return embed

        # Başlangıç embed
        embed = create_embed(current_page)
        view = SiparisView(pages, create_embed)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class SiparisView(discord.ui.View):
    def __init__(self, pages, embed_fn):
        super().__init__(timeout=60)
        self.pages = pages
        self.embed_fn = embed_fn
        self.index = 0

    @discord.ui.button(label="⬅️ Geri", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index > 0:
            self.index -= 1
            await interaction.response.edit_message(embed=self.embed_fn(self.index), view=self)

    @discord.ui.button(label="İleri ➡️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index < len(self.pages) - 1:
            self.index += 1
            await interaction.response.edit_message(embed=self.embed_fn(self.index), view=self)

async def setup(bot):
    await bot.add_cog(Siparislerim(bot))

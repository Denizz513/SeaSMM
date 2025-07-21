import discord
from discord import app_commands
from discord.ext import commands
from utils import db
from config import ADMIN_IDS

class Kredi(commands.Cog):
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

    @app_commands.command(name="onayla", description="Kredi yüklemesini onayla (Sadece Admin).")
    @app_commands.describe(user="Kimin hesabına yüklenecek?", miktar="Yüklenecek kredi miktarı")
    async def onayla(self, interaction: discord.Interaction, user: discord.User, miktar: int):
        if interaction.user.id not in ADMIN_IDS:
            await interaction.response.send_message("<a:iptal:1384601834806706238> Bu komutu sadece adminler kullanabilir.", ephemeral=True)
            return

        if user.id not in db.pending_requests or db.pending_requests[user.id] != miktar:
            await interaction.response.send_message("❌ Bu kullanıcı için geçerli bir bekleyen talep bulunamadı.", ephemeral=True)
            return

        db.user_credits[user.id] = db.user_credits.get(user.id, 0) + miktar
        del db.pending_requests[user.id]
        db.save_data()

        # Ödeme onay logunu gönder
        await db.log_odeme_onayi(self.bot, user, miktar)

        try:
            await user.send(f"<:para:1384606293968294029> {miktar} kredi hesabına yüklendi!")
        except:
            pass

        await interaction.response.send_message(f"✅ {user.name} adlı kullanıcıya {miktar} kredi yüklendi.")

async def setup(bot):
    await bot.add_cog(Kredi(bot))
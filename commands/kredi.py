import discord
from discord import app_commands
from discord.ext import commands
from utils import db
from config import ADMIN_IDS, BASVURU_KANAL_ID, ONAY_KANAL_ID

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

    @app_commands.command(name="bakiye", description="Kredini gösterir.")  
    async def bakiye(self, interaction: discord.Interaction):  
        kredi = db.user_credits.get(interaction.user.id, 0)  
        await interaction.response.send_message(f"<:cuzdan:1384605029398220951> Kredin: *{kredi}*")  

    @app_commands.command(name="bakiye_yukle", description="Kredi yükleme talebi oluştur.")  
    @app_commands.describe(miktar="Kaç kredi yüklemek istiyorsun?", dekont="Dekont görselini yükle")  
    async def bakiye_yukle(self, interaction: discord.Interaction, miktar: int, dekont: discord.Attachment):  
        if interaction.user.id in db.pending_requests:  
            await interaction.response.send_message(
                "<a:iptal:1384601834806706238> Zaten bekleyen bir talebin var. Lütfen önceki onaylansın.", 
                ephemeral=True
            )  
            return  

        if dekont.content_type not in ["image/png", "image/jpeg", "image/jpg"]:  
            await interaction.response.send_message(
                "<a:iptal:1384601834806706238> Sadece görsel formatındaki dekontlar kabul edilir (PNG/JPG).", 
                ephemeral=True
            )  
            return  

        db.pending_requests[interaction.user.id] = miktar  
        db.save_data()  

        await interaction.response.send_message(
            f"<a:onayla:1384602443463004343> {miktar} kredi için başvurun alındı. Dekont kontrol edilecek."
        )  

        kanal = self.bot.get_channel(BASVURU_KANAL_ID)  
        if kanal and isinstance(kanal, discord.TextChannel):  
            embed = discord.Embed(
                title="📩 Kredi Yükleme Talebi",
                description=f"Kullanıcı: {interaction.user.mention} ({interaction.user.id})\n"
                            f"Miktar: **{miktar} kredi**\n"
                            f"Komut: `/onayla user:{interaction.user.id} miktar:{miktar}`",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else discord.Embed.Empty)
            await kanal.send(embed=embed)
            await kanal.send(file=await dekont.to_file())
        else:  
            await interaction.followup.send("⚠️ Başvuru kanalı bulunamadı.", ephemeral=True)  

    @app_commands.command(name="onayla", description="Kredi yüklemesini onayla (Sadece Admin).")  
    @app_commands.describe(user="Kimin hesabına yüklenecek?", miktar="Yüklenecek kredi miktarı")  
    async def onayla(self, interaction: discord.Interaction, user: discord.User, miktar: int):  
        if interaction.user.id not in ADMIN_IDS:  
            await interaction.response.send_message(
                "<a:iptal:1384601834806706238> Bu komutu sadece adminler kullanabilir.", 
                ephemeral=True
            )  
            return  

        if user.id not in db.pending_requests or db.pending_requests[user.id] != miktar:  
            await interaction.response.send_message("❌ Bu kullanıcı için geçerli bir bekleyen talep bulunamadı.", ephemeral=True)  
            return  

        db.user_credits[user.id] = db.user_credits.get(user.id, 0) + miktar  
        del db.pending_requests[user.id]  
        db.save_data()  

        try:  
            await user.send(f"<:para:1384606293968294029> {miktar} kredi hesabına yüklendi!")  
        except:  
            pass  

        # ONAY KANALINA EMBED LOG GÖNDER
        onay_kanal = self.bot.get_channel(ONAY_KANAL_ID)
        if onay_kanal and isinstance(onay_kanal, discord.TextChannel):
            embed = discord.Embed(
                title="✅ Ödeme Onayı",
                description=(
                    f"Kullanıcı: {user.mention} ({user.id})\n"
                    f"Yüklenen Kredi: **{miktar} kredi**\n"
                    f"Onaylayan: {interaction.user.mention}"
                ),
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=user.avatar.url if user.avatar else discord.Embed.Empty)
            await onay_kanal.send(embed=embed)

        await interaction.response.send_message(f"✅ {user.name} adlı kullanıcıya {miktar} kredi yüklendi.")

async def setup(bot):
    await bot.add_cog(Kredi(bot))
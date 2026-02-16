import discord
from discord.ext import commands, tasks
from discord import app_commands
from views.call_view import VoicePanelView
from embed.announceServer import announce_server
from embed.announceVoicePanel import announce_voice_panel
from config import CHANNEL_ANNOUNCE, CHANNEL_VOICE_PANEL, CHANNEL_TEST

INTERVAL_HOURS = 6  # tempo entre mensagens


class AutoAnnounce(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.announce.start()
        self._sent_on_ready = False

    def cog_unload(self):
        self.announce.cancel()

    @app_commands.command(
        name="anuncio",
        description="Envia o embed de informações do servidor")
    @app_commands.checks.has_permissions(administrator=True)
    async def anuncio(self, interaction: discord.Interaction):

        await interaction.channel.send(embed=announce_server)
        await interaction.response.send_message("✅ Anúncio enviado.", ephemeral=True)

    @tasks.loop(hours=INTERVAL_HOURS)
    async def announce(self):
        # MUDAR PARA CHAT GERAL DEPOIS
        channel = self.bot.get_channel(CHANNEL_TEST)
        if not channel:
            return

        await channel.send(embed=announce_server)

    @announce.before_loop
    async def before_announce(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        if self._sent_on_ready:
            return

        channel = self.bot.get_channel(CHANNEL_VOICE_PANEL)
        if not channel:
            print("❌ Canal não encontrado")
            return

        async for msg in channel.history(limit=30):
            if msg.author == self.bot.user and msg.embeds:
                embed = msg.embeds[0]
                if embed.title == announce_voice_panel.title:
                    await msg.delete()
        voice_cog = self.bot.get_cog("VoicePanel")
        if not voice_cog:
            print("❌ Cog VoicePanel não carregado.")
            return
        await channel.send(embed=announce_voice_panel, view=VoicePanelView(voice_cog))
        self._sent_on_ready = True


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoAnnounce(bot))

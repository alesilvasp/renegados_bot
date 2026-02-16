import discord
from discord.ext import commands
from embed.announceVoicePanel import announce_voice_panel
from views.call_view import VoicePanelView
from config import CHANNEL_VOICE_PANEL


class VoicePanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dynamic_channels = set()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel and before.channel.id in self.dynamic_channels:
            if len(before.channel.members) == 0:
                await before.channel.delete()
                self.dynamic_channels.discard(before.channel.id)

    @discord.app_commands.command(name="painelcall", description="Envia o painel de criação de salas de voz")
    async def painelcall(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=announce_voice_panel,
            view=VoicePanelView(self)
        )

    async def announce(self):
        channel = self.bot.get_channel(CHANNEL_VOICE_PANEL)
        if channel:
            await channel.send(embed=announce_voice_panel, view=VoicePanelView(self))


async def setup(bot):
    await bot.add_cog(VoicePanel(bot))

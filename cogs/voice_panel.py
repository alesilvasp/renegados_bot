import discord
from discord.ext import commands
from embed.voice_panel_embed import VOICE_PANEL_EMBED
from views.voice_panel_view import VoicePanelView
from config import CHANNEL_VOICE_PANEL


class VoicePanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dynamic_channels = set()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel and before.channel.id in self.dynamic_channels:
            if not before.channel.members:
                await before.channel.delete()
                self.dynamic_channels.discard(before.channel.id)

    @discord.app_commands.command(name="voicepanel")
    async def voice_panel(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=VOICE_PANEL_EMBED,
            view=VoicePanelView(self)
        )


async def setup(bot):
    await bot.add_cog(VoicePanel(bot))

from views import call_view
import discord
from discord.ext import commands

embed = discord.Embed(
    title="Crie a sala de voz do seu dino",
    description=("Clique no botão abaixo para criar sua própria sala!\n"
                 "Escolha a categoria, qual o dino e convide seus amigos!\n\n"),
    color=discord.Color.green()
)


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

        print(interaction.guild.me.guild_permissions)

        await interaction.response.send_message(embed=embed, view=call_view.VoicePanelView())

    async def announce(self):
        channel = self.bot.get_channel(1472182125728895027)
        if not channel:
            return

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(VoicePanel(bot))

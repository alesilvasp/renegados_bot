import discord
from discord.ext import commands, tasks
from discord import app_commands

CHANNEL_ID = 1463563610482806855  # <-- coloque o ID do canal
INTERVAL_HOURS = 6  # tempo entre mensagens

embed = discord.Embed(
    title="📌 Atenção Renegados:",
    description=(
        "👑 **Canais Úteis:**\n"
        "• <#1463563610482806855> — Leia as Regras\n"
        "• Só um teste. Não temos regras ainda...\n"
        "• <#1463563610482806855> — Aqui nesse canal é para falar besteira!\n\n"
        "• <#1471916423751274538> — Aqui pra testar os bots, mas to testando onde eu quiser!\n\n"
        "👉 https://xvideos.com\n\n"
        "NÃO CLIQUE NO LINK ACIMA"
    ),
    color=discord.Color.dark_blue()
)


class AutoAnnounce(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.announce.start()

    def cog_unload(self):
        self.announce.cancel()

    @app_commands.command(
        name="anuncio",
        description="Envia o embed de informações do servidor")
    @app_commands.checks.has_permissions(administrator=True)
    async def anuncio(self, interaction: discord.Interaction):

        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("✅ Anúncio enviado.", ephemeral=True)

    @tasks.loop(hours=INTERVAL_HOURS)
    async def announce(self):
        channel = self.bot.get_channel(CHANNEL_ID)
        if not channel:
            return

        await channel.send(embed=embed)

    @announce.before_loop
    async def before_announce(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoAnnounce(bot))

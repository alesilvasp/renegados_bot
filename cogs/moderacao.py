import discord
from discord import app_commands
from discord.ext import commands


class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="limpar", description="Apaga mensagens do canal")
    @app_commands.describe(quantidade="Quantidade de mensagens (1–100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def limpar(
        self,
        interaction: discord.Interaction,
        quantidade: int
    ):
        if quantidade < 1 or quantidade > 100:
            await interaction.response.send_message(
                "Escolha um valor entre 1 e 100.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)
        apagadas = await interaction.channel.purge(limit=quantidade)
        
        await interaction.followup.send(
            f"{quantidade} mensagens apagadas.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Moderacao(bot))

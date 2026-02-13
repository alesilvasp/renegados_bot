import discord
from discord import app_commands
from discord.ext import commands

from views.shop_view import ShopView


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @app_commands.command(
        name="shop",
        description="Abre a loja de planos de apoiador"
    )
    async def shop(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Loja de planos foi aberta.",
            ephemeral=True
        )

        await interaction.channel.send(
            "**🛒 Loja de Apoiadores**\n"
            "Escolha um plano abaixo:",
            view=ShopView(self.db)
        )


async def setup(bot):
    await bot.add_cog(Shop(bot))

import discord
from discord import app_commands
from discord.ext import commands


class FoodFree(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Food-Free",
        style=discord.ButtonStyle.danger,
        emoji="🍖"
    )
    async def clique(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "De fome você não morre...",
            ephemeral=True
        )

class DietaFull(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label=" Full Dieta ",
        style=discord.ButtonStyle.success,
        emoji="🥗"
    )
    async def clique(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Carboidrato, proteína e lipídios. Agora bora treinar!",
            ephemeral=True
        )


class FoodFreeButton(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="food-free",
        description="Cria um botão de food-free"
    )
    async def botao(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Food Free foi postado",
            ephemeral=True
        )

        await interaction.channel.send(
            view=FoodFree()
        )
class DietaFullButton(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="dieta-full",
        description="Cria um botão de dieta 100%"
    )
    async def botao(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Dieta 100% foi postado",
            ephemeral=True
        )

        await interaction.channel.send(
            view=DietaFull()
        )


async def setup(bot):
    await bot.add_cog(FoodFreeButton(bot))
    await bot.add_cog(DietaFullButton(bot))

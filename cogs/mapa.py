import discord
from discord import app_commands
from discord.ext import commands

MAP_BASE_URL = "https://vulnona.com/game/map/"
MAP_TOKEN = "#map=Gateway_v0.21/"  # coloque o token correto aqui


class Mapa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="mapa",
        description="Abre o mapa dinâmico em uma coordenada específica"
    )
    @app_commands.describe(
        x="Coordenada X",
        y="Coordenada Y"
    )
    async def mapa(
        self,
        interaction: discord.Interaction,
        x: int,
        y: int
    ):
        # Monta a URL com coordenadas
        url = f"{MAP_BASE_URL}#{MAP_TOKEN}{x},{y}"
        print(url)

        embed = discord.Embed(
            title="📍 Localização no mapa",
            description=f"Coordenadas: **X {x} / Y {y}**\n\n"
                        f"[👉 Abrir mapa]({url})",
            color=discord.Color.green()
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Mapa(bot))

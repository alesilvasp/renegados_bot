import asyncio
import discord
from config import CHANNEL_VOICE_PANEL
from services.auto_delete import auto_delete_if_empty

TIMEOUT = 27


class CategoriaDinoView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=30)
        self.cog = cog

    @discord.ui.select(
        placeholder="Escolha a categoria",
        options=[
            discord.SelectOption(label="Carnívoros", emoji="🍖"),
            discord.SelectOption(label="Herbívoros", emoji="🌿"),
            discord.SelectOption(label="Onívoros", emoji="🍽️"),
        ]
    )
    async def select_categoria(self, interaction: discord.Interaction, select: discord.ui.Select):
        categoria = select.values[0]

        await interaction.response.edit_message(
            content=f"🦖 Escolha o {categoria}:",
            view=ListaDinosView(self.cog, categoria)
        )


class ListaDinosView(discord.ui.View):
    DINO_LIMITS = {"Rex": 2, "Omni": 8, "Allo": 3, "Cerato": 5, "Carno": 3, "Deino": 2, "Dillo": 4, "Herrera": 7, "Troodon": 10, "Ptero": 6,
                   "Trike": 4, "Stego": 5, "Diablo": 6, "Tenonto": 8, "Hypsi": 10, "Dryo": 12, "Pachy": 8, "Maia": 10, "Galli": 8, "Beipi": 12, }

    DINO_CATEGORIES = {"Carnívoros": ["Rex", "Omni", "Allo", "Cerato", "Carno", "Deino", "Dillo", "Herrera", "Troodon", "Ptero",], "Herbívoros": [
        "Trike", "Stego", "Diablo", "Tenonto", "Hypsi", "Dryo", "Pachy", "Maia",], "Onívoros": ["Galli", "Beipi"]}

    def __init__(self, cog, categoria):
        super().__init__(timeout=30)
        self.cog = cog
        self.categoria = categoria

        self.add_item(DinoSelect(self.cog, self.categoria))


class DinoSelect(discord.ui.Select):
    def __init__(self, cog, categoria):
        self.cog = cog
        options = [
            discord.SelectOption(label=dino)
            for dino in ListaDinosView.DINO_CATEGORIES[categoria]
        ]

        super().__init__(placeholder="Escolha o dinossauro", options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        dino = self.values[0]

        canal_base = guild.get_channel(CHANNEL_VOICE_PANEL)
        if not canal_base:
            await interaction.response.send_message(
                "❌ Canal base de voz não encontrado. Avise um admin.",
                ephemeral=True
            )
            return
        limite = ListaDinosView.DINO_LIMITS.get(dino, 0)
        nome_final = f"{dino} - {member.display_name}"

        for cid in self.view.cog.dynamic_channels:
            ch = guild.get_channel(cid)
            if ch and ch.name.endswith(member.display_name):
                await interaction.response.send_message(
                    "⚠️ Você já tem uma sala criada.",
                    ephemeral=True
                )
                return

        channel = await guild.create_voice_channel(
            name=nome_final,
            category=canal_base.category,
            user_limit=limite
        )

        self.view.cog.dynamic_channels.add(channel.id)

        await interaction.response.send_message(
            f"✅ Sala criada: {channel.mention}\n⏳ Se ninguém entrar em 20s, ela será apagada.",
            ephemeral=True
        )

        await auto_delete_if_empty(channel, self.view.cog.dynamic_channels, TIMEOUT)

    # async def _timeout_delete(self, channel):
    #     for _ in range(TIMEOUT):
    #         await asyncio.sleep(1)
    #         if len(channel.members) > 0:
    #             return

    #     if len(channel.members) == 0:
    #         await channel.delete()
    #         self.view.cog.dynamic_channels.discard(channel.id)

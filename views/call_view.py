import discord
from discord.ext import commands
import asyncio

DINO_LIMITS = {
    "Rex": 2,
    "Omni": 8,
    "Allo": 3,
    "Cerato": 5,
    "Carno": 3,
    "Deino": 2,
    "Dillo": 4,
    "Herrera": 7,
    "Troodon": 10,
    "Ptero": 6,
    "Trike": 4,
    "Stego": 5,
    "Diablo": 6,
    "Tenonto": 8,
    "Hypsi": 10,
    "Dryo": 12,
    "Pachy": 8,
    "Maia": 10,
    "Galli": 8,
    "Beipi": 12,
}

DINO_CATEGORIES = {
    "Carnívoros": ["Rex",
                   "Omni",
                   "Allo",
                   "Cerato",
                   "Carno",
                   "Deino",
                   "Dillo",
                   "Herrera",
                   "Troodon",
                   "Ptero",],
    "Herbívoros": ["Trike",
                   "Stego",
                   "Diablo",
                   "Tenonto",
                   "Hypsi",
                   "Dryo",
                   "Pachy",
                   "Maia",],
    "Onívoros": ["Galli", "Beipi,"]
}

TIMEOUT = 20


class VoicePanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Criar sala", style=discord.ButtonStyle.green, emoji="🎤")
    async def criar_sala(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Escolha a categoria:",
            view=CategorySelectView(),
            ephemeral=True
        )


class CategorySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Herbívoros", emoji="🌿"),
            discord.SelectOption(label="Carnívoros", emoji="🍖"),
            discord.SelectOption(label="Onívoros", emoji="🥚"),
        ]
        super().__init__(placeholder="Escolha a categoria...", options=options)

    async def callback(self, interaction: discord.Interaction):
        categoria = self.values[0]
        await interaction.response.edit_message(
            content=f"Escolha um dinossauro ({categoria}):",
            view=DinoSelectView(categoria, user=discord.Member)
        )


class CategorySelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(CategorySelect())


class DinoSelect(discord.ui.Select):
    def __init__(self, categoria: str, user: discord.Member):
        dinos = DINO_CATEGORIES[categoria]
        self.user = user
        options = [
            discord.SelectOption(label=dino.capitalize(), value=dino)
            for dino in dinos
        ]
        super().__init__(placeholder="Escolha o dinossauro...", options=options)
        self.categoria = categoria

    async def callback(self, interaction: discord.Interaction):
        dino = self.values[0]
        limit = DINO_LIMITS.get(dino, 99)

        guild = interaction.guild
        user = interaction.user

        category = discord.utils.get(guild.categories, name="Salas de Voz")
        if not category:
            category = await guild.create_category("Salas de Voz")

        channel = await guild.create_voice_channel(
            name=f"🦖 • {dino.capitalize()} ▹ {user.display_name}",
            category=category,
            user_limit=limit
        )

        cog = interaction.client.get_cog("VoicePanel")
        cog.dynamic_channels.add(channel.id)

        def barra_loading(tempo_restante: int, tempo_total: int, tamanho: int = 20):
            proporcao = tempo_restante / tempo_total
            cheios = round(proporcao * tamanho)
            vazios = tamanho - cheios
            return "█" * cheios + "░" * vazios

        await interaction.response.edit_message(
            content=f"✅ Sala criada: {channel.mention}\n⏳ {barra_loading(TIMEOUT, TIMEOUT)} {TIMEOUT}s restantes",
            view=None
        )
        msg = await interaction.original_response()

        async def countdown():
            seconds = TIMEOUT
            while seconds > 0:
                await asyncio.sleep(1)
                seconds -= 1

                # se alguém entrou, para o contador
                if len(channel.members) > 0:
                    await msg.delete()
                    return

                try:
                    await msg.edit(
                        content=f"✅ Sala criada: {channel.mention}\n⏳ {barra_loading(seconds, TIMEOUT)} {seconds}s restantes",
                    )
                except:
                    return

            # Se ninguém entrou até o final
            try:
                await msg.delete()
            except:
                pass

        interaction.client.loop.create_task(countdown())

        async def delete_if_empty():
            await asyncio.sleep(27)
            if len(channel.members) == 0:
                await channel.delete()
                cog.dynamic_channels.discard(channel.id)

        interaction.client.loop.create_task(delete_if_empty())


class DinoSelectView(discord.ui.View):
    def __init__(self, categoria: str, user: discord.Member):
        super().__init__(timeout=60)
        self.add_item(DinoSelect(categoria, user))

import discord
from services.voice_rooms import create_free_room
from views.dinos_view import CategoriaDinoView


def barra_loading(tempo_restante: int, tempo_total: int, tamanho: int = 10):
    proporcao = tempo_restante / tempo_total
    cheios = round(proporcao * tamanho)
    vazios = tamanho - cheios
    return "█" * cheios + "░" * vazios


class VoicePanelView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(
        label="🦖 Criar sala de Dino",
        style=discord.ButtonStyle.green,
        row=0)
    async def criar_dino(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button):
        await interaction.response.send_message(
            "🦖 Escolha a categoria do dinossauro:",
            view=CategoriaDinoView(self.cog),
            ephemeral=True
        )

    @discord.ui.button(
        label="🎮 Sala Livre",
        style=discord.ButtonStyle.blurple,
        custom_id="create_free_room"
    )
    async def create_free_room_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(FreeRoomModal(self.cog))


class FreeRoomModal(discord.ui.Modal, title="Criar Sala Livre"):
    room_name = discord.ui.TextInput(
        label="Nome da sala",
        placeholder="Ex: Rust, REPO...",
        max_length=30
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        await create_free_room(
            interaction=interaction,
            room_name=self.room_name.value,
            cog=self.cog,
            dynamic_channels=self.cog.dynamic_channels
        )

import discord
from discord.ui import Modal, TextInput
from services.voice_rooms import create_free_voice_room


class FreeRoomModal(Modal, title="Create Free Room"):
    name_room = TextInput(label="Room Name", placeholder="Ex: Rankeds")

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        await create_free_voice_room(
            interaction,
            self.name_room.value,
            self.cog
        )
        await interaction.response.send_message(
            f"Room created: {self.name_room.value}",
            ephemeral=True
        )

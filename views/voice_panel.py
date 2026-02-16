import discord
from views.free_room_modal import FreeRoomModal
from views.dino_voice_views import DinoCategoryView

class VoicePanelView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="🦖 Dino Room", style=discord.ButtonStyle.green)
    async def dino_button(self, interaction, button):
        await interaction.response.send_message(
            "Choose Dino Category",
            view=DinoCategoryView(self.cog),
            ephemeral=True
        )

    @discord.ui.button(label="🎮 Free Room", style=discord.ButtonStyle.primary)
    async def free_room_button(self, interaction, button):
        await interaction.response.send_modal(FreeRoomModal(self.cog))

import discord
from config import CHANNEL_VOICE_PANEL
from services.auto_delete import auto_delete_if_empty


async def create_free_room(interaction: discord.Interaction, room_name: str, cog, dynamic_channels: set):
    guild = interaction.guild
    member = interaction.user

    category = guild.get_channel(CHANNEL_VOICE_PANEL)
    if not category:
        return await interaction.response.send_message(
            "❌ Categoria de salas temporárias não encontrada.",
            ephemeral=True
        )

    channel_name = f"{room_name} | {member.display_name}"

    voice = await guild.create_voice_channel(
        name=channel_name,
        category=category.category,
        user_limit=0
    )

    cog.dynamic_channels.add(voice.id)

    try:
        await voice.set_permissions(
            member,
            connect=True,
            speak=True,
            move_members=True
        )
    except discord.Forbidden:
        # Loga, mas não quebra a criação da sala
        print("⚠️ Bot sem permissão para setar permissões no canal de voz.")

    await interaction.response.send_message(
        f"✅ Sala criada: {voice.mention}",
        ephemeral=True
    )
    await auto_delete_if_empty(voice, dynamic_channels, timeout=27)

    return voice

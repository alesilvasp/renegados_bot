import asyncio
import discord
from config import CHANNEL_VOICE_PANEL


async def auto_delete_empty(channel, dynamic_channels: set, timeout: int):
    for _ in range(timeout):
        await asyncio.sleep(1)
        if channel.members:
            return
    if not channel.members:
        await channel.delete()
        dynamic_channels.discard(channel.id)


async def create_free_voice_room(
    interaction: discord.Interaction,
    room_name: str,
    cog
):
    guild = interaction.guild
    member = interaction.user

    base_channel = guild.get_channel(CHANNEL_VOICE_PANEL)
    category = base_channel.category

    channel = await guild.create_voice_channel(
        name=f"{room_name} | {member.display_name}",
        category=category,
        user_limit=0
    )

    cog.dynamic_channels.add(channel.id)
    return channel

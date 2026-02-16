import asyncio


def barra_loading(tempo_restante: int, tempo_total: int, tamanho: int = 10):
    proporcao = tempo_restante / tempo_total
    cheios = round(proporcao * tamanho)
    vazios = tamanho - cheios
    return "█" * cheios + "░" * vazios


async def auto_delete_if_empty(channel, dynamic_channels: set, timeout: int = 20):
    for _ in range(timeout):
        await asyncio.sleep(1)
        if len(channel.members) > 0:
            return
        loading_bar = barra_loading(timeout, 20, tamanho=10)

        try:
            await msg.edit
    if len(channel.members) == 0:
        await channel.delete()
        dynamic_channels.discard(channel.id)

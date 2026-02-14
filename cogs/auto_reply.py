from discord.ext import commands
import time


class AutoReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}

        self.targets = {
            266565950067834882: "Não marque o Andrey, chame outro!",
            326820084817592321: "Se eu fosse você não chamaria ela não... Chame outro! 😂",
            1236994843755024464: "Nhocco tá ocupado sempre! Chame outro! 😂",
            275705864818524160: "Op é PJ (Pessoa Judiada)! Se não está trabalhando, está dormindo. Chame outro! 😂",
            "everyone": "Para de marcar geral! Chama no PV, por favor!",
            718126022935052379: "Vc quis dizer Cesta Básica de Alimentos?"
        }

    @commands.Cog.listener()
    async def on_message(self, message):

        print("mensagem:", message.content)
        if "😉" in message.content:
            await message.channel.send("Vai piscar pra suas negas!")
        # Ignora mensagens do próprio bot
        if message.author.bot:
            return

        # ignora se for respostas
        if message.reference is not None:
            return

        if message.mention_everyone:

            if "everyone" in self.targets:
                await message.channel.send(self.targets["everyone"])

            return
        if not message.mentions:
            return

        now = time.time()
        channel_id = message.channel.id

        # last = self.cooldowns.get(channel_id, 0)
        # if now - last < 20:
        #     return
        print(message.type)
        for user in message.mentions:
            if user.id in self.targets:
                # self.cooldowns[channel_id] = now
                await message.channel.send(self.targets[user.id])
                break

        content = message.content.lower()

        # Gatilho
        if "sexo" in content:
            await message.channel.send("Cuidado com suas palavras, Mitarada!")


async def setup(bot):
    await bot.add_cog(AutoReply(bot))

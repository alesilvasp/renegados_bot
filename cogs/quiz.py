import discord
from discord import app_commands
from discord.ext import commands
import random


class QuizView(discord.ui.View):
    def __init__(self, pergunta, callback):
        super().__init__(timeout=30)
        self.pergunta = pergunta
        self.callback_func = callback

        for i, opcao in enumerate(pergunta["opcoes"]):
            self.add_item(
                discord.ui.Button(
                    label=opcao,
                    style=discord.ButtonStyle.primary,
                    custom_id=str(i)
                )
            )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Permite qualquer usuário responder
        return True

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

    async def interaction_check(self, interaction: discord.Integration) -> bool:
        escolha = int(interaction.data["custom_id"])
        await self.callback_func(interaction, escolha)
        return False


class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.perguntas = [
            {
                "pergunta": "Qual dino é canibal por natureza?",
                "opcoes": ["Pteranodon", "Carnotaurus", "Ceratossauro", "Troodon"],
                "resposta": 2
            }
        ]

        self.quiz_ativo = {}   # guild_id -> resposta correta
        self.pontuacao = {}   # user_id -> pontos

    quiz = app_commands.Group(
        name="quiz",
        description="Comandos do quiz"
    )

    @quiz.command(name="iniciar", description="Inicia um quiz com botões")
    async def iniciar(self, interaction: discord.Interaction):

        pergunta = random.choice(self.perguntas)
        self.quiz_ativo[interaction.guild.id] = pergunta["resposta"]

        texto = f"🧠 **QUIZ**\n\n{pergunta['pergunta']}"

        view = QuizView(pergunta, self.processar_resposta)

        await interaction.response.send_message(
            texto,
            view=view
        )

    async def processar_resposta(
        self,
        interaction: discord.Interaction,
        escolha: int
    ):
        guild_id = interaction.guild.id

        if guild_id not in self.quiz_ativo:
            await interaction.response.send_message(
                "Este quiz já foi encerrado.",
                ephemeral=True
            )
            return

        correta = self.quiz_ativo[guild_id]

        if escolha == correta:
            user_id = interaction.user.id
            self.pontuacao[user_id] = self.pontuacao.get(user_id, 0) + 1

            await interaction.response.send_message(
                "Resposta correta! +1 ponto.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "Resposta errada.",
                ephemeral=True
            )

        del self.quiz_ativo[guild_id]

    @quiz.command(name="pontuacao", description="Mostra sua pontuação")
    async def pontuacao_cmd(self, interaction: discord.Interaction):
        pontos = self.pontuacao.get(interaction.user.id, 0)
        await interaction.response.send_message(
            f"Sua pontuação: **{pontos}**",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Quiz(bot))

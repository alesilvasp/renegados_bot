import discord
from discord import app_commands
from discord.ext import commands

from services.permissoes import can_use, register_use
from services.planos import PLANS



class Grow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @app_commands.command(
        name="grow",
        description="Usa seu grow semanal de plano apoiador"
    )
    async def grow(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        # 1️⃣ Verifica se pode usar
        ok, msg = can_use(self.db, interaction.user.id, "grow")
        if not ok:
            return await interaction.response.send_message(
                msg,
                ephemeral=True
            )

        # 2️⃣ EXECUTA A AÇÃO REAL
        # (aqui entraria integração com o jogo, API, log, etc.)
        # Exemplo fictício:
        # await executar_grow(interaction.user)
        # await game_api.give_grow(user_id)

        # 3️⃣ REGISTRA O USO
        
        register_use(self.db, interaction.user.id, "grow")

        # 4️⃣ RESPONDE
        plan = self.db.get_weekly_usage(user_id)
        plan_cfg = PLANS[plan["plan_name"]]

        

        used = self.db.get_weekly_usage(user_id, action="grow")
        limit = plan_cfg["weekly_limits"]["grow"]

        await interaction.response.send_message(
            f"Grow utilizado com sucesso.\n"
            f"Uso semanal: {used}/{limit}",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Grow(bot))

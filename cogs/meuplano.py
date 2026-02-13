import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

from services.planos import PLANS



class MeuPlano(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    @app_commands.command(
        name="meuplano",
        description="Mostra informações do seu plano de apoiador"
    )
    async def meuplano(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        plan = self.db.get_user_plan(user_id)

        # Usuário sem plano
        if not plan:
            return await interaction.response.send_message(
                "Você não possui um plano de apoiador ativo.",
                ephemeral=True
            )

        now = datetime.now(timezone.utc)
        remaining_days = (plan["end_date"] - now).days

        plan_cfg = PLANS.get(plan["plan_name"])
        if not plan_cfg:
            return await interaction.response.send_message(
                "Plano inválido. Contate a administração.",
                ephemeral=True
            )

        # Monta lista de benefícios
        benefits_lines = []
        for action, limit in plan_cfg.get("weekly_limits", {}).items():
            used = self.db.get_weekly_usage(user_id, action)
            benefits_lines.append(
                f"• {action.capitalize()}: {used}/{limit} usado(s)"
            )

        benefits_text = "\n".join(benefits_lines) if benefits_lines else "Nenhum benefício semanal."

        # Resposta final
        await interaction.response.send_message(
            f"**Plano:** {plan_cfg['display']}\n"
            f"**Expira em:** {remaining_days} dia(s)\n\n"
            f"**Benefícios semanais:**\n{benefits_text}",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(MeuPlano(bot))

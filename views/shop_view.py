import discord
from services.planos import PLANS



class ShopView(discord.ui.View):
    def __init__(self,db):
        super().__init__(timeout=None)
        self.db = db

    async def buy_plan(self, interaction: discord.Interaction, plan_key: str):
        plan = PLANS[plan_key]

        # 🔒 AQUI entrará o sistema de saldo futuramente
        # Exemplo:
        # if not has_balance(interaction.user.id, plan["price"]):
        #     return await interaction.response.send_message("Saldo insuficiente.", ephemeral=True)

        # Ativa / substitui plano
        self.db.set_user_plan(
            user_id=interaction.user.id,
            plan_name=plan_key,
            duration_days=plan["duration_days"]
        )

        await interaction.response.send_message(
            f"Plano **{plan['display']}** ativado com sucesso por {plan['duration_days']} dias.",
            ephemeral=True
        )

    @discord.ui.button(label="FERRO", style=discord.ButtonStyle.secondary, custom_id="shop:ferro")
    async def ferro(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.buy_plan(interaction, "ferro")

    @discord.ui.button(label="BRONZE", style=discord.ButtonStyle.primary, custom_id="shop:bronze")
    async def bronze(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.buy_plan(interaction, "bronze")

    @discord.ui.button(label="OURO", style=discord.ButtonStyle.success, custom_id="shop:ouro")
    async def ouro(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.buy_plan(interaction, "ouro")

    @discord.ui.button(label="DIAMANTE", style=discord.ButtonStyle.danger, custom_id="shop:diamante")
    async def diamante(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.buy_plan(interaction, "diamante")

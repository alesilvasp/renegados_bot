from datetime import datetime, timezone
from services.planos import PLANS


def can_use(db, user_id: int, action: str):
    plan = db.get_user_plan(user_id)
    now = datetime.now(timezone.utc)

    if not plan:
        return False, "Você não possui um plano ativo."

    if plan["end_date"].replace(tzinfo=timezone.utc) < now:
        db.remove_user_plan(user_id)
        return False, "Seu plano expirou."

    plan_cfg = PLANS.get(plan["plan_name"])
    if not plan_cfg:
        return False, "Plano inválido. Contate a administração."

    limits = plan_cfg.get("weekly_limits", {})
    if action not in limits:
        return False, "Seu plano não permite essa ação."

    used = db.get_weekly_usage(user_id, action)
    limit = limits[action]

    if used >= limit:
        return False, f"Limite semanal atingido ({used}/{limit})."

    return True, f"Disponível ({used}/{limit})."


def register_use(db, user_id: int, action: str):
    db.increment_weekly_usage(user_id, action)

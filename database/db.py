from datetime import datetime, timedelta, timezone
import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=1,
        max_size=5,
        timeout=60,
        command_timeout=60
    )

    async def _create_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_plans (
                    user_id BIGINT PRIMARY KEY,
                    plan_name TEXT NOT NULL,
                    start_date TIMESTAMPTZ NOT NULL,
                    end_date TIMESTAMPTZ NOT NULL
                );
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS weekly_usage (
                    user_id BIGINT NOT NULL,
                    week_start DATE NOT NULL,
                    action TEXT NOT NULL,
                    used INT NOT NULL,
                    PRIMARY KEY (user_id, week_start, action)
                );
            """)

    @staticmethod
    def get_week_start():
        today = datetime.now(timezone.utc)
        week_start = today - timedelta(days=today.weekday())
        return week_start.date()

    async def set_user_plan(self, user_id: int, plan_name: str, duration_days: int):
        start = datetime.now(timezone.utc)
        end = start + timedelta(days=duration_days)

        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO user_plans (user_id, plan_name, start_date, end_date)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (user_id)
                DO UPDATE SET
                    plan_name = EXCLUDED.plan_name,
                    start_date = EXCLUDED.start_date,
                    end_date = EXCLUDED.end_date;
            """, user_id, plan_name, start, end)

    async def get_user_plan(self, user_id: int):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM user_plans WHERE user_id = $1
            """, user_id)

        if not row:
            return None

        return dict(row)

    async def get_weekly_usage(self, user_id: int, action: str):
        week_start = self.get_week_start()

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT used FROM weekly_usage
                WHERE user_id = $1 AND week_start = $2 AND action = $3
            """, user_id, week_start, action)

        return row["used"] if row else 0

    async def increment_weekly_usage(self, user_id: int, action: str):
        week_start = self.get_week_start()

        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO weekly_usage (user_id, week_start, action, used)
                VALUES ($1, $2, $3, 1)
                ON CONFLICT (user_id, week_start, action)
                DO UPDATE SET used = weekly_usage.used + 1;
            """, user_id, week_start, action)


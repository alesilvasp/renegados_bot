import sqlite3
from datetime import datetime, timedelta, timezone
import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL =", DATABASE_URL)
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não definido")


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL)

    async def _create_tables(self):

        async with self.pool.acquire() as conn:
            await conn.execute("""
        CREATE TABLE IF NOT EXISTS user_plans (
            user_id INTEGER PRIMARY KEY,
            plan_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL
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

        self.conn.commit()

    # =========================
    # UTILIDADES DE DATA
    # =========================
    @staticmethod
    def get_week_start():
        today = datetime.now(timezone.utc)
        week_start = today - timedelta(days=today.weekday())
        return week_start.date().isoformat()

    # =========================
    # PLANOS
    # =========================
    def set_user_plan(self, user_id: int, plan_name: str, duration_days: int):
        start = datetime.now(timezone.utc)
        end = start + timedelta(days=duration_days)

        self.cursor.execute("""
        INSERT OR REPLACE INTO user_plans (user_id, plan_name, start_date, end_date)
        VALUES (?, ?, ?, ?)
        """, (
            user_id,
            plan_name,
            start.isoformat(),
            end.isoformat()
        ))
        self.conn.commit()

    def get_user_plan(self, user_id: int):
        self.cursor.execute("""
        SELECT * FROM user_plans WHERE user_id = ?
        """, (user_id,))
        row = self.cursor.fetchone()

        if not row:
            return None

        return {
            "plan_name": row["plan_name"],
            "start_date": datetime.fromisoformat(row["start_date"]),
            "end_date": datetime.fromisoformat(row["end_date"])
        }

    def remove_user_plan(self, user_id: int):
        self.cursor.execute("""
        DELETE FROM user_plans WHERE user_id = ?
        """, (user_id,))
        self.conn.commit()

    # =========================
    # USO SEMANAL
    # =========================
    def get_weekly_usage(self, user_id: int, action: str):
        week_start = self.get_week_start()

        self.cursor.execute("""
        SELECT used FROM weekly_usage
        WHERE user_id = ? AND week_start = ? AND action = ?
        """, (user_id, week_start, action))

        row = self.cursor.fetchone()
        return row["used"] if row else 0

    def increment_weekly_usage(self, user_id: int, action: str):
        week_start = self.get_week_start()

        current = self.get_weekly_usage(user_id, action)

        self.cursor.execute("""
        INSERT OR REPLACE INTO weekly_usage (user_id, week_start, action, used)
        VALUES (?, ?, ?, ?)
        """, (user_id, week_start, action, current + 1))

        self.conn.commit()

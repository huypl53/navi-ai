"""
    generate data from .csv file
"""

import sys
import os

app_path = os.path.dirname(sys.path[0])
sys.path.append(app_path)

from app.db.connector import engine
from app.model.baseMd import BaseMd
import asyncio

async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseMd.metadata.drop_all)
        await conn.run_sync(BaseMd.metadata.create_all)
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()

asyncio.run(start_db())
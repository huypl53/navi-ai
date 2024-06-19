import pytest
import sys
import os
import asyncio

app_path = os.path.dirname(sys.path[0])
sys.path.append(app_path)

from app.db.connector import engine
from app.model.baseMd import BaseMd

@pytest.fixture(
    scope="session",
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ],
)
def anyio_backend(request):
    return request.param


@pytest.fixture(scope="session")
async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseMd.metadata.drop_all)
        await conn.run_sync(BaseMd.metadata.create_all)
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()

def test_db(start_db):
    asyncio.run(start_db())
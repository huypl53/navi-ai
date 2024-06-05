from fastapi import FastAPI

from middleware import LogMiddleware, setup_cors
from route import router

app = FastAPI()
setup_cors(app)
app.include_router(router)

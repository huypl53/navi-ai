from fastapi import FastAPI

from app.middleware import LogMiddleware, setup_cors
from app.route import model_router

app = FastAPI()
setup_cors(app)
app.include_router(model_router)

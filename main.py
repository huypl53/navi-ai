from fastapi import FastAPI

from app.middleware import LogMiddleware, setup_cors
from app.route import router, model_router, user_router

app = FastAPI()
setup_cors(app)
app.include_router(router)
app.include_router(model_router)

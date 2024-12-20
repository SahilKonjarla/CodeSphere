from fastapi import FastAPI
from app.routes.debug_routes import debug_router

app = FastAPI()

app.include_router(debug_router)

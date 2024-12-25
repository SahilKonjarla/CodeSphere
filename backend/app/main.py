from fastapi import FastAPI
from app.routes.debug_routes import debug_router
from app.routes.optimize_routes import optimize_router
from app.routes.document_routes import document_router

app = FastAPI()

app.include_router(debug_router)
app.include_router(optimize_router)
app.include_router(document_router)

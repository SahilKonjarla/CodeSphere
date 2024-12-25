from fastapi import FastAPI
from app.routes.debug_routes import debug_router
from app.routes.optimize_routes import optimize_router
from app.routes.document_routes import document_router

# Make connection to FastAPI
app = FastAPI()

# Add routers to the main function
app.include_router(debug_router)
app.include_router(optimize_router)
app.include_router(document_router)

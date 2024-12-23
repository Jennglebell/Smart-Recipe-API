from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import recipe_router

app = FastAPI(
    title="Smart Recipe API",
    description="An intelligent API for recipe management and meal planning",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipe_router.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 
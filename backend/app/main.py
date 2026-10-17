from fastapi import FastAPI
from app.api.routes.restaurants import router

app = FastAPI(
    title="Project Double Double API",
    description="Restaurant discovery and menu browsing: list, search and filter restaurants, view details and menus, and manage restaurants and menu items.",
    version="1.0.0",
)

@app.get("/", include_in_schema=False)
def read_root():
    return {"Hello": "World"}

app.include_router(router)

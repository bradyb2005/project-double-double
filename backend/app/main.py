from app.api.routes.login import router as login_router
from app.api.routes.restaurants import router as restaurant_router
from app.api.routes.users import router as user_router
from fastapi import FastAPI

app = FastAPI(
    title="Project Double Double API",
    description="Restaurant discovery and menu browsing: list, search and filter restaurants, view details and menus, and manage restaurants and menu items.",
    version="1.0.0",
)

@app.get("/", include_in_schema=False)
def read_root():
    return {"Hello": "World"}

app.include_router(restaurant_router)
app.include_router(user_router)
app.include_router(login_router)

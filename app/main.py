from fastapi import FastAPI
from app.api.routes.restaurants import router
from app.api.routes.menu import menu_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(router)
app.include_router(menu_router)


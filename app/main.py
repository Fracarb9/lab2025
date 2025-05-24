from fastapi import FastAPI
from app.routers import books, frontend, users
from fastapi.staticfiles import StaticFiles
from app.data.db import init_database
from contextlib import asynccontextmanager

#Decoratore per l'utilizzo di async whit (gestione risorse asincrone come avvio e chiusura app)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # on start
    init_database()
    yield   #Prima dello yield: eseguito all'avio. Dopo: eseguito alla chiusura dell'app
    # on close


app = FastAPI(lifespan=lifespan)
app.include_router(books.router, tags=["books"])
app.include_router(frontend.router)
app.include_router(users.router, tags=["users"])
app.mount("/static", StaticFiles(directory="app/static"), name="static")


if __name__ == "__main__":
    # TODO: if you launch the application from here, you must modify the
    #  relative path to the static folder (in this file) from "app/static" to
    #  "static" and the relative path to the templates folder (in
    #  routers/frontend.py file) from "app/templates" to "templates".
    import uvicorn
    uvicorn.run("main:app", reload=True)

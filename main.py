from fastapi import FastAPI
import models
from database import engine
# from routers import auth, todos, admin, users
from routers import episodes, pitches, sharks, seasons
app = FastAPI()

# only is run if the todos.db does not exist
models.Base.metadata.create_all(bind=engine)

app.include_router(episodes.router)
app.include_router(pitches.router)
app.include_router(sharks.router)
app.include_router(seasons.router)
# app.include_router(auth.router)
# app.include_router(todos.router)
# app.include_router(admin.router)
# app.include_router(users.router)

import uvicorn
from fastapi import FastAPI

from modules.users.module import get_module_router


app = FastAPI()
app.include_router(get_module_router())
uvicorn.run(
    app=app,
    host="0.0.0.0",
    port=8080,
)

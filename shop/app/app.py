from fastapi import FastAPI

from modules.users.module import get_module_router


app = FastAPI()
app.include_router(get_module_router())

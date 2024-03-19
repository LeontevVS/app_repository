import uvicorn
from fastapi import FastAPI

from modules.auth.api import router as auth_router


app = FastAPI()

app.include_router(auth_router)


uvicorn.run(app=app, host='localhost', port=8080)

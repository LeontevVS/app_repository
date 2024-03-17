import uvicorn
from fastapi import FastAPI

from api import router


app = FastAPI()

app.include_router(router)


uvicorn.run(app=app, host='localhost', port=8080)

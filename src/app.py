import uvicorn
from fastapi import FastAPI

from modules.auth.api import router as auth_router
from modules.test_module.api import router as test_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(test_router)


uvicorn.run(app=app, host='localhost', port=8080)

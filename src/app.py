from fastapi import FastAPI

from routing.landings import router as landings_routing


app = FastAPI()

app.include_router(landings_routing)

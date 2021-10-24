from fastapi import FastAPI
from routes.car import car
from routes.concesionary import conc

app = FastAPI()
app.include_router(car)
app.include_router(conc)


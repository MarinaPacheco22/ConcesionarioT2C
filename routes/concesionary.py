from fastapi import APIRouter
from config.db import conn
from schemas.concesionary import concEntity, concsEntity
from models.concesionary import Concesionary
from bson import ObjectId

conc = APIRouter()

### CONCESIONARIOS ###
@conc.get('/concesionarios')
def find_all_concs():
    return concsEntity(conn.ConcesionarioT2C.concesionarios.find())

@conc.get('/concesionarios/{id}')
def find_conc(id):
    return concEntity(conn.ConcesionarioT2C.concesionarios.find_one({"_id": ObjectId(id)}))

@conc.post('/concesionarios')
def create_concs(concesionario: Concesionary):
    conn.ConcesionarioT2C.concesionarios.insert_one(dict(concesionario))
    return 'Se ha insertado el nuevo concesionario'

@conc.delete('/concesionarios/{id}')
def delete_concs(id):
    concEntity(conn.ConcesionarioT2C.concesionarios.find_one_and_delete({"_id": ObjectId(id)}))
    return 'Se ha borrado el concesionario con éxito'
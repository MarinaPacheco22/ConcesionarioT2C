from fastapi import APIRouter

from config.db import conn
from schemas.car import carEntity, carsEntity
from models.car import Car, CarUpdate
from bson import ObjectId

car = APIRouter()


### COCHES ###
@car.get('/coches')
def find_all_cars():
    return carsEntity(conn.ConcesionarioT2C.coches.find())


@car.get('/coches/{id}')
def find_car(id):
    return carEntity(conn.ConcesionarioT2C.coches.find_one({"_id": ObjectId(id)}))


@car.post('/coches')
def create_car(car: Car):
    matricula = car.matricula
    if matricula == "":
        return 'No se aceptan coches sin matricular'

    for c in carsEntity(conn.ConcesionarioT2C.coches.find()):
        if matricula == c['matricula']:
            return 'Ya existe un coche con esta matrícula'

    coste = str(car.coste)
    if not coste.isnumeric():
        rango = len(coste)
        print(rango)
        i = 0
        print(i < rango)
        print(coste[i].isnumeric())
        while i < rango and coste[i].isnumeric():
            i = i+1

        euros = coste[0:i]
        centimos = coste[i+1:rango]
        if centimos == '':
            res1 = float(euros)
        else:
            res1 = float(euros + '.' + centimos)
        car.coste = res1
    else:
        car.coste = float(car.coste)
    precio = str(car.precio_de_venta)
    if precio != "":
        if not precio.isnumeric():
            rango = len(precio)
            i = 0
            while i < rango and precio[i].isnumeric():
                i = i + 1

            euros = precio[0:i]
            centimos = precio[i + 1:rango]
            if centimos == '':
                res2 = float(euros)
            else:
                res2 = float(euros + '.' + centimos)
            car.precio_de_venta = res2
        car.precio_de_venta = float(car.precio_de_venta)
    conn.ConcesionarioT2C.coches.insert_one(dict(car))
    return 'Añadido'


@car.patch('/coches/{id}')
def sell_car(id, car: CarUpdate):
    coche = conn.ConcesionarioT2C.coches.find_one({"_id": ObjectId(id)})

    if coche['vendido'] == False:
        info_coche = Car(**coche)  # Recuperamos los datos (no recupera datetime)
        precio = str(car.precio_de_venta)
        if not precio.isnumeric():
            rango = len(precio)
            i = 0
            while i < rango and precio[i].isnumeric():
                i = i + 1

            euros = precio[0:i]
            centimos = precio[i + 1:rango]
            if centimos == '':
                res = float(euros)
            else:
                res = float(euros + '.' + centimos)
            car.precio_de_venta = res
        else:
            car.precio_de_venta = float(car.precio_de_venta)
        coche_actualizado = info_coche.copy(update=dict(car)) # Copia los datos, actualizando los campos
        carEntity(conn.ConcesionarioT2C.coches.find_one_and_update({"_id": ObjectId(id)},
                                                                          {"$set": dict(coche_actualizado)}))
        return 'Coche actualizado'
    else:
        return 'Este coche ya ha sido vendido'


@car.delete('/coches/{id}')
def delete_car(id):
    coche = conn.ConcesionarioT2C.coches.find_one({"_id": ObjectId(id)})
    if coche['vendido'] == True:
        return 'No se puede dar de baja un coche vendido'
    else:
        carEntity(conn.ConcesionarioT2C.coches.find_one_and_delete({"_id": ObjectId(id)}))
        return 'Coche dado de baja correctamente'

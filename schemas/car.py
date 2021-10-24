from bson import ObjectId

from config.db import conn


def carEntity(item) -> dict:  # Devuelve un dict
    id_conc = item['concesionario'];
    conc = conn.ConcesionarioT2C.concesionarios.find_one({"_id": ObjectId(id_conc)})

    return {
        "id": str(item["_id"]),
        "marca": item["marca"],
        "coste": item["coste"],
        "fecha_de_ingreso": item["fecha_de_ingreso"],
        "vendido": item["vendido"],
        "matricula": item["matricula"],
        "precio_de_venta": item["precio_de_venta"],
        "concesionario": conc["direccion"]
    }


def carsEntity(entity) -> list:
    return [carEntity(item) for item in entity]  # Por cada item en la lista, genera un coche
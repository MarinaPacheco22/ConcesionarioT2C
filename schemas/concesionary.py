def concEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "direccion": item["direccion"]
    }


def concsEntity(entity) -> list:
    return [concEntity(item) for item in entity]

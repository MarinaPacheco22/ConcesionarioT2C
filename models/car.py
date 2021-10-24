from pydantic import BaseModel
from typing import Optional

class Car(BaseModel):
    marca: str
    coste: str
    fecha_de_ingreso: str
    vendido: bool
    matricula: str
    precio_de_venta: Optional[str] = "0"
    concesionario: str

class CarUpdate(BaseModel):
    precio_de_venta: str
    vendido: bool = True

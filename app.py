from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

# Instancia de una aplicacion
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/ConcesionarioT2C"
mongo = PyMongo(app)

### Peticiones requeridas ###

# Ver lista de coches
@app.route('/coches', methods=['GET'])
def get_cars():
    cars = mongo.db.coches
    output = []
    for c in cars.find():
        output.append({'marca': c['marca'],
                       'coste': c['coste'],
                       'fecha_de_ingreso': c['fecha_de_ingreso'],
                       'vendido': c['vendido'],
                       'matricula': c['matricula'],
                       'precio_de_venta': c['precio_de_venta']})
    return jsonify({'result': output})


# Ver info de un coche
@app.route('/coches/<matricula>', methods=['GET'])
def get_car(matricula):
    coche = mongo.db.coches
    c = coche.find_one({'matricula': matricula})
    if c:
        concesionario = mongo.db.concesionarios
        cc = concesionario.find_one({'_id': ObjectId(c['concesionario'])})
        output = {'marca': c['marca'],
                  'coste': c['coste'],
                  'fecha_de_ingreso': c['fecha_de_ingreso'],
                  'vendido': c['vendido'],
                  'matricula': c['matricula'],
                  'precio_de_venta': c['precio_de_venta'],
                  'concesionario': cc['direccion']}
    else:
        output = "Coche no encontrado"
    return jsonify({'result': output})

# Dar de baja aun coche
@app.route('/coches/<id>', methods=['DELETE'])
def delete_car(id):
    coche = mongo.db.coches.find_one({'_id': ObjectId(id)})
    if coche['vendido'] == True:
        response = 'No se puede dar de baja un coche vendido'
    else:
        mongo.db.coches.delete_one({'_id': ObjectId(id)})
        response = 'Se ha dado de baja el coche seleccionado'
    return response


# Actualizar un coche
@app.route('/coches/<id>', methods=['PUT'])
def sold_car(id):
    coche = mongo.db.coches.find_one({'_id': ObjectId(id)})

    if coche['vendido'] == False:
        precio_venta_final = request.json['precio_de_venta']
        mongo.db.coches.update_one({'_id': ObjectId(id)}, {'$set': {
            'precio_de_venta': precio_venta_final,
            'vendido': True
        }})
        return 'Actualizado'

    else:
        return ('Este coche ya ha sido vendido')


### Peticiones extra

# Coches en db
@app.route('/cochesbd', methods=['GET'])
def get_coches_db():
    coches = mongo.db.concesionarios.find()
    response = json_util.dumps(coches)
    return Response(response, mimetype='application/json')


# Concesionarios en db
@app.route('/concesionarios', methods=['GET'])
def get_concesionaries():
    concesionarios = mongo.db.concesionarios.find()
    response = json_util.dumps(concesionarios)
    return Response(response, mimetype='application/json')


# Ver info de un concesionario
@app.route('/concesionarios/<id>', methods=['GET'])
def get_concesionary(id):
    concesionario = mongo.db.concesionarios.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(concesionario)
    return Response(response, mimetype='application/json')


# Anadir un coche
@app.route('/coches', methods=['POST'])
def add_car():
    # Recibe datos del formulario
    marca = request.json['marca']
    coste = request.json['coste']
    fecha_ingreso = request.json['fecha_de_ingreso']
    vendido = request.json['vendido']
    matricula = request.json['matricula']
    precio_venta = request.json['precio_de_venta']
    concesionario = request.json['concesionario']

    if (marca and coste and fecha_ingreso and vendido and matricula and precio_venta and concesionario) != None:
        id = mongo.db.coches.insert_one(
            {'marca': marca,
             'coste': coste,
             'fecha_de_ingreso': fecha_ingreso,
             'vendido': vendido,
             'matricula': matricula,
             'precio_de_venta': precio_venta,
             'concesionario': concesionario}
        )
        response = 'Coche añadido correctamente'
        return response

    else:
        return 'Error'


# Anadir un concesionario
@app.route('/concesionarios', methods=['POST'])
def add_concesionary():
    # Recibe datos del formulario
    direccion = request.json['direccion']

    if direccion:
        id = mongo.db.concesionarios.insert(
            {'direccion': direccion}
        )
        response = {
            'id': str(id),
            'direccion': direccion
        }
        return response

    else:
        return {'Error___'}


# Al hacer un cambio, reinicia
if __name__ == "__main__":
    app.run(debug=True)

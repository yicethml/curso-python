from flask import Flask, request, jsonify # Importamos jsonify para devolver diccionarios Python como JSON

app = Flask(__name__)

# --- Base de Datos (Diccionario) ---
plants = {"1": {"name": "ROMERO",
    "family": "Lamiaceae",
    "size": "Evergreen shrub, typically 3-6 feet (1-2 meters) tall",
    "leaves": "Needle-like, small, dark green above and white underneath",
    "scent": "Pungent, woody, and evergreen"},
    
    "2": {"name": "MENTA",
    "family": "Lamiaceae",
    "size": "1 meters tall",
    "leaves": "Mint Leaves",
    "scent": "Highly aromatic, cooling, and refreshing (due to menthol)"},
    
    "3": {"name": "TOMILLO",
    "family": "Lamiaceae",
    "size": "Low-growing woody perennial, usually under 12 inches (30 cm) tall",
    "leaves": "Tiny, oval, and slightly curled at the edges",
    "scent": "Herbal, earthy, slightly floral"},
    
    "4": {"name": "ALBAHACA",
    "family": "Lamiaceae",
    "size": "1 - 2 meters tall",
    "leaves": "Large, ovate, and bright green (can be purple in some varieties)",
    "scent": "Sweet, slightly spicy, and highly fragrant"},
    
    "5": {"name": "HINOJO",
    "family": "Apiaceae",
    "size": "60 cm tall",
    "leaves": "Fennel Fronds",
    "scent": "Anise-like (or licorice-like), sweet, aromatic"}}

# --- ENDPOINTS ---

@app.route('/')
def home():
    """Ruta de inicio."""
    return "<h1>Welcome greenhouse Yiyi</h1>"

# 1. Obtener detalles de una planta por ID
@app.route('/api/plant/<string:id>')
def get_plant_by_id(id):
    """Obtiene una planta por su ID (clave del diccionario)."""
    if id in plants:
        return jsonify(plants[id]), 200
    else:
        # Error 404 (Not Found) 
        return jsonify({"message": f"Plant with ID {id} not found"}), 404

# 2. Obtener todas las plantas (Opcional, pero útil para una API)
@app.route('/api/plants')
def get_all_plants():
    #"""Devuelve la lista completa de plantas."""
    #Obtener los parametros por defecto son None.
    name_filter = request.args.get("name")
    family_filter = request.args.get("family")

# Obtener todas las plantas como una lista de diccionarios
    all_plants_list = list(plants.values())
    filtered_plants = all_plants_list

    if name_filter:
        # Filtrar por nombre (sin distinción de mayúsculas/minúsculas) usando filter y lambda
        filtered_plants = list(filter(
            lambda plant: plant["name"].lower() == name_filter.lower(),
            filtered_plants
    ))

    if family_filter:
        # Filtrar por familia (sin distinción de mayúsculas/minúsculas) usando filter y lambda
        # Se usa 'in' para permitir búsquedas parciales en la familia (más robusto)
        filtered_plants = list(filter(
            lambda plant: family_filter.lower() in plant["family"].lower(),
            filtered_plants
    ))
    # Devolver la lista de plantas filtradas (o todas si no hay filtros)
    return jsonify(filtered_plants), 200

# Adicionar una planta con el metodo POST
@app.route('/api/plant', methods = ["POST"])
def add_plant():
    body = request.json
    plant_id = str(body["id"])
    if plant_id in plants:
        return {"message": "Plant with id" + plant_id + "already exist"}, 409
    else:
        del body["id"]
        plants[plant_id] = body
        return plants[plant_id],201 # 201 created

# Eliminar una planta con el metodo DELETE
@app.route('/api/plant/<string:id>', methods = ["DELETE"])
def delete_plant(id): 
    if id not in plants:
        return {"message": "Plant with id " + id + " dont found"},208
    else:
        del plants[id]
        return {"message": "Plant with id " + id + " successfully deleted"},200

if __name__ == '__main__':
    # Usamos puerto 8000 como lo especificaste
    app.run(debug=True, port=8000, host='0.0.0.0')

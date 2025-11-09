from flask import Flask, Response, request, send_file
from flask_cors import CORS
from flasgger import Swagger
import sqlite3
import io

import import_snus

DATABASE = "db.sqlite"
SNUS_TYPES = ['loose', 'white', 'original', 'nicotine_pouch', 'other']
DEFAULT_THUMBNAIL = None
with open("default_thumbnail.webp", "rb") as f:
    DEFAULT_THUMBNAIL = f.read()


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS location (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            ) STRICT
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS snus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                rating INTEGER CHECK(rating >= 0 AND rating <= 10),
                nicotine_g REAL CHECK(nicotine_g >= 0),
                nicotine_portion REAL CHECK(nicotine_portion >= 0),
                portion_g REAL CHECK(portion_g > 0),
                type TEXT CHECK(type in (%s))
            ) STRICT
        """ % ", ".join([f"'{t}'" for t in SNUS_TYPES]))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS image (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snusid INTEGER NOT NULL,
                file BLOB,
                mime TEXT,
                FOREIGN KEY(snusid) REFERENCES snus(id)
            ) STRICT
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS snus_location (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snusid INTEGER NOT NULL,
                locationid INTEGER NOT NULL,
                amount INTEGER,
                FOREIGN KEY(snusid) REFERENCES snus(id),
                FOREIGN KEY(locationid) REFERENCES location(id)
            ) STRICT
        """)
        conn.commit()


app = Flask(__name__)
CORS(app)
app.config['SWAGGER'] = {
    'title': 'Snusmanager API',
    'uiversion': 3,
    'termsOfService': None,
    'version': "0.1.0"
}
swagger = Swagger(app)
init_db()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/locations")
def get_locations():
    """
    get all locations
    ---
    responses:
      200:
        description: A list of locations
    """
    conn = get_db_connection()
    locations = conn.execute("SELECT * FROM location").fetchall()
    return [dict(l) for l in locations]


@app.route("/api/locations/<string:name>", methods=["POST"])
def post_location(name: str):
    """
    create a location
    ---
    parameters:
      - name: name
        description: location name
        in: path
        type: string
        required: true
    responses:
      200:
        description: location created successfully
    """
    conn = get_db_connection()
    locations = conn.execute(f"INSERT INTO location(name) VALUES (?)", (name,))
    conn.commit()
    return Response(status=200)


@app.route("/api/snus")
def get_snus():
    """
    get a list of every snus
    ---
    parameters:
      - name: type
        type: string
        required: false
        description: only return snus with this type
    responses:
      200:
        description: A list of snus
    """
    snustype = request.args.get("type")
    if snustype is None:
        conn = get_db_connection()
        snus = conn.execute("SELECT * FROM snus").fetchall()
        return [dict(s) for s in snus]
    elif snustype in SNUS_TYPES:
        conn = get_db_connection()
        snus = conn.execute("SELECT * FROM snus WHERE type = ?", (snustype, )).fetchall()
        return [dict(s) for s in snus]
    else:
        return {"error": "Invalid snus type"}, 400


@app.route('/api/snus', methods=['POST'])
def add_snus():
    """
    add a snus
    ---
    responses:
      200:
        description: A list of snus
    """
    # Get the data from the request
    data = request.json
    
    # Validate the data
    if not data:
        return {"error": "No data provided in the request"}, 400
    
    name = data.get('name')
    description = data.get('description')
    rating = data.get('rating')
    nicotine_g = data.get('nicotine_g')
    nicotine_portion = data.get('nicotine_portion')
    portion_g = data.get('portion_g')
    snustype = data.get('type')
    
    # Check if required fields are present
    if not name:
        return {"error": "Missing name"}, 400

    # Ensure the type is in the allowed types
    if snustype not in SNUS_TYPES:
        return {"error": "Invalid snus type"}, 400

    # Insert the snus into the database
    try:
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO snus (name, description, rating, nicotine_g, nicotine_portion, portion_g, type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, description, rating, nicotine_g, nicotine_portion, portion_g, snustype))
        conn.commit()
        return Response(status=200)
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


@app.route("/api/snus/<int:snusid>", methods=['DELETE'])
def delete_snus(snusid: int):
    """
    delete a snus
    ---
    parameters:
      - name: snusid
        type: int
        required: true
    responses:
      200:
        description: snus deleted successfully
    """
    conn = get_db_connection()
    conn.execute("DELETE FROM snus WHERE id = ?", (snusid, ))
    conn.execute("DELETE FROM image WHERE snusid = ?", (snusid, ))
    conn.execute("DELETE FROM snus_location WHERE snusid = ?", (snusid, ))
    conn.commit()
    return Response(status=200)


@app.route("/api/snus/from_url", methods=['POST'])
def add_snus_from_url():
    """
    import a snus from a url
    ---
    parameters:
      - name: type
        type: string
        required: false
        description: only return snus with this type
    responses:
      200:
        description: A list of snus types
    """
    # Get the data from the request
    data = request.json
    
    # Validate the data
    if not data:
        return {"error": "No data provided in the request"}, 400
    
    url = data.get('url')

    # Check if required fields are present
    if not url:
        return {"error": "Missing url"}, 400

    try:
        snus = import_snus.import_snus(url)
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO snus (name, description, rating, nicotine_g, nicotine_portion, portion_g, type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (snus.name, snus.description, snus.rating, snus.nicotine_g, snus.nicotine_portion, snus.portion_g, snus.snustype))
        conn.commit()
        snusid = conn.execute("SELECT MAX(id) FROM snus WHERE name = ?", (snus.name, )).fetchone()[0]
        print(f"id = {snusid}")
        if snus.image is not None and snus.image_mime is not None:
            conn.execute("INSERT INTO image (snusid, file, mime) VALUES (?, ?, ?)", (snusid, snus.image, snus.image_mime))
            conn.commit()
        return Response(status=200)
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


@app.route("/api/snustypes")
def get_snustypes():
    """
    get a list of every snus type
    ---
    responses:
      200:
        description: A list of snus types
    """
    return SNUS_TYPES


@app.route("/api/thumbnail/<int:snusid>")
def get_thumbnail(snusid: int):
    """
    get a thumbnail image for a snus
    ---
    parameters:
      - name: snusid
        type: int
        required: true
    responses:
      200:
        description: An image
    """
    conn = get_db_connection()
    image = conn.execute("SELECT file, mime FROM image WHERE snusid = ?", (snusid, )).fetchone()
    if image is not None:
        return send_file(io.BytesIO(image[0]), mimetype=image[1])
    else:
        return send_file(io.BytesIO(DEFAULT_THUMBNAIL), mimetype='image/webp')

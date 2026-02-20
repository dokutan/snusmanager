from flask import Flask, Response, request, send_file, send_from_directory
from flask_cors import CORS
import sqlite3
import io
import base64

import import_snus
import calculate_missing
import crop_image
import convert_image
from snus import Snus

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
                weight_g REAL CHECK(weight_g > 0),
                portions INTEGER CHECK(portions > 0),
                type TEXT CHECK(type in (%s)),
                brand TEXT
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
app.logger.setLevel("INFO")
init_db()

@app.route("/api/locations")
def get_locations():
    """
    get all locations
    ---
    responses:
      200:
        description: A list of locations
    """
    try:
        conn = get_db_connection()
        locations = conn.execute("SELECT * FROM location").fetchall()
        return [dict(l) for l in locations]
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


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
    try:
        conn = get_db_connection()
        locations = conn.execute(f"INSERT INTO location(name) VALUES (?)", (name,))
        conn.commit()
        return Response(status=200)
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


@app.route("/api/locations/<int:locationid>", methods=['DELETE'])
def delete_location(locationid: int):
    """
    delete a location
    ---
    parameters:
      - name: locationid
        type: int
        required: true
    responses:
      200:
        description: location deleted successfully
    """
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM location WHERE id = ?", (locationid, ))
        conn.execute("DELETE FROM snus_location WHERE locationid = ?", (locationid, ))
        conn.commit()
        return Response(status=200)
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


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
    try:
        snustype = request.args.get("type")
        snuslist = []
        if snustype is None:
            conn = get_db_connection()
            snus = conn.execute("SELECT * FROM snus").fetchall()
            snuslist = [dict(s) for s in snus]
        elif snustype in SNUS_TYPES:
            conn = get_db_connection()
            snus = conn.execute("SELECT * FROM snus WHERE type = ?", (snustype, )).fetchall()
            snuslist = [dict(s) for s in snus]
        else:
            return {"error": "Invalid snus type"}, 400

        for snus in snuslist:
            amount_per_location = conn.execute("SELECT locationid, amount FROM snus_location WHERE snusid = ?", (snus["id"], )).fetchall()
            snus["locations"] = [{"id": l[0], "amount": l[1]} for l in amount_per_location]
        return snuslist
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


@app.route("/api/snus/<int:snusid>")
def get_snus_by_id(snusid: int):
    """
    get a snus by id
    ---
    responses:
      200:
        description: A list of snus
    """
    try:
        conn = get_db_connection()
        snus = conn.execute("SELECT * FROM snus WHERE id = ?", (snusid, )).fetchone()
        if snus is None:
            return {"error": "No snus with id %s" % snusid}, 400
        snus = dict(snus)
        amount_per_location = conn.execute("SELECT locationid, amount FROM snus_location WHERE snusid = ?", (snusid, )).fetchall()
        snus["locations"] = [{"id": l[0], "amount": l[1]} for l in amount_per_location]
        return snus
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


@app.route('/api/snus', methods=['POST'])
def add_snus():
    """
    add a snus
    ---
    responses:
      200:
        description: A list of snus
    """
    try:
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
        weight_g = data.get('weight_g')
        portions = data.get('portions')
        snustype = data.get('type')
        brand = data.get('brand')

        # Check if required fields are present
        if not name:
            return {"error": "Missing name"}, 400

        # Ensure the type is in the allowed types
        if snustype not in SNUS_TYPES:
            return {"error": "Invalid snus type"}, 400

        # Insert the snus into the database
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO snus (name, description, rating, nicotine_g, nicotine_portion, portion_g, weight_g, portions, type, brand)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, description, rating, nicotine_g, nicotine_portion, portion_g, weight_g, portions, snustype, brand))
        conn.commit()

        if "thumbnail_base64" in data.keys() and "thumbnail_mime" in data.keys():
            snusid = conn.execute("SELECT MAX(id) FROM snus WHERE name = ?", (name, )).fetchone()[0]
            conn.execute("INSERT INTO image (snusid, file, mime) VALUES (?, ?, ?)", (snusid, base64.decodebytes(data.get("thumbnail_base64").encode("ascii")), data.get("thumbnail_mime")))
            conn.commit()

        return Response(status=200)
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


@app.route('/api/snus/<int:snusid>', methods=['PATCH'])
def update_snus(snusid: int):
    """
    update a snus
    ---
    parameters:
      - name: snusid
        type: int
        required: true
    responses:
      200:
        description: snus updated successfully
    """
    try:
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
        weight_g = data.get('weight_g')
        portions = data.get('portions')
        snustype = data.get('type')
        brand = data.get('brand')
        locations = data.get('locations')
        thumbnail_base64 = data.get("thumbnail_base64")
        thumbnail_mime = data.get("thumbnail_mime")

        # Ensure the type is in the allowed types
        if snustype and snustype not in SNUS_TYPES:
            return {"error": "Invalid snus type"}, 400

        # Update the snus in the database
        conn = get_db_connection()
        if "name" in data.keys(): conn.execute("UPDATE snus SET name = ? WHERE id = ?", (name, snusid))
        if "description" in data.keys(): conn.execute("UPDATE snus SET description = ? WHERE id = ?", (description, snusid))
        if "rating" in data.keys(): conn.execute("UPDATE snus SET rating = ? WHERE id = ?", (rating, snusid))
        if "nicotine_g" in data.keys(): conn.execute("UPDATE snus SET nicotine_g = ? WHERE id = ?", (nicotine_g, snusid))
        if "nicotine_portion" in data.keys(): conn.execute("UPDATE snus SET nicotine_portion = ? WHERE id = ?", (nicotine_portion, snusid))
        if "portion_g" in data.keys(): conn.execute("UPDATE snus SET portion_g = ? WHERE id = ?", (portion_g, snusid))
        if "weight_g" in data.keys(): conn.execute("UPDATE snus SET weight_g = ? WHERE id = ?", (weight_g, snusid))
        if "portions" in data.keys(): conn.execute("UPDATE snus SET portions = ? WHERE id = ?", (portions, snusid))
        if "type" in data.keys(): conn.execute("UPDATE snus SET type = ? WHERE id = ?", (snustype, snusid))
        if "brand" in data.keys(): conn.execute("UPDATE snus SET brand = ? WHERE id = ?", (brand, snusid))
        if "thumbnail_base64" in data.keys() and "thumbnail_mime" in data.keys():
            conn.execute("DELETE FROM image WHERE snusid = ?", (snusid, ))
            conn.execute("INSERT INTO image (snusid, file, mime) VALUES (?, ?, ?)", (snusid, base64.decodebytes(thumbnail_base64.encode("ascii")), thumbnail_mime))
        if "locations" in data.keys():
            for l in locations:
                locationid = int(l["id"])
                amount = int(l["amount"])
                conn.execute("DELETE FROM snus_location WHERE locationid = ? AND snusid = ?", (locationid, snusid))
                if amount > 0: conn.execute("INSERT INTO snus_location (locationid, snusid, amount) VALUES (?, ?, ?)", (locationid, snusid, amount))
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
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM snus WHERE id = ?", (snusid, ))
        conn.execute("DELETE FROM image WHERE snusid = ?", (snusid, ))
        conn.execute("DELETE FROM snus_location WHERE snusid = ?", (snusid, ))
        conn.commit()
        return Response(status=200)
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


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
    try:
        # Get the data from the request
        data = request.json

        # Validate the data
        if not data:
            return {"error": "No data provided in the request"}, 400

        url = data.get('url')

        # Check if required fields are present
        if not url:
            return {"error": "Missing url"}, 400

        snus = import_snus.import_snus(url)
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO snus (name, description, rating, nicotine_g, nicotine_portion, portion_g, weight_g, portions, type, brand)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (snus.name, snus.description, snus.rating, snus.nicotine_g, snus.nicotine_portion, snus.portion_g, snus.weight_g, snus.portions, snus.snustype, snus.brand))
        conn.commit()
        snusid = conn.execute("SELECT MAX(id) FROM snus WHERE name = ?", (snus.name, )).fetchone()[0]
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
    try:
        conn = get_db_connection()
        image = conn.execute("SELECT file, mime FROM image WHERE snusid = ? ORDER BY CASE WHEN mime = 'image/webp' THEN 1 ELSE 2 END", (snusid, )).fetchone()
        if image is not None:
            return send_file(io.BytesIO(image[0]), mimetype=image[1])
        else:
            return send_file(io.BytesIO(DEFAULT_THUMBNAIL), mimetype='image/webp')
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


@app.route("/api/calculate_missing", methods=["POST"])
def calculate_missing_values():
    """
    calculate missing values
    ---
      200:
        description: Ok
    """
    try:
        conn = get_db_connection()
        all_snus = conn.execute("SELECT * FROM snus").fetchall()
        result = []
        for s in all_snus:
            s = dict(s)
            snus = Snus()
            snus.nicotine_g = s["nicotine_g"]
            snus.nicotine_portion = s["nicotine_portion"]
            snus.portion_g = s["portion_g"]
            snus.weight_g = s["weight_g"]
            snus.portions = s["portions"]
            snus = calculate_missing.calculate_missing(snus)
            if snus:
                result.append({"id": s["id"], "name": s["name"], "solver_status": "satisfied"})
                conn.execute("UPDATE snus SET nicotine_g = ? WHERE id = ? AND nicotine_g IS NULL", (round(snus.nicotine_g, 2), s["id"]))
                conn.execute("UPDATE snus SET nicotine_portion = ? WHERE id = ? AND nicotine_portion IS NULL", (round(snus.nicotine_portion, 2), s["id"]))
                conn.execute("UPDATE snus SET portion_g = ? WHERE id = ? AND portion_g IS NULL", (round(snus.portion_g, 2), s["id"]))
                conn.execute("UPDATE snus SET weight_g = ? WHERE id = ? AND weight_g IS NULL", (round(snus.weight_g, 2), s["id"]))
                conn.execute("UPDATE snus SET portions = ? WHERE id = ? AND portions IS NULL", (snus.portions, s["id"]))
                conn.commit()
            else:
                result.append({"id": s["id"], "name": s["name"], "solver_status": "unsatisfied"})
        return result
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


@app.route("/api/crop_images", methods=["POST"])
def crop_images():
    """
    remove any transparent border around images
    ---
      200:
        description: Ok
    """
    try:
        conn = get_db_connection()
        images = conn.execute("SELECT id, file FROM image").fetchall()
        for row in images:
            cropped = crop_image.crop_image(row[1])
            if cropped:
                conn.execute("UPDATE image SET file = ? WHERE id = ?", (cropped, row[0]))
                conn.execute("UPDATE image SET mime = 'image/png' WHERE id = ?", (row[0], ))
                conn.commit()
                app.logger.info("cropped image %s", row[0])
        return Response(status=200)
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


@app.route("/api/convert_images", methods=["POST"])
def convert_images():
    """
    create webp versions of all images
    ---
      200:
        description: Ok
    """
    try:
        conn = get_db_connection()
        images = conn.execute("SELECT snusid, file FROM image WHERE snusid NOT IN (SELECT DISTINCT snusid FROM image WHERE mime = 'image/webp')").fetchall()
        for row in images:
            converted = convert_image.convert_image(row[1])
            if converted:
                conn.execute("INSERT INTO image (snusid, file, mime) VALUES (?, ?, ?)", (row[0], converted, "image/webp"))
                conn.commit()
                app.logger.info("converted image %s to webp", row[0])
        return Response(status=200)
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}, 500


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('dist/snusmanager/browser', path)

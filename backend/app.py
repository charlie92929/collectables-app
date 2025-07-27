from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import datetime
import os

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app=Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

db=SQLAlchemy(app)


class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    tags = db.Column(db.String(121), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    def to_dict(self): 
        return { 
            "id": self.item_id,
            "name": self.name, 
            "image": self.image,
            "description": self.description,
            "tags": self.tags.split(',') if self.tags else [],
            "date_created": self.date_created
        }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS       

@app.before_request
def create_table():
    db.create_all()

@app.route('/')
def hello():
    return'hello world'

@app.route('/upload', methods=["POST"])
def upload():
    if 'image' not in request.files:
        return jsonify({'message': 'no file in request'}, 400)
     # old
    # {
    #     'item': "Charizard"
    # }
    # new
    # {
    #     'name': "Charizard",
    #     'description': "A rare pokemon you can only get if you're lucky",
    #     'tags': "shiny, epic",
    #     'image': charizard.png,
    #     'date_created': 2025-07-27::18:16:26
    # }
    name = request.form.get('name')
    description = request.form.get('description')
    tags = request.form.get('tags')

    filename = None
    if 'image' in request.files:
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
    # Creates a new instance of the item class
    # Item(id, "Charizard")
    # converts it to an item that we can actually perform actions on 
    # name, description, tags, image
    new_item = Item(
        # name of new database item = name of item we are uploading to backend
        name=name,
        description=description,
        tags=tags,
        image=f'/uploads/{filename}'
    )
    # add new_item to database
    db.session.add(new_item)
    # complete  the transaction
    db.session.commit()
    return jsonify(f"Item {name} has been added")

@app.route('/uploads/<filename>')
def display_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/items')
def items():
    # Render all items in the database in dictionary format
    return jsonify([item.to_dict() for item in Item.query.all()])

if __name__ == '__main__':
    app.run(debug=True)

# to run: source virtual_env/bin/activate && python3 app.

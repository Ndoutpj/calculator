from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "url": self.url}

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/api/images', methods=['GET'])
def get_images():
    images = Image.query.all()
    return jsonify([img.to_dict() for img in images])

@app.route('/api/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Image.query.get(image_id)
    if image:
        return jsonify(image.to_dict())
    return jsonify({"error": "Image not found"}), 404

@app.route('/api/images', methods=['POST'])
def add_image():
    data = request.get_json()
    new_image = Image(name=data.get("name"), url=data.get("url"))
    db.session.add(new_image)
    db.session.commit()
    return jsonify(new_image.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)
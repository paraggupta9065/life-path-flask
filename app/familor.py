from flask import request, jsonify
from app import app
from app.models.models import FamiliarFace, db, face_schema, faces_schema

@app.route('/faces', methods=['POST'])
def add_familiar_face():
    data = request.get_json()
    new_face = FamiliarFace(
        patient_id=data.get('patient_id'),
        name=data.get('name'),
        relationship=data.get('relationship'),
        photo_url=data.get('photo_url', ''),  # Optional
        voice_note_url=data.get('voice_note_url', '')  # Optional
    )
    db.session.add(new_face)
    db.session.commit()
    return face_schema.jsonify(new_face), 201

@app.route('/faces', methods=['GET'])
def get_familiar_faces():
    all_faces = FamiliarFace.query.all()
    return faces_schema.jsonify(all_faces)

@app.route('/faces/<int:id>', methods=['GET'])
def get_familiar_face(id):
    face = FamiliarFace.query.get_or_404(id)
    return face_schema.jsonify(face)

@app.route('/faces/<int:id>', methods=['PUT'])
def update_familiar_face(id):
    face = FamiliarFace.query.get_or_404(id)
    data = request.get_json()

    face.name = data.get('name', face.name)
    face.relationship = data.get('relationship', face.relationship)
    face.photo_url = data.get('photo_url', face.photo_url)
    face.voice_note_url = data.get('voice_note_url', face.voice_note_url)

    db.session.commit()
    return face_schema.jsonify(face)

@app.route('/faces/<int:id>', methods=['DELETE'])
def delete_familiar_face(id):
    face = FamiliarFace.query.get_or_404(id)
    db.session.delete(face)
    db.session.commit()
    return jsonify({'message': 'Familiar face deleted successfully'})
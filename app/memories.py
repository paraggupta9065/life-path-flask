import os
from flask import request, jsonify, url_for
from app import UPLOAD_FOLDER, app
from app.models.models import db, Memory, memory_schema, memories_schema

@app.route('/memories', methods=['POST'])
def add_memory():
    data = request.get_json()
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"

    if not file:
        return jsonify({'message': 'Image not found!'}), 400
        
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
        
    image_url = url_for('static', filename=f'uploads/{file.filename}', _external=True)
    
    new_memory = Memory(
        title=data.get('title'),
        description=data.get('description', ''),
        image_url=image_url,
        date=data.get('date')
    )
    db.session.add(new_memory)
    db.session.commit()
    return memory_schema.jsonify(new_memory), 201

@app.route('/memories', methods=['GET'])
def get_memories():
    all_memories = Memory.query.all()
    return memories_schema.jsonify(all_memories)

@app.route('/memories/<int:id>', methods=['GET'])
def get_memory(id):
    memory = Memory.query.get_or_404(id)
    return memory_schema.jsonify(memory)

@app.route('/memories/<int:id>', methods=['PUT'])
def update_memory(id):
    memory = Memory.query.get_or_404(id)
    data = request.get_json()

    memory.title = data.get('title', memory.title)
    memory.description = data.get('description', memory.description)
    memory.image_url = data.get('image_url', memory.image_url)
    memory.date = data.get('date', memory.date)

    db.session.commit()
    return memory_schema.jsonify(memory)

@app.route('/memories/<int:id>', methods=['DELETE'])
def delete_memory(id):
    memory = Memory.query.get_or_404(id)
    db.session.delete(memory)
    db.session.commit()
    return jsonify({'message': 'Memory deleted successfully'})
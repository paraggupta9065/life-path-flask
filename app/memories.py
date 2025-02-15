from flask import request, jsonify
from app import app
from app.models.models import db, Memory, memory_schema, memories_schema

@app.route('/memories', methods=['POST'])
def add_memory():
    data = request.get_json()
    new_memory = Memory(
        title=data.get('title'),
        description=data.get('description', ''),
        image_url=data.get('image_url', ''),
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
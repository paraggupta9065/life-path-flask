from flask import Flask, request, jsonify
from app import app

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Server up and running'}), 200
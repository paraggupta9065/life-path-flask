import base64
import os
import uuid
from app import UPLOAD_FOLDER, app
from flask import request, jsonify, url_for
from app import app
from app.models.models import FamiliarFace, db, face_schema, faces_schema
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

@app.route('/faces', methods=['POST'])
def add_familiar_face():
    return face_schema.jsonify(new_face), 201
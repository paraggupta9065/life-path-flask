from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app import app
from google import genai


@app.route('/gen_ai', methods=['GET'])
def gen_ai():

    client = genai.Client(api_key="AIzaSyCqOx08su_nmPiSZsUQ1ktLSOqmu3NXg6I")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="Explain how AI works"
    )
    
    return jsonify({'message': response.text})
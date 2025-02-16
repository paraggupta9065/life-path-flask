from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app import app
from google import genai


@app.route('/gen_ai', methods=['POST'])
def gen_ai():
    data = request.get_json()
    
    client = genai.Client(api_key="AIzaSyCYAQMATgLJY0dcTV9wBNKarrGzxFSg_Ek")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=data.get('message', ''),
    )
    
    return jsonify({'message': response.text})
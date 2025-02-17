import base64
import os
import uuid
from app import UPLOAD_FOLDER, app
from flask import request, jsonify, url_for # type: ignore
from app import app
from app.models.models import Answer, answer_schema, db
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request # type: ignore

@app.route('/answers', methods=['POST'])
def add_answer():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    try:
        data = request.json

        if "user_id" not in data:
            return jsonify({"message": "user_id is required!"}), 400

        if not data or 'image' not in data:
            return jsonify({'message': 'Image data is required!'}), 400

        image_data = data['image']
        mime_type = 'image/jpeg'
        
        if ',' in image_data:
            header, image_data = image_data.split(',', 1)
            mime_type = header.split(';')[0].split(':')[1]
        
        if mime_type not in ['image/jpeg', 'image/png']:
            return jsonify({'message': 'Unsupported image type. Only JPEG and PNG allowed!'}), 400

        file_ext = 'png' if 'png' in mime_type else 'jpg'
        
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            return jsonify({'message': 'Invalid base64 encoding', 'error': str(e)}), 400

        filename = f"memory_{user_id}_{uuid.uuid4().hex}.{file_ext}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        try:
            with open(file_path, 'wb') as img_file:
                img_file.write(image_bytes)
        except IOError as e:
            return jsonify({'message': 'Failed to save image', 'error': str(e)}), 500

        image_url = url_for('uploaded_file', filename=filename, _external=True)

        new_answer = Answer(
            answer_text=data.get("answer_text"),
            que=data.get("que"),
            user_id=user_id,
            image_url=image_url,
            scored=data.get("scored", 0),
        )
        db.session.add(new_answer)
        db.session.commit()

        return answer_schema.jsonify(new_answer), 201

    except Exception as e:
        return jsonify({"message": "Error saving answer", "error": str(e)}), 500
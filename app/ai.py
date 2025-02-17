from app.models.models import User, Memory, Reminder, FamiliarFace, Answer
from flask import request, jsonify
from app import app, db
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
import datetime
from google import genai

@app.route("/gen_ai", methods=["POST"])
def gen_ai():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    
    # Get the message from the request
    data = request.get_json()
    user_message = data.get("message", "")

    # Fetch user-specific data from the database
    user = User.query.get(user_id)
    reminders = Reminder.query.filter_by(user_id=user_id).all()
    memories = Memory.query.filter_by(user_id=user_id).all()
    familiar_faces = FamiliarFace.query.filter_by(user_id=user_id).all()
    answers = Answer.query.filter_by(user_id=user_id).all()

    context = {
        "purpose":"we want answer to given question in very few lines probably 3-4 lines no more and there will be no mention of context and any technical jargons direct text output for dementia patients",
        "user_id": user.id,
        "user_info": {
            "name": user.name,
            "email": user.email,
            "emergency_contact": user.emergency_contact,
 
        },
        "context": {
            "active_reminders": [
                {
                    "id": reminder.id,
                    "title": reminder.title,
                    "time": reminder.time,
                    "date": reminder.date,
                    "description": reminder.description,
                    "status": reminder.status
                }
                for reminder in reminders
            ],
            "memories": [
                {
                    "id": memory.id,
                    "title": memory.title,
                    "description": memory.description,
                    "image_url": memory.image_url,
                    "date": memory.date
                }
                for memory in memories
            ],
            "familiar_faces": [
                {
                    "id": face.id,
                    "name": face.name,
                    "relationship": face.relationship,
                    "image_url": face.image_url
                }
                for face in familiar_faces
            ],
         
        },
 
  
    }

    client = genai.Client(api_key="AIzaSyCYAQMATgLJY0dcTV9wBNKarrGzxFSg_Ek")

    input_contents = [
        user_message,  
        str(context)   
    ]

    # Generate a response using the AI model
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=input_contents  # Pass the input as a list
    )

    # Return the AI response
    return jsonify({"message": response.text})
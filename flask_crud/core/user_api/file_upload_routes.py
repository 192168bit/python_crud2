from flask import request, jsonify, current_app
from supabase import create_client
from . import file_upload_api_blueprint
from core.models import File
from core import database
from datetime import datetime

# Initialize Supabase client
def get_supabase():
    return create_client(
        current_app.config["SUPABASE_URL"],
        current_app.config["SUPABASE_KEY"]
    )

# Unified route for both uploading and getting files
@file_upload_api_blueprint.route('/files', methods=['GET', 'POST'])
def manage_files():
    if request.method == 'POST':
        # Handle file upload
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        file_path = f"uploads/{file.filename}"

        try:
            # Upload the file to Supabase storage
            supabase = get_supabase()
            res = supabase.storage.from_(current_app.config["SUPABASE_BUCKET"]).upload(file_path, file)

            if res.status_code != 200:
                return jsonify({'error': 'File upload failed'}), 500

            # Generate file URL
            file_url = f"{current_app.config['SUPABASE_URL']}/storage/v1/object/public/{current_app.config['SUPABASE_BUCKET']}/{file_path}"

            # Save file metadata to the database
            new_file = File(filename=file.filename, url=file_url, uploaded_at=datetime.utcnow())
            database.session.add(new_file)
            database.session.commit()

            return jsonify({
                "id": new_file.id,
                "filename": new_file.filename,
                "url": new_file.url,
                "uploaded_at": new_file.uploaded_at.isoformat()
            }), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'GET':
        # Handle file retrieval
        try:
            # Query the database to get the file metadata
            files = File.query.all()

            if not files:
                return jsonify({"message": "No files found"}), 404

            # Return file metadata
            file_data = []
            for file in files:
                file_data.append({
                    "id": file.id,
                    "filename": file.filename,
                    "url": file.url,
                    "uploaded_at": file.uploaded_at.isoformat()  # Convert to ISO format for JSON compatibility
                })

            return jsonify(file_data), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

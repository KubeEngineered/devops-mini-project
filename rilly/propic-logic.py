import os
from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)

# Configuration
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB in bytes
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
UPLOAD_FOLDER = 'uploads/profiles'

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def is_allowed_file(filename):
    """Check if the extension is strictly .jpg or .jpeg."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@app.route('/upload-profile-picture', methods=['POST'])
def upload_profile_picture():
    # 1. Check if an image file was sent in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # 2. Validate file extension
    if not is_allowed_file(file.filename):
        return jsonify({'error': 'Invalid file format. Only .jpg and .jpeg are allowed'}), 400

    # 3. Validate file size (under 5 MB)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset pointer back to beginning after checking size

    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': f'File size exceeds limit of 5MB ({file_size / (1024 * 1024):.2f}MB)'}), 400

    # 4. Deep validation: Verify it is genuinely a valid JPEG image (prevents renamed files)
    try:
        img = Image.open(file.stream)
        if img.format.upper() != 'JPEG':
            return jsonify({'error': 'File content is not a valid JPEG image'}), 400
        img.verify()
    except Exception:
        return jsonify({'error': 'Corrupted or invalid image file'}), 400

    # Reset file pointer again before saving
    file.seek(0)

    # 5. Save file safely (e.g., user_123_profile.jpg)
    user_id = request.form.get('user_id', 'default_user')
    save_filename = f"user_{user_id}_profile.jpg"
    file_path = os.path.join(UPLOAD_FOLDER, save_filename)

    file.save(file_path)

    return jsonify({
        'message': 'Profile picture uploaded successfully',
        'file_path': file_path
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import boto3
import os
from models import db, File
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
    region_name=os.getenv('AWS_REGION')
)
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    s3.upload_fileobj(file, BUCKET_NAME, filename)
    s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

    new_file = File(filename=filename, s3_url=s3_url)
    db.session.add(new_file)
    db.session.commit()

    return jsonify({'message': 'Arquivo enviado', 's3_url': s3_url}), 201

@app.route('/files', methods=['GET'])
def list_files():
    files = File.query.all()
    return jsonify([{'id': f.id, 'filename': f.filename, 's3_url': f.s3_url} for f in files])

@app.route('/file/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    s3.delete_object(Bucket=BUCKET_NAME, Key=file.filename)
    db.session.delete(file)
    db.session.commit()
    return jsonify({'message': 'Arquivo deletado'}), 200

@app.route('/file/<int:file_id>', methods=['PUT'])
def rename_file(file_id):
    file = File.query.get_or_404(file_id)
    new_name = request.json.get('new_name')

    copy_source = {'Bucket': BUCKET_NAME, 'Key': file.filename}
    s3.copy_object(Bucket=BUCKET_NAME, CopySource=copy_source, Key=new_name)
    s3.delete_object(Bucket=BUCKET_NAME, Key=file.filename)

    file.filename = new_name
    file.s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{new_name}"
    db.session.commit()

    return jsonify({'message': 'Arquivo renomeado', 's3_url': file.s3_url})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from caption_model import generate_caption

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['SECRET_KEY'] = 'your_secret_key'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Generate caption
            caption = generate_caption(file_path)

            return render_template('result.html', image_url=file_path, caption=caption)

    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)

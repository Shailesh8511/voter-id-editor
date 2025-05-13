from flask import Flask, request, render_template, send_file
from utils import process_voter_id
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    sd_pdf = request.files['sd_pdf']
    ssd_img = request.files['ssd_img']
    sd_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sd_input.pdf')
    ssd_img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'ssd_input.jpg')
    output_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'final_output.pdf')

    sd_pdf.save(sd_pdf_path)
    ssd_img.save(ssd_img_path)

    process_voter_id(sd_pdf_path, ssd_img_path, output_pdf_path)
    return send_file(output_pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

import os
import io
import zipfile
import datetime
import traceback
import pillow_avif
from flask import Flask, request, send_file, render_template, jsonify
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'files' not in request.files:
        return jsonify({'error': '尚未上傳檔案'}), 400
    
    files = request.files.getlist('files')
    quality = int(request.form.get('quality', 100))
    zip_filename = request.form.get('zipFilename', '').strip()
    
    if not files or files[0].filename == '':
        return jsonify({'error': '尚未選擇檔案'}), 400

    if not zip_filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"converted_images_{timestamp}.zip"
    elif not zip_filename.lower().endswith('.zip'):
        zip_filename += '.zip'

    print(f"[DEBUG] Processing {len(files)} files, quality={quality}, output={zip_filename}", flush=True)

    converted_files = []
    
    for i, file in enumerate(files):
        try:
            print(f"[DEBUG] Opening file {file.filename}", flush=True)
            img = Image.open(file.stream)
            avif_buffer = io.BytesIO()
            
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA') if 'A' in img.mode else img.convert('RGB')
                
            print(f"[DEBUG] Saving as AVIF with quality {quality}", flush=True)
            img.save(avif_buffer, format='AVIF', quality=quality)
            avif_buffer.seek(0)
            
            original_filename = file.filename
            avif_filename = original_filename.rsplit('.', 1)[0] + '.avif'
            
            converted_files.append((avif_filename, avif_buffer.getvalue()))
            print(f"[DEBUG] Appended {avif_filename}", flush=True)
        except Exception as e:
            print(f"[ERROR] Error processing image {file.filename}: {e}", flush=True)
            traceback.print_exc()
            continue

    if not converted_files:
        return jsonify({'error': '檔案轉換失敗，請確認檔案格式是否正確。'}), 500

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename, data in converted_files:
            zf.writestr(filename, data)
    
    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=zip_filename
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

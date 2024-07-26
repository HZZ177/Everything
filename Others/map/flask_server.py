from flask import Flask, request, jsonify, send_from_directory, url_for
import json
import os

app = Flask(__name__)

# 存储标记点的文件路径
MARKERS_FILE = 'markers.json'
# 存储图片的文件夹
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 加载现有的标记点数据
def load_markers():
    try:
        with open(MARKERS_FILE, 'r') as file:
            markers = json.load(file)
    except FileNotFoundError:
        markers = []
    return markers

# 保存标记点数据
def save_markers(markers):
    with open(MARKERS_FILE, 'w') as file:
        json.dump(markers, file)

@app.route('/add_marker', methods=['POST'])
def add_marker():
    marker = request.json
    markers = load_markers()
    markers.append(marker)
    save_markers(markers)
    return jsonify(success=True)

@app.route('/delete_marker', methods=['POST'])
def delete_marker():
    marker_id = request.json['id']
    markers = load_markers()
    markers = [marker for marker in markers if marker['id'] != marker_id]
    save_markers(markers)
    return jsonify(success=True)

@app.route('/edit_marker', methods=['POST'])
def edit_marker():
    updated_marker = request.json
    markers = load_markers()
    for marker in markers:
        if marker['id'] == updated_marker['id']:
            marker['description'] = updated_marker['description']
            break
    save_markers(markers)
    return jsonify(success=True)

@app.route('/get_markers', methods=['GET'])
def get_markers():
    markers = load_markers()
    for marker in markers:
        if 'image' in marker and marker['image']:
            marker['image'] = url_for('serve_upload', filename=marker['image'], _external=True)
    return jsonify(markers)

@app.route('/delete_marker', methods=['POST'])
def delete_marker():
    marker_data = request.json
    markers = load_markers()
    markers = [marker for marker in markers if not (marker['lat'] == marker_data['lat'] and marker['lon'] == marker_data['lon'])]
    save_markers(markers)
    return jsonify(success=True)

@app.route('/save_marker', methods=['POST'])
def save_marker():
    marker_data = request.json
    markers = load_markers()
    for marker in markers:
        if marker['lat'] == marker_data['lat'] and marker['lon'] == marker_data['lon']:
            marker['description'] = marker_data['description']
            if 'image' in marker_data and marker_data['image']:
                marker['image'] = marker_data['image']
    save_markers(markers)
    return jsonify(success=True)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    lat = request.form['lat']
    lon = request.form['lon']
    file = request.files['image']
    filename = f"{lat}_{lon}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    markers = load_markers()
    for marker in markers:
        if marker['lat'] == lat and marker['lon'] == lon:
            marker['image'] = filename  # 保存相对路径

    save_markers(markers)
    return jsonify(success=True, image=url_for('serve_upload', filename=filename, _external=True))

# 提供上传文件
@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 提供静态HTML文件
@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(debug=True)

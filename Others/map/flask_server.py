from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# 存储标记点的文件路径
MARKERS_FILE = 'markers.json'

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

@app.route('/get_markers', methods=['GET'])
def get_markers():
    markers = load_markers()
    return jsonify(markers)

# 提供静态HTML文件
@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(debug=True)

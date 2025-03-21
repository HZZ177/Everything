from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import uuid
import time

app = Flask(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传大小为16MB

# 确保上传文件夹和数据文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('data', exist_ok=True)

# 标记数据文件路径
MARKERS_FILE = 'data/markers.json'

# 如果标记数据文件不存在，创建一个空的JSON文件
if not os.path.exists(MARKERS_FILE):
    with open(MARKERS_FILE, 'w') as f:
        json.dump([], f)


@app.route('/')
def index():
    # 直接设置高德地图API密钥和安全码
    amap_key = '8ef795506531a55d59ba9ccdd9c58210'  # 高德key
    amap_security_code = '53fea11a3e89ff6aaf1e538b2f41eacc'  # 高德安全码
    return render_template('index.html', amap_key=amap_key, amap_security_code=amap_security_code)



@app.route('/api/markers', methods=['GET'])
def get_markers():
    try:
        with open(MARKERS_FILE, 'r') as f:
            markers = json.load(f)
        return jsonify(markers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/markers', methods=['POST'])
def add_marker():
    try:
        marker = request.get_json()
        if not marker:
            return jsonify({'error': 'Invalid JSON data'}), 400

        marker['id'] = str(uuid.uuid4())  # 为新标记生成唯一ID
        marker['createTime'] = time.time()
        marker['images'] = []  # 初始化为空图片列表

        with open(MARKERS_FILE, 'r') as f:
            try:
                markers = json.load(f)
            except json.JSONDecodeError:
                markers = []  # 文件为空或格式错误，初始化为空列表

        markers.append(marker)

        with open(MARKERS_FILE, 'w') as f:
            json.dump(markers, f, indent=2, ensure_ascii=False)

        return jsonify(marker), 201

    except Exception as e:
        app.logger.error(f"Error adding marker: {e}") # 记录错误日志
        return jsonify({'error': str(e)}), 500



@app.route('/api/markers/<marker_id>', methods=['PUT'])
def update_marker(marker_id):
    try:
        updated_marker = request.json

        with open(MARKERS_FILE, 'r') as f:
            markers = json.load(f)

        for i, marker in enumerate(markers):
            if marker.get('id') == marker_id:
                # 保留原有的图片列表
                if 'images' not in updated_marker:
                    updated_marker['images'] = marker.get('images', [])
                markers[i] = updated_marker
                break

        with open(MARKERS_FILE, 'w') as f:
            json.dump(markers, f, indent=2)

        return jsonify(updated_marker)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/markers/<marker_id>', methods=['DELETE'])
def delete_marker(marker_id):
    try:
        with open(MARKERS_FILE, 'r') as f:
            markers = json.load(f)

        # 找到要删除的标记
        marker_to_delete = None
        for marker in markers:
            if marker.get('id') == marker_id:
                marker_to_delete = marker
                break

        if marker_to_delete:
            # 删除与该标记相关的图片
            for image in marker_to_delete.get('images', []):
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image['filename']))
                except:
                    pass  # 如果删除失败，继续执行

            # 从列表中删除标记
            markers = [m for m in markers if m.get('id') != marker_id]

            with open(MARKERS_FILE, 'w') as f:
                json.dump(markers, f, indent=2)

            return jsonify({'success': True, 'id': marker_id})
        else:
            return jsonify({'error': 'Marker not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/markers/<marker_id>/images', methods=['POST'])
def upload_image(marker_id):
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # 生成唯一文件名以避免冲突
        filename = f"{int(time.time())}_{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # 更新标记数据
        with open(MARKERS_FILE, 'r') as f:
            markers = json.load(f)

        for marker in markers:
            if marker.get('id') == marker_id:
                if 'images' not in marker:
                    marker['images'] = []

                image_info = {
                    'id': str(uuid.uuid4()),
                    'filename': filename,
                    'originalName': file.filename,
                    'uploadTime': time.time()
                }
                marker['images'].append(image_info)

                with open(MARKERS_FILE, 'w') as f:
                    json.dump(markers, f, indent=2)

                return jsonify(image_info)

        return jsonify({'error': 'Marker not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/markers/<marker_id>/images/<image_id>', methods=['DELETE'])
def delete_image(marker_id, image_id):
    try:
        with open(MARKERS_FILE, 'r') as f:
            markers = json.load(f)

        for marker in markers:
            if marker.get('id') == marker_id and 'images' in marker:
                # 找到要删除的图片
                image_to_delete = None
                for image in marker['images']:
                    if image.get('id') == image_id:
                        image_to_delete = image
                        break

                if image_to_delete:
                    # 从文件系统删除图片
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_to_delete['filename']))
                    except:
                        pass  # 如果删除失败，继续执行

                    # 从列表中删除图片记录
                    marker['images'] = [img for img in marker['images'] if img.get('id') != image_id]

                    with open(MARKERS_FILE, 'w') as f:
                        json.dump(markers, f, indent=2)

                    return jsonify({'success': True, 'id': image_id})
                else:
                    return jsonify({'error': 'Image not found'}), 404

        return jsonify({'error': 'Marker not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

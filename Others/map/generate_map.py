import folium
import requests
import re

# 高德地图API Key
amap_api_key = '7fe0142b23646af138b5f5471ff9d06c'  # 替换为你的实际API Key

# 获取地理编码信息
def get_geocode(address, amap_api_key):
    url = f'https://restapi.amap.com/v3/geocode/geo?address={address}&key={amap_api_key}'
    response = requests.get(url)
    geocode = response.json()
    if geocode['status'] == '1' and len(geocode['geocodes']) > 0:
        location = geocode['geocodes'][0]['location']
        lon, lat = map(float, location.split(','))
        return lat, lon
    else:
        raise Exception('Failed to get geocode')

# 初始化地图
center_address = 'Chengdu'
center_lat, center_lon = get_geocode(center_address, amap_api_key)
map_ = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# 保存基础地图到HTML文件
map_file = 'interactive_map.html'
map_.save(map_file)

# 自定义的JavaScript代码
custom_js = f"""
<script>
document.addEventListener('DOMContentLoaded', function() {{
    console.log("文档已加载");

    // 初始化地图
    var map = L.map('map').setView([{center_lat}, {center_lon}], 12);

    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        maxZoom: 19
    }}).addTo(map);

    // 添加点击事件
    function addMarker(e) {{
        var newMarker = L.marker(e.latlng).addTo(map);
        newMarker.bindPopup(createPopupContent(e.latlng.lat, e.latlng.lng, "新标记", null));

        var markerData = {{
            lat: e.latlng.lat,
            lon: e.latlng.lng,
            description: "新标记",  // 默认描述信息
            image: null
        }};

        fetch('/add_marker', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify(markerData)
        }}).then(response => response.json())
        .then(data => {{
            if (data.success) {{
                console.log('标记已成功添加');
            }} else {{
                console.log('添加标记失败');
            }}
        }});
    }}

    // 创建弹出窗口内容
    function createPopupContent(lat, lon, description, image) {{
        return `
            <div>
                <textarea id="desc_${{lat}}_${{lon}}">${{description}}</textarea>
                <br/>
                <input type="file" id="img_${{lat}}_${{lon}}" accept="image/*" onchange="uploadImage(${{lat}}, ${{lon}})" data-image="${{image || ''}}"/>
                <br/>
                ${{image ? '<img src="' + image + '" style="max-width:100%;"/>' : ''}}
                <br/>
                <button onclick="deleteMarker(${{lat}}, ${{lon}})">删除</button>
                <button onclick="saveMarker(${{lat}}, ${{lon}})">保存</button>
            </div>
        `;
    }}

    // 获取现有的标记点
    fetch('/get_markers')
        .then(response => response.json())
        .then(data => {{
            data.forEach(marker => {{
                var newMarker = L.marker([marker.lat, marker.lon]).addTo(map);
                newMarker.bindPopup(createPopupContent(marker.lat, marker.lon, marker.description, marker.image));
            }});
        }});

    // 绑定点击事件
    map.on('click', addMarker);

    // 删除标记点
    window.deleteMarker = function(lat, lon) {{
        fetch('/delete_marker', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{ lat: lat, lon: lon }})
        }}).then(response => response.json())
        .then(data => {{
            if (data.success) {{
                alert('标记已成功删除');
                location.reload();  // 刷新页面以更新标记点
            }} else {{
                alert('删除标记失败');
            }}
        }});
    }};

    // 保存标记点
    window.saveMarker = function(lat, lon) {{
        var description = document.getElementById(`desc_${{lat}}_${{lon}}`).value;
        var fileInput = document.getElementById(`img_${{lat}}_${{lon}}`);
        var image = fileInput.dataset.image;

        fetch('/save_marker', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{ lat: lat, lon: lon, description: description, image: image }})
        }}).then(response => response.json())
        .then(data => {{
            if (data.success) {{
                alert('标记已成功保存');
                // 更新弹出窗口内容
                var marker = L.marker([lat, lon]).addTo(map);
                marker.bindPopup(createPopupContent(lat, lon, description, image)).openPopup();
            }} else {{
                alert('保存标记失败');
            }}
        }});
    }};

    // 上传图片
    window.uploadImage = function(lat, lon) {{
        var fileInput = document.getElementById(`img_${{lat}}_${{lon}}`);
        var formData = new FormData();
        formData.append('lat', lat);
        formData.append('lon', lon);
        formData.append('image', fileInput.files[0]);

        fetch('/upload_image', {{
            method: 'POST',
            body: formData
        }}).then(response => response.json())
        .then(data => {{
            if (data.success) {{
                alert('图片已成功上传');
                // 设置图片路径到 dataset
                fileInput.dataset.image = data.image;
                // 更新弹出窗口内容
                var marker = L.marker([lat, lon]).addTo(map);
                marker.bindPopup(createPopupContent(lat, lon, data.description, data.image)).openPopup();
            }} else {{
                alert('图片上传失败');
            }}
        }});
    }};
}});
</script>
"""

# 读取生成的HTML文件内容
with open(map_file, 'r', encoding='utf-8') as file:
    map_html = file.read()

# 动态查找和替换地图实例ID和变量名
map_html = re.sub(r'id="map_\w+"', 'id="map"', map_html)
map_html = re.sub(r'var map_\w+', 'var map', map_html)

# 在地图HTML中插入自定义的JavaScript代码
if '</body>' in map_html:
    map_html = map_html.replace('</body>', custom_js + '</body>')
else:
    map_html += custom_js

# 保存更新后的HTML文件
with open(map_file, 'w', encoding='utf-8') as file:
    file.write(map_html)

print("Interactive map has been saved to", map_file)

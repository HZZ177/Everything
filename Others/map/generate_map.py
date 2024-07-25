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
        console.log("Document is ready");

        // 初始化地图
        var map = L.map('map').setView([{center_lat}, {center_lon}], 12);

        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19
        }}).addTo(map);

        // 添加点击事件
        function addMarker(e) {{
            console.log("Map was clicked at ", e.latlng);
            var newMarker = L.marker(e.latlng).addTo(map);
            newMarker.bindPopup("You clicked the map at " + e.latlng.toString());

            var markerData = {{
                lat: e.latlng.lat,
                lon: e.latlng.lng
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
                    console.log('Marker added successfully');
                }} else {{
                    console.log('Failed to add marker');
                }}
            }});
        }}

        // 获取现有的标记点
        fetch('/get_markers')
            .then(response => response.json())
            .then(data => {{
                console.log("Markers loaded: ", data);
                data.forEach(marker => {{
                    var newMarker = L.marker([marker.lat, marker.lon]).addTo(map);
                    newMarker.bindPopup("Stored marker at " + marker.lat + ", " + marker.lon);
                }});
            }});

        // 绑定点击事件
        map.on('click', addMarker);
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
map_html = map_html.replace('</body>', custom_js + '</body>')

# 保存更新后的HTML文件
with open(map_file, 'w', encoding='utf-8') as file:
    file.write(map_html)

print("Interactive map has been saved to", map_file)

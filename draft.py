import math
import json


# 步骤1：找到夹角小于140度的折点
def find_acute_angles(points):
    def angle_between(v1, v2):
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
        magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)
        if magnitude_v1 == 0 or magnitude_v2 == 0:
            return 0
        cos_theta = dot_product / (magnitude_v1 * magnitude_v2)
        angle = math.acos(cos_theta)
        return math.degrees(angle)

    acute_points = []
    for i in range(1, len(points) - 1):
        v1 = (points[i][0] - points[i - 1][0], points[i][1] - points[i - 1][1])
        v2 = (points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1])
        angle = angle_between(v1, v2)
        if angle < 100:
            acute_points.append(i)
    return acute_points


# 步骤2：将折线A分成多段折线，并过滤掉长度为1的线段
def split_line_at_points(points, split_indices):
    split_lines = []
    prev_index = 0
    for index in split_indices:
        if index + 1 > prev_index:
            split_lines.append(points[prev_index:index + 1])
        prev_index = index
    if prev_index < len(points):
        split_lines.append(points[prev_index:])
    return [line for line in split_lines if len(line) > 1]


# 步骤3：根据折点数比例将m分成多份
def distribute_points_among_lines(split_lines, total_points):
    # 计算每段折线的真实长度
    def line_length(line):
        return sum(math.sqrt((line[i + 1][0] - line[i][0]) ** 2 + (line[i + 1][1] - line[i][1]) ** 2) for i in
                   range(len(line) - 1))

    lengths = [line_length(line) for line in split_lines]
    total_length = sum(lengths)

    # 分配点数
    points_distribution = []
    remaining_points = total_points

    for length in lengths[:-1]:
        points_for_line = round(total_points * (length / total_length))
        points_distribution.append(points_for_line)
        remaining_points -= points_for_line

    points_distribution.append(remaining_points)
    return points_distribution


# 步骤4：在每段折线上生成等距的点并计算垂点坐标
def generate_points_on_line(line, num_points):
    if num_points == 0:
        return []

    generated_points = []
    total_length = sum(math.sqrt((line[i + 1][0] - line[i][0]) ** 2 + (line[i + 1][1] - line[i][1]) ** 2) for i in
                       range(len(line) - 1))
    segment_length = total_length / (num_points + 1)

    current_length = 0
    for i in range(len(line) - 1):
        segment = (line[i], line[i + 1])
        segment_vector = (segment[1][0] - segment[0][0], segment[1][1] - segment[0][1])
        segment_magnitude = math.sqrt(segment_vector[0] ** 2 + segment_vector[1] ** 2)

        while current_length + segment_magnitude >= segment_length:
            ratio = (segment_length - current_length) / segment_magnitude
            new_point = (segment[0][0] + ratio * segment_vector[0], segment[0][1] + ratio * segment_vector[1])
            generated_points.append(new_point)
            current_length = 0
            segment = (new_point, segment[1])
            segment_vector = (segment[1][0] - segment[0][0], segment[1][1] - segment[0][1])
            segment_magnitude = math.sqrt(segment_vector[0] ** 2 + segment_vector[1] ** 2)

        current_length += segment_magnitude

    return generated_points


# 步骤5：输出所有点并存储为GeoJSON格式的文件
def create_geojson(points):
    features = []
    for point in points:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": point
            },
            "properties": {}
        })
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson


# 示例点坐标
points = [
    (104.029245, 30.649609),
    (104.029371, 30.649544),
    (104.029852, 30.649262),
    (104.030065, 30.649154),
    (104.030065, 30.649154),
    (104.030113, 30.649132),
    (104.030143, 30.649128),
    (104.030234, 30.649123),
    (104.030369, 30.649123),
    (104.03072, 30.649132),
    (104.03072, 30.649132),
    (104.031415, 30.649141),
    (104.031415, 30.649141),
    (104.031684, 30.649136),
    (104.031684, 30.649136),
    (104.032118, 30.649141),
    (104.032118, 30.649141),
    (104.032157, 30.649141),
    (104.032157, 30.649141),
    (104.032405, 30.649145)
]

m = 50  # 总点数

# 运行所有步骤
try:
    acute_points = find_acute_angles(points)
    print("Acute points:", acute_points)

    split_lines = split_line_at_points(points, acute_points)
    print("Split lines:", split_lines)

    points_distribution = distribute_points_among_lines(split_lines, m)
    print("Points distribution:", points_distribution)

    generated_points = []
    for i, line in enumerate(split_lines):
        generated_points.extend(generate_points_on_line(line, points_distribution[i]))

    print("Generated points:", generated_points)

#    geojson = create_geojson(generated_points)

# 保存为GeoJSON文件
#     with open("generated_points.geojson", "w") as f:
#     json.dump(geojson, f, indent=4)

#    print("GeoJSON文件已生成：generated_points.geojson")
except Exception as e:
    print("Error:", e)

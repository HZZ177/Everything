import requests


def create_road_and_park():
    url_add_road = "http://roadtest.keytop.cn:30031/web/parking/road/add"
    url_get_road_id = "http://roadtest.keytop.cn:30031/web/parking/road/getRoadList"
    url_batch_insert_park = "http://roadtest.keytop.cn:30031/web/parking/parkspace/batchAdd"

    for i in range(100):
        payload_add_road = {
            "id": "",
            "parkCode":
                "LC5110000001",
            "roadName": f"{basic_road_name}_{i + 1}",
            "longitude": "",
            "latitude": ""
        }

        payload_get_road_id = {
            "parkCode": "LC5110000001"
        }

        payload_batch_insert_park = {
            "parkCode": "LC5110000001",
            "roadCode": "",
            "parkspaceType": 1,
            "parkspaceStartCode": "1",
            "batchAddNum": 100
        }

        # 新增路段
        response_add_road = requests.post(url_add_road, headers=headers, json=payload_add_road)
        if response_add_road.status_code != 200:
            print(f"第{i + 1}个路段新增失败：{response_add_road.text}")
            continue
        else:
            print(f"第{i + 1}个路段新增成功：{response_add_road.text}，查询路段id")
            # 查询路段id
            response_get_road_id = requests.post(url_get_road_id, headers=headers, json=payload_get_road_id)

            if response_get_road_id.status_code != 200:
                print(f"查询路段id失败：{response_get_road_id.text}")
                continue
            else:
                print(f"查询路段id成功：{response_get_road_id.text}，开始批量新增车位")
                for n in response_get_road_id.json()["data"]:
                    if n["roadName"] == f"{basic_road_name}_{i + 1}":
                        payload_batch_insert_park["roadCode"] = n["roadCode"]
                        break
                # 批量新增车位
                response_batch_insert_park = requests.post(url_batch_insert_park, headers=headers,
                                                           json=payload_batch_insert_park)
                if response_batch_insert_park.status_code != 200:
                    print(f"批量新增车位失败：{response_batch_insert_park.text}")
                else:
                    print(f"批量新增车位成功：{response_batch_insert_park.text}")


def delete_road():
    url_query = "http://roadtest.keytop.cn:30031/web/parking/road/page"
    # 先查询第一页的数据，获取总页数
    payload = {
        "current": 1,
        "parkCode": "LC5110000001",
        "size": 10
    }
    response = requests.post(url_query, headers=headers, json=payload)
    total_page = response.json()["data"]["size"]
    print(f"共有{total_page}页数据")

    # 遍历每一页，收集需要删除的路段，以basic_road_name为标识收集待删除路段
    road_to_delete = {}
    for i in range(1, total_page + 1):
        print(f"正在查询第{i}页数据")
        payload["current"] = i
        response = requests.post(url_query, headers=headers, json=payload)
        for n in response.json()["data"]["records"]:
            if n["roadName"].startswith(basic_road_name):
                print(f"收集待删除路段：{n['roadName']}")
                road_to_delete[n["roadName"]] = n["id"]
            else:
                print(f"跳过非待删除路段：{n['roadName']}")
    print(f"待删除路段：{road_to_delete}")

    # 开始删除路段
    for road_name, road_id in road_to_delete.items():
        url_delete = "http://roadtest.keytop.cn:30031/web/parking/road/disable"
        payload = {
            "id": road_id
        }
        response = requests.post(url_delete, headers=headers, json=payload)
        # print(f"删除路段{road_name}:{road_id}")
        if response.json()["code"] != 200:
            print(f"删除路段{road_name}失败：{response.text}")
        else:
            print(f"删除路段{road_name}成功：{response.text}")


if __name__ == "__main__":
    headers = {
        "authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiI2Zjk3MGJlMTg4MDI0MDY1ODgyZjk1ZmYzNjVkMGQxOCIsImF1dGg"
                         "iOiIiLCJzdWIiOiIxODIyNzYzOTIyOSJ9.G-tkwbJ6Z19C_epTllUm04EDNK7ZbqTAoOhfKcExcifW_scOLrSJClpXu"
                         "cPLui9u-XlegciFTqPp9OBvwE-LiQ_higha622d47a8c9a4a818dac00f840e59f37",
        "operatorname": "%E4%BD%95%E5%AE%88%E4%B8%80",
        "code": "a622d47a8c9a4a818dac00f840e59f37",
        "parkcode": "LC5110000001"
    }

    basic_road_name = "守一の超大量路段"

    # 批量创建路段和车位
    # create_road_and_park()
    # 批量删除路段
    delete_road()

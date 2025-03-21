import requests

url_add_road = "http://roadtest.keytop.cn:30031/web/parking/road/add"
url_get_road_id = "http://roadtest.keytop.cn:30031/web/parking/road/getRoadList"
url_batch_insert_park = "http://roadtest.keytop.cn:30031/web/parking/parkspace/batchAdd"

headers = {
    "authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJiNGM5YTY3ZWZmYzM0ZTdmYWNhMGVmOGNiZTc0ZTNjYyIsImF1dGgiOiIiLCJzdWIiOiIxODIyNzYzOTIyOSJ9.ZPGihbr6MuNjiO1BFBNaWLlPAf4PzNyTbSmDBRu4UXYp2ateYS2gRhiDsupEegmr0Rhx_K-jB573Ss7Dhdeiyw_higha8630339fc0a48e3a03a4f26197d52cf",
    "operatorname": "%E4%BD%95%E5%AE%88%E4%B8%80",
    "code": "a8630339fc0a48e3a03a4f26197d52cf"
}


def main():
    for i in range(100):
        road_name = "守一の超大量路段"
        payload_add_road = {
            "id": "",
            "parkCode":
                "LC5110000001",
            "roadName": f"{road_name}_{i + 1}",
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
                    if n["roadName"] == f"{road_name}_{i + 1}":
                        payload_batch_insert_park["roadCode"] = n["roadCode"]
                        break
                # 批量新增车位
                response_batch_insert_park = requests.post(url_batch_insert_park, headers=headers,
                                                           json=payload_batch_insert_park)
                if response_batch_insert_park.status_code != 200:
                    print(f"批量新增车位失败：{response_batch_insert_park.text}")
                else:
                    print(f"批量新增车位成功：{response_batch_insert_park.text}")


if __name__ == "__main__":
    main()

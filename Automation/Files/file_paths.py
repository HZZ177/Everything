import os

"""环境地址"""
environment250_page = "http://192.168.25.250:8083/web/login"
environment249_page = "http://192.168.25.249:8083/web/login"
environment229_page = "http://117.173.153.92:57108/web/login"   # 公网地址

"""登录地址"""
environment250_login = "http://192.168.25.250:8083/auth/login"
environment249_login = "http://192.168.25.249:8083/auth/login"
environment229_login = "http://119.3.77.222:35001/auth/login"  # 公网地址

"""一级目录"""  # 项目一级文件夹目录
project_path = os.path.dirname(os.path.realpath(__file__))  # 当前文件夹目录（Files）

"""二级目录"""
verify_picture_path = os.path.join(project_path, "verifycode.png")  # 保存验证码图片目录


"""接口目录"""
route = {
    "get_all_screen_address": "screen/getAllTcpAddr",
    "car_in": "park/enter",
    "update_plate_no": "park/updatePlateNo",
    "car_leave": "/park/leave",
    "floor_insert": "floorInfo/insert",
    "floor_update": "floorInfo/update"
}


if __name__ == "__main__":
    print(verify_picture_path)

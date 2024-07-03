import requests

#############################


def area_areadeviceupdatestatus(addr: int, reqid: str, status: int):
    """
    区域相机更新拥堵状态
    :param int addr: 区域相机地址
    :param str reqid: 请求唯一id，用于追踪请求
    :param int status: 区域相机拥堵状态（0 不拥堵   1 拥堵）
    """
    url = 'http://119.3.77.222:35022' + '/area/areaDeviceUpdateStatus'
    params = {
        'addr': addr,
        'reqid': reqid,
        'status': status,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def area_enter(list: list, reqid: str):
    """
    (弃用)区域入车
    :param list list: 进出车参数
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/area/enter'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def area_leave(list: list, reqid: str):
    """
    (弃用)区域出车
    :param list list: 进出车参数
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/area/leave'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def area_updatestereoscopicdetectorparkaddrlist():
    """
    更新立体区域关联探测器地址服务内存数据
    
    """
    url = 'http://119.3.77.222:35022' + '/area/updateStereoscopicDetectorParkAddrList'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def areacamera_areainout(eventid: str, plateno: str, platereliability: int, regionip: str, triggerflag: int):
    """
    区域相机进出车
    :param str eventid: 事件ID --对应图片事件Id
    :param str plateno: 车牌
    :param int platereliability: 可信度
    :param str regionip: 相机ip
    :param int triggerflag: 触发事件：3=来车 2=去车；
    """
    url = 'http://119.3.77.222:35022' + '/areaCamera/areaInOut'
    params = {
        'eventid': eventid,
        'plateno': plateno,
        'platereliability': platereliability,
        'regionip': regionip,
        'triggerflag': triggerflag,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def areacamera_areapostpicture(carimageurl: str, eventid: str, regionip: str):
    """
    区域相机更新图片
    :param str carimageurl: 图片路径
    :param str eventid: 事件ID
    :param str regionip: 区域相机ip
    """
    url = 'http://119.3.77.222:35022' + '/areaCamera/areaPostPicture'
    params = {
        'carimageurl': carimageurl,
        'eventid': eventid,
        'regionip': regionip,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def carinout_listinoutcarinfo(intimeend: str, intimestart: str, pageindex: int, pagesize: int, plateno: str, spaceno: str):
    """
    历史进出车明细分页查询
    :param str intimeend: 查询入车结束时间（必填，时间跨度最长30天）
    :param str intimestart: 查询入车开始时间（必填，时间跨度最长30天）
    :param int pageindex: 页数
    :param int pagesize: 每页条目数
    :param str plateno: 车牌号
    :param str spaceno: 车位号
    """
    url = 'http://119.3.77.222:35022' + '/carInOut/listInOutCarInfo'
    params = {
        'intimeend': intimeend,
        'intimestart': intimestart,
        'pageindex': pageindex,
        'pagesize': pagesize,
        'plateno': plateno,
        'spaceno': spaceno,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def charge_postcaroutinfo(plateno: str):
    """
    出场上报
    :param str plateno: 车牌号
    """
    url = 'http://119.3.77.222:35022' + '/charge/postCarOutInfo'
    params = {
        'plateno': plateno,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def deviceescalation_getinfo(areaname: str, deviceip: str, deviceport: int, floorname: str, parkno: str):
    """
    查询车位编号对应地址信息
    :param str areaname: 区域名称
    :param str deviceip: 上报设备IP
    :param int deviceport: 上报设备端口
    :param str floorname: 楼层名称
    :param str parkno: 车位编号
    """
    url = 'http://119.3.77.222:35022' + '/deviceEscalation/getInfo'
    params = {
        'areaname': areaname,
        'deviceip': deviceip,
        'deviceport': deviceport,
        'floorname': floorname,
        'parkno': parkno,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def deviceescalation_saveinfo(areaname: str, deviceip: str, deviceport: int, floorname: str, parkno: str):
    """
    保存相机对应车位信息
    :param str areaname: 区域名称
    :param str deviceip: 上报设备IP
    :param int deviceport: 上报设备端口
    :param str floorname: 楼层名称
    :param str parkno: 车位编号
    """
    url = 'http://119.3.77.222:35022' + '/deviceEscalation/saveInfo'
    params = {
        'areaname': areaname,
        'deviceip': deviceip,
        'deviceport': deviceport,
        'floorname': floorname,
        'parkno': parkno,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def emergencymode_off():
    """
    关闭紧急模式
    
    """
    url = 'http://119.3.77.222:35022' + '/emergencyMode/off'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def emergencymode_on():
    """
    打开紧急模式
    
    """
    url = 'http://119.3.77.222:35022' + '/emergencyMode/on'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def healthcheck():
    """
    healthCheck
    
    """
    url = 'http://119.3.77.222:35022' + '/healthCheck'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def inichange_pushconfig(comname: str, dsprecog: int, firstserverip: str, picswitch: int, province: str, ret: int, witch: int):
    """
    下发配置信息到C++
    :param str comname: 连接服务器的端口号 windows下是COM5, linux下是/dev/ttyS0
    :param int dsprecog: 控制软识别与硬识别 0 软识别, 1 硬识别
    :param str firstserverip: 设备IP前缀
    :param int picswitch: 是否开启空车牌图片收集功能  1 开启,  0 关闭
    :param str province: 车牌的默认省份(省份简称汉字) 默认为空
    :param int ret: 控制TCP还是485通讯 0 tcp, 1 485
    :param int witch: 控制故障状态的设备的开关 0 关闭， 1 开启
    """
    url = 'http://119.3.77.222:35022' + '/iniChange/pushConfig'
    params = {
        'comname': comname,
        'dsprecog': dsprecog,
        'firstserverip': firstserverip,
        'picswitch': picswitch,
        'province': province,
        'ret': ret,
        'witch': witch,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def ledscreen_notice(reqid: str, screenidlist: list):
    """
    传入子屏id集合，触发这些子屏统计屏关联车位，并下发屏指令
    :param str reqid: 请求id
    :param list screenidlist: 子屏id集合
    """
    url = 'http://119.3.77.222:35022' + '/ledScreen/notice'
    params = {
        'reqid': reqid,
        'screenidlist': screenidlist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def ledscreen_noticetest(reqid: str, screenidlist: list):
    """
    传入子屏id集合，进行屏测试操作，并下发屏指令
    :param str reqid: 请求id
    :param list screenidlist: 子屏id集合
    """
    url = 'http://119.3.77.222:35022' + '/ledScreen/noticeTest'
    params = {
        'reqid': reqid,
        'screenidlist': screenidlist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def ledscreen_updatescreencmd(reqid: str, screenidlist: list):
    """
    第三方屏控制接口
    :param str reqid: 请求id
    :param list screenidlist: 子屏id集合
    """
    url = 'http://119.3.77.222:35022' + '/ledScreen/updateScreenCmd'
    params = {
        'reqid': reqid,
        'screenidlist': screenidlist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def nodedevice_initstatusbatch():
    """
    初始化节点设备状态为离线
    
    """
    url = 'http://119.3.77.222:35022' + '/nodeDevice/initStatusBatch'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def nodedevice_select485andipcamlist():
    """
    查询485节点和相机设备信息
    
    """
    url = 'http://119.3.77.222:35022' + '/nodeDevice/select485AndIpCamList'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def nodedevice_selectalllist():
    """
    查询所有节点设备地址
    
    """
    url = 'http://119.3.77.222:35022' + '/nodeDevice/selectAllList'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def nodedevice_selectinterandipcamlist():
    """
    查询网络节点和相机节点设备信息
    
    """
    url = 'http://119.3.77.222:35022' + '/nodeDevice/selectInterAndIpCamList'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def nodedevice_updatestatusbatchbyaddr(addrstr: str, status: int):
    """
    批量更新节点设备状态
    :param str addrstr: 节点地址（,分割）
    :param int status: 节点设备状态(0 离线  1 在线)
    """
    url = 'http://119.3.77.222:35022' + '/nodeDevice/updateStatusBatchByAddr'
    params = {
        'addrstr': addrstr,
        'status': status,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_clearcaptureurl(parkaddr: int):
    """
    清除内存中车位对应抓拍信息
    :param int parkaddr: parkAddr
    """
    url = 'http://119.3.77.222:35022' + '/park/clearCaptureUrl'
    params = {
        'parkaddr': parkaddr,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_enter(list: list, reqid: str):
    """
    车位入车
    :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/park/enter'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_faultforfindcar(list: list, reqid: str):
    """
    故障(找车系统)
    :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/park/faultForFindCar'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_faultforguidance(list: list, reqid: str):
    """
    故障(引导系统)
    :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/park/faultForGuidance'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_freeforfindcar(list: list, reqid: str):
    """
    无车(找车系统)
    :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/park/freeForFindCar'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_freeforguidance(list: list, reqid: str):
    """
    无车(引导系统)
    :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/park/freeForGuidance'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_getcaptureurl(parkaddr: int):
    """
    获取内存中车位对应抓拍信息
    :param int parkaddr: parkAddr
    """
    url = 'http://119.3.77.222:35022' + '/park/getCaptureUrl'
    params = {
        'parkaddr': parkaddr,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_getemptycount(reqid: str):
    """
    获取空车位数量
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/park/getEmptyCount'
    params = {
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_leave(list: list, reqid: str):
    """
    车位出车
    :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/park/leave'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_occupyforfindcar(list: list, reqid: str):
    """
    有车(找车系统)
    :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/park/occupyForFindCar'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_occupyforguidance(list: list, reqid: str):
    """
    有车(引导系统)
    :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/park/occupyForGuidance'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_pushparkcamera(parkingip: str, parkingport: int):
    """
    下发C++相机抓拍指令
    :param str parkingip: parkingIp
    :param int parkingport: parkingPort
    """
    url = 'http://119.3.77.222:35022' + '/park/pushParkCamera'
    params = {
        'parkingip': parkingip,
        'parkingport': parkingport,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_selectparklistbycondition(parkaddr: int, reqid: str, status: int):
    """
    根据条件查询车位信息
    :param int parkaddr: 车位地址
    :param str reqid: 请求唯一id，用于追踪请求
    :param int status: 车位状态  0：空闲  1：占用  2：故障  3：停止服务
    """
    url = 'http://119.3.77.222:35022' + '/park/selectParkListByCondition'
    params = {
        'parkaddr': parkaddr,
        'reqid': reqid,
        'status': status,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_snapallbylot():
    """
    全场车位相机抓拍指令
    
    """
    url = 'http://119.3.77.222:35022' + '/park/snapAllByLot'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_test(addr: str):
    """
    test
    :param str addr: addr
    """
    url = 'http://119.3.77.222:35022' + '/park/test'
    params = {
        'addr': addr,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_test2():
    """
    test2
    
    """
    url = 'http://119.3.77.222:35022' + '/park/test2'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_updateallfault(reqid: str):
    """
    更新所有车位为故障
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/park/updateAllFault'
    params = {
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_updatecaptureurl(parkaddr: str, parkingcaptureurl: str):
    """
    更新车位相机抓拍照片路径
    :param str parkaddr: 车位地址(此处为不含后两位相机通道端口的车位地址)
    :param str parkingcaptureurl: 抓拍照片路径
    """
    url = 'http://119.3.77.222:35022' + '/park/updateCaptureUrl'
    params = {
        'parkaddr': parkaddr,
        'parkingcaptureurl': parkingcaptureurl,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_updateplateno(list: list, reqid: str):
    """
    更新车牌
    :param list list: 更新参数
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/park/updatePlateNo'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def parkinglight_notice(freecolor: int, lighttype: int, lotid: int, noticetype: int, occupycolor: int, parkaddr: int, parkinglightarearelationlist: list, reqid: str, type: int, warningcolor: int):
    """
    方案推送
    :param int freecolor: 空闲颜色
    :param int lighttype: 灯类型  1-有线多彩灯  2-有线双色灯
    :param int lotid: 车场id
    :param int noticetype: 通知类型 0-按车位地址 1-按区域
    :param int occupycolor: 占用颜色
    :param int parkaddr: 车位地址
    :param list parkinglightarearelationlist: 车位灯方案和区域的关系列表
    :param str reqid: 请求id
    :param int type: 设备类型  0-DSP车位相机   1-NODE节点控制器
    :param int warningcolor: 告警颜色
    """
    url = 'http://119.3.77.222:35022' + '/parking-light/notice'
    params = {
        'freecolor': freecolor,
        'lighttype': lighttype,
        'lotid': lotid,
        'noticetype': noticetype,
        'occupycolor': occupycolor,
        'parkaddr': parkaddr,
        'parkinglightarearelationlist': parkinglightarearelationlist,
        'reqid': reqid,
        'type': type,
        'warningcolor': warningcolor,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def parkinglight_noticeforstopwarn(reqid: str, screenidlist: list):
    """
    用于终止违停告警的下发灯指令方法
    :param str reqid: 请求id
    :param list screenidlist: 子屏id集合
    """
    url = 'http://119.3.77.222:35022' + '/parking-light/noticeForStopWarn'
    params = {
        'reqid': reqid,
        'screenidlist': screenidlist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def parkmall_carend(platenumber: str):
    """
    车辆出场上报
    :param str platenumber: 车牌号
    """
    url = 'http://119.3.77.222:35022' + '/parkmall/carEnd'
    params = {
        'platenumber': platenumber,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def screen_getalltcpaddr(reqid: str):
    """
    获取所有网络屏的子屏地址
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/screen/getAllTcpAddr'
    params = {
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def screen_getlcdscreendata(ip: str, type: int):
    """
    获取LCD屏下发数据
    :param str ip: 屏ip
    :param int type: 屏类型
    """
    url = 'http://119.3.77.222:35022' + '/screen/getLcdScreenData'
    params = {
        'ip': ip,
        'type': type,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def screen_initalloffline(reqid: str):
    """
    把所有屏初始化为离线
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/screen/initAllOffLine'
    params = {
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def screen_ledpagerefresh(reqid: str, screenidlist: list):
    """
    LED屏页面刷新
    :param str reqid: No description
    :param list screenidlist: No description
    """
    url = 'http://119.3.77.222:35022' + '/screen/ledPageRefresh'
    params = {
        'reqid': reqid,
        'screenidlist': screenidlist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def screen_sendlcdscreendata(cmd: str, data: str, ip: str, reqid: str, scene: int, showtemplate: int, ts: int, type: int):
    """
    指令下发LCD屏数据
    :param str cmd: pageUpdate页面更新;dataUpdate数据更新;temporaryPush临时推送;scriptExecution脚本执行;
    :param str data: 数据体
    :param str ip: lcd屏ip
    :param str reqid: 请求ID(不传入时，系统内部会随机生成默认值)
    :param int scene: 场景:1标准引导;999非标页面,默认：1标准引导
    :param int showtemplate: 展示模板  0=非标模板 1=模板一
    :param int ts: 时间戳(不传入时，系统内部会根据当前时间生成默认值)
    :param int type: 屏标识(0:一体屏,1:双拼接屏左屏,2:双拼接屏右屏)
    """
    url = 'http://119.3.77.222:35022' + '/screen/sendLcdScreenData'
    params = {
        'cmd': cmd,
        'data': data,
        'ip': ip,
        'reqid': reqid,
        'scene': scene,
        'showtemplate': showtemplate,
        'ts': ts,
        'type': type,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def screen_sendlcdscreendefaultdata(ip: str, type: int):
    """
    下发LCD屏默认(数据库)数据
    :param str ip: 屏ip
    :param int type: 屏类型
    """
    url = 'http://119.3.77.222:35022' + '/screen/sendLcdScreenDefaultData'
    params = {
        'ip': ip,
        'type': type,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def screen_updatestatusbyaddr(addr: int, reqid: str, status: int):
    """
    更新指定的屏为指定状态
    :param int addr: 子屏地址
    :param str reqid: 请求唯一id，用于追踪请求
    :param int status: 状态  1：在线  2：离线
    """
    url = 'http://119.3.77.222:35022' + '/screen/updateStatusByAddr'
    params = {
        'addr': addr,
        'reqid': reqid,
        'status': status,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def screenrelated_listlcdscreen(iplist: list, pageindex: int, pagesize: int):
    """
    LCD屏设备列表查询
    :param list iplist: 屏ip集合
    :param int pageindex: 页数
    :param int pagesize: 每页条目数
    """
    url = 'http://119.3.77.222:35022' + '/screenRelated/listLcdScreen'
    params = {
        'iplist': iplist,
        'pageindex': pageindex,
        'pagesize': pagesize,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def taskmanage_resetall():
    """
    重新加载所有系统定时任务
    
    """
    url = 'http://119.3.77.222:35022' + '/taskManage/resetAll'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_controlhightask(flag: int):
    """
    控制高负载任务(告警 进出车触发屏统计 有车无车上报) 1=开启 0=关闭
    :param int flag: flag
    """
    url = 'http://119.3.77.222:35022' + '/tool/controlHighTask'
    params = {
        'flag': flag,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_dealwithgrpccmd(areaid: int, areaname: str, beginareaname: str, beginfloorname: str, beginspaceno: str, cmd: str, endareaname: str, endfloorname: str, endspaceno: str, floorid: int, floorname: str, imgname: str, intimeend: str, intimestart: str, ip: str, iplist: list, isbind: int, lcdcmddata: str, lighttype: int, nodedeviceaddr: str, operatetype: int, pageindex: int, pagesize: int, parkschmeparam: list, parkupdateparam: list, parkupdatestatusdtolist: list, plateno: str, reqid: str, spaceno: str, systemtype: int, testingbatchid: str, warntype: int):
    """
    grpc的指令处理
    :param int areaid: 区域Id
    :param str areaname: 区域名称
    :param str beginareaname: 起点区域名称
    :param str beginfloorname: 起点楼层名称
    :param str beginspaceno: 开始车位号
    :param str cmd: 指令
    :param str endareaname: 终点区域名称
    :param str endfloorname: 终点楼层名称
    :param str endspaceno: 终点车位号
    :param int floorid: 楼层id
    :param str floorname: 楼层名称
    :param str imgname: 图片名称
    :param str intimeend: 查询入车结束时间（必填，时间跨度最长30天）
    :param str intimestart: 查询入车开始时间（必填，时间跨度最长30天）
    :param str ip: IP
    :param list iplist: 屏ip集合
    :param int isbind: 是否绑定
    :param str lcdcmddata: 指令数据
    :param int lighttype: 灯类型 1-有线多彩灯 2-有线双色灯
    :param str nodedeviceaddr: 节点设备地址
    :param int operatetype: 操作类型 0-停止 1-开始
    :param int pageindex: 页数
    :param int pagesize: 每页条目数
    :param list parkschmeparam: 根据车位编号修改车位灯方案
    :param list parkupdateparam: 根据车位编号修改车位类型参数
    :param list parkupdatestatusdtolist: 根据车位编号修改车位状态
    :param str plateno: 车牌号
    :param str reqid: 请求唯一id
    :param str spaceno: 车位编号
    :param int systemtype: 设备类型  0-DSP车位相机   1-NODE节点控制器
    :param str testingbatchid: 质检中心检测批次ID
    :param int warntype: 告警类型  1：车位占用告警   2：车辆违停告警  3：特殊车辆入车  4：特殊车辆出车  5：车辆压线 6：油车违停
    """
    url = 'http://119.3.77.222:35022' + '/tool/dealWithGrpcCmd'
    params = {
        'areaid': areaid,
        'areaname': areaname,
        'beginareaname': beginareaname,
        'beginfloorname': beginfloorname,
        'beginspaceno': beginspaceno,
        'cmd': cmd,
        'endareaname': endareaname,
        'endfloorname': endfloorname,
        'endspaceno': endspaceno,
        'floorid': floorid,
        'floorname': floorname,
        'imgname': imgname,
        'intimeend': intimeend,
        'intimestart': intimestart,
        'ip': ip,
        'iplist': iplist,
        'isbind': isbind,
        'lcdcmddata': lcdcmddata,
        'lighttype': lighttype,
        'nodedeviceaddr': nodedeviceaddr,
        'operatetype': operatetype,
        'pageindex': pageindex,
        'pagesize': pagesize,
        'parkschmeparam': parkschmeparam,
        'parkupdateparam': parkupdateparam,
        'parkupdatestatusdtolist': parkupdatestatusdtolist,
        'plateno': plateno,
        'reqid': reqid,
        'spaceno': spaceno,
        'systemtype': systemtype,
        'testingbatchid': testingbatchid,
        'warntype': warntype,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def tool_sendcommandtoallscreen():
    """
    统计所有的屏数据，并下发指令
    
    """
    url = 'http://119.3.77.222:35022' + '/tool/sendCommandToAllScreen'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_sendlightcommandtofindcar(cmd: str, lighttype: int, list: list, reqid: str):
    """
    给找车系统发送灯指令
    :param str cmd: No description
    :param int lighttype: No description
    :param list list: No description
    :param str reqid: No description
    """
    url = 'http://119.3.77.222:35022' + '/tool/sendLightCommandToFindCar'
    params = {
        'cmd': cmd,
        'lighttype': lighttype,
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def tool_sendlightcommandtoguidance(cmd: str, lighttype: int, list: list, reqid: str):
    """
    给引导系统发送灯指令
    :param str cmd: No description
    :param int lighttype: No description
    :param list list: No description
    :param str reqid: No description
    """
    url = 'http://119.3.77.222:35022' + '/tool/sendLightCommandToGuidance'
    params = {
        'cmd': cmd,
        'lighttype': lighttype,
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def tool_snap():
    """
    质检 - 抓拍
    
    """
    url = 'http://119.3.77.222:35022' + '/tool/snap'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_uniteapipro(appid: str, appsecret: str, params: dict, parkid: str, servicecode: str, uri: str, version: str):
    """
    测试统一接口（正式环境）
    :param str appid: No description
    :param str appsecret: No description
    :param dict params: 接口的额外参数 用json字符串传入
    :param str parkid: No description
    :param str servicecode: No description
    :param str uri: 接口uri
    :param str version: 请求头里的version 一般为1.0.0
    """
    url = 'http://119.3.77.222:35022' + '/tool/uniteApiPro'
    params = {
        'appid': appid,
        'appsecret': appsecret,
        'params': params,
        'parkid': parkid,
        'servicecode': servicecode,
        'uri': uri,
        'version': version,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def tool_uniteapitest(appid: str, appsecret: str, params: dict, parkid: str, servicecode: str, uri: str, version: str):
    """
    测试统一接口（测试环境）
    :param str appid: No description
    :param str appsecret: No description
    :param dict params: 接口的额外参数 用json字符串传入
    :param str parkid: No description
    :param str servicecode: No description
    :param str uri: 接口uri
    :param str version: 请求头里的version 一般为1.0.0
    """
    url = 'http://119.3.77.222:35022' + '/tool/uniteApiTest'
    params = {
        'appid': appid,
        'appsecret': appsecret,
        'params': params,
        'parkid': parkid,
        'servicecode': servicecode,
        'uri': uri,
        'version': version,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def tool_uploadimg(url: str):
    """
    场端图片统一上云
    :param str url: url
    """
    url = 'http://119.3.77.222:35022' + '/tool/uploadImg'
    params = {
        'url': url,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def unified_getcarlocinfo(pageindex: int, pagesize: int, plateno: str):
    """
    车辆停放位置查询接口(精准)
    :param int pageindex: 页数
    :param int pagesize: 每页条目数
    :param str plateno: 车牌号码
    """
    url = 'http://119.3.77.222:35022' + '/unified/getCarLocInfo'
    params = {
        'pageindex': pageindex,
        'pagesize': pagesize,
        'plateno': plateno,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def unified_getparklistbyplateno(pageindex: int, pagesize: int, plateno: str):
    """
    车辆停放位置查询接口(模糊)
    :param int pageindex: 页数
    :param int pagesize: 每页条目数
    :param str plateno: 车牌号（必填，不限制位数，支持带汉字和不带汉字）
    """
    url = 'http://119.3.77.222:35022' + '/unified/getParkListByPlateNo'
    params = {
        'pageindex': pageindex,
        'pagesize': pagesize,
        'plateno': plateno,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def warnlog_generatecrossline(list: list, reqid: str):
    """
    生成压线记录
    :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/warnLog/generateCrossLine'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def warnlog_stopcrossline(list: list, reqid: str):
    """
    停止压线告警
    :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    """
    url = 'http://119.3.77.222:35022' + '/warnLog/stopCrossLine'
    params = {
        'list': list,
        'reqid': reqid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()



import requests


class ChannelAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def area_areadeviceupdatestatus(self, access_token: str, addr: int = '', reqid: str = '', status: int = ''):
        """
        区域相机更新拥堵状态
        :param int addr: 区域相机地址
    :param str reqid: 请求唯一id，用于追踪请求
    :param int status: 区域相机拥堵状态（0 不拥堵   1 拥堵）
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/area/areaDeviceUpdateStatus'
        params = {
            'addr': addr,
            'reqid': reqid,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def area_enter(self, access_token: str, list: list = '', reqid: str = ''):
        """
        (弃用)区域入车
        :param list list: 进出车参数
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/area/enter'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def area_leave(self, access_token: str, list: list = '', reqid: str = ''):
        """
        (弃用)区域出车
        :param list list: 进出车参数
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/area/leave'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def area_updatestereoscopicdetectorparkaddrlist(self, access_token: str):
        """
        更新立体区域关联探测器地址服务内存数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/area/updateStereoscopicDetectorParkAddrList'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def areacamera_areainout(self, access_token: str, eventid: str = '', plateno: str = '', platereliability: int = '', regionip: str = '', triggerflag: int = ''):
        """
        区域相机进出车
        :param str eventid: 事件ID --对应图片事件Id
    :param str plateno: 车牌
    :param int platereliability: 可信度
    :param str regionip: 相机ip
    :param int triggerflag: 触发事件：3=来车 2=去车；
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaCamera/areaInOut'
        params = {
            'eventid': eventid,
            'plateno': plateno,
            'platereliability': platereliability,
            'regionip': regionip,
            'triggerflag': triggerflag,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areacamera_areapostpicture(self, access_token: str, carimageurl: str = '', eventid: str = '', regionip: str = ''):
        """
        区域相机更新图片
        :param str carimageurl: 图片路径
    :param str eventid: 事件ID
    :param str regionip: 区域相机ip
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaCamera/areaPostPicture'
        params = {
            'carimageurl': carimageurl,
            'eventid': eventid,
            'regionip': regionip,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def carinout_listinoutcarinfo(self, access_token: str, carinoutrecordendtablename: str = '', carinoutrecordstarttablename: str = '', intimeend: str = '', intimestart: str = '', outtimeend: str = '', outtimestart: str = '', pageindex: int = 1, pagesize: int = 100, plateno: str = '', spaceno: str = ''):
        """
        历史进出车明细分页查询
        :param str carinoutrecordendtablename: 查询入车结束时间对应表名
    :param str carinoutrecordstarttablename: 查询入车开始时间对应表名
    :param str intimeend: 查询入车结束时间（必填，时间跨度最长30天）
    :param str intimestart: 查询入车开始时间（必填，时间跨度最长30天）
    :param str outtimeend: 出车时间结束（必填，时间跨度最长30天）
    :param str outtimestart: 出车时间开始（必填，时间跨度最长30天）
    :param int pageindex: 页数
    :param int pagesize: 每页条目数
    :param str plateno: 车牌号
    :param str spaceno: 车位号
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/carInOut/listInOutCarInfo'
        params = {
            'carinoutrecordendtablename': carinoutrecordendtablename,
            'carinoutrecordstarttablename': carinoutrecordstarttablename,
            'intimeend': intimeend,
            'intimestart': intimestart,
            'outtimeend': outtimeend,
            'outtimestart': outtimestart,
            'pageindex': pageindex,
            'pagesize': pagesize,
            'plateno': plateno,
            'spaceno': spaceno,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def charge_postcaroutinfo(self, access_token: str, plateno: str = ''):
        """
        出场上报
        :param str plateno: 车牌号
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/charge/postCarOutInfo'
        params = {
            'plateno': plateno,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def deviceescalation_getinfo(self, access_token: str, areaname: str = '', deviceip: str = '', deviceport: int = '', floorname: str = '', parkno: str = ''):
        """
        查询车位编号对应地址信息
        :param str areaname: 区域名称
    :param str deviceip: 上报设备IP
    :param int deviceport: 上报设备端口
    :param str floorname: 楼层名称
    :param str parkno: 车位编号
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceEscalation/getInfo'
        params = {
            'areaname': areaname,
            'deviceip': deviceip,
            'deviceport': deviceport,
            'floorname': floorname,
            'parkno': parkno,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def deviceescalation_saveinfo(self, access_token: str, areaname: str = '', deviceip: str = '', deviceport: int = '', floorname: str = '', parkno: str = ''):
        """
        保存相机对应车位信息
        :param str areaname: 区域名称
    :param str deviceip: 上报设备IP
    :param int deviceport: 上报设备端口
    :param str floorname: 楼层名称
    :param str parkno: 车位编号
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceEscalation/saveInfo'
        params = {
            'areaname': areaname,
            'deviceip': deviceip,
            'deviceport': deviceport,
            'floorname': floorname,
            'parkno': parkno,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def deviceinfoopen_getdeviceinfostatus(self, access_token: str, deviceaddrs: list = '', deviceids: list = ''):
        """
        查询设备的实时状态
        :param list deviceaddrs: 设备地址集合
    :param list deviceids: 设备id集合
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceInfoOpen/getDeviceInfoStatus'
        params = {
            'deviceaddrs': deviceaddrs,
            'deviceids': deviceids,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def deviceinfoopen_selectpagelist(self, access_token: str, deviceaddrip: str = '', devicetype: int = '', id: int = '', nodedeviceaddr: str = '', onlinestatus: int = '', pageindex: int = 1, pagesize: int = 100, protocoltype: int = ''):
        """
        查询设备的实时状态分页查询
        :param str deviceaddrip: 设备地址（IP或者拨码）
    :param int devicetype: 设备类型 0=未知  1=车位相机  2=超声波探测器  3=LED屏  4=找车机  5=车位灯 6 LCD屏  7节点设备
    :param int id: 主键id
    :param str nodedeviceaddr: 节点设备地址
    :param int onlinestatus: 在线状态  0=离线  1=在线
    :param int pageindex: 页数
    :param int pagesize: 每页条目数
    :param int protocoltype: 设备协议类型
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceInfoOpen/selectPageList'
        params = {
            'deviceaddrip': deviceaddrip,
            'devicetype': devicetype,
            'id': id,
            'nodedeviceaddr': nodedeviceaddr,
            'onlinestatus': onlinestatus,
            'pageindex': pageindex,
            'pagesize': pagesize,
            'protocoltype': protocoltype,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def emergencymode_off(self, access_token: str):
        """
        关闭紧急模式
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/emergencyMode/off'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def emergencymode_on(self, access_token: str):
        """
        打开紧急模式
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/emergencyMode/on'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def healthcheck(self, access_token: str):
        """
        healthCheck
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/healthCheck'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def inichange_pushconfig(self, access_token: str, comname: str = '', dsprecog: int = '', firstserverip: str = '', picswitch: int = '', province: str = '', ret: int = '', witch: int = ''):
        """
        下发配置信息到C++
        :param str comname: 连接服务器的端口号 windows下是COM5, linux下是/dev/ttyS0
    :param int dsprecog: 控制软识别与硬识别 0 软识别, 1 硬识别
    :param str firstserverip: 设备IP前缀
    :param int picswitch: 是否开启空车牌图片收集功能  1 开启,  0 关闭
    :param str province: 车牌的默认省份(省份简称汉字) 默认为空
    :param int ret: 控制TCP还是485通讯 0 tcp, 1 485
    :param int witch: 控制故障状态的设备的开关 0 关闭， 1 开启
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/iniChange/pushConfig'
        params = {
            'comname': comname,
            'dsprecog': dsprecog,
            'firstserverip': firstserverip,
            'picswitch': picswitch,
            'province': province,
            'ret': ret,
            'witch': witch,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def ledscreen_notice(self, access_token: str, reqid: str = '', screenidlist: list = ''):
        """
        传入子屏id集合，触发这些子屏统计屏关联车位，并下发屏指令
        :param str reqid: 请求id
    :param list screenidlist: 子屏id集合
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/ledScreen/notice'
        params = {
            'reqid': reqid,
            'screenidlist': screenidlist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def ledscreen_noticetest(self, access_token: str, reqid: str = '', screenidlist: list = ''):
        """
        传入子屏id集合，进行屏测试操作，并下发屏指令
        :param str reqid: 请求id
    :param list screenidlist: 子屏id集合
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/ledScreen/noticeTest'
        params = {
            'reqid': reqid,
            'screenidlist': screenidlist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def ledscreen_updatescreencmd(self, access_token: str, reqid: str = '', screenidlist: list = ''):
        """
        第三方屏控制接口
        :param str reqid: 请求id
    :param list screenidlist: 子屏id集合
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/ledScreen/updateScreenCmd'
        params = {
            'reqid': reqid,
            'screenidlist': screenidlist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def nodedevice_initstatusbatch(self, access_token: str):
        """
        初始化节点设备状态为离线
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/nodeDevice/initStatusBatch'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def nodedevice_select485andipcamlist(self, access_token: str):
        """
        查询485节点和相机设备信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/nodeDevice/select485AndIpCamList'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def nodedevice_selectalllist(self, access_token: str):
        """
        查询所有节点设备地址
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/nodeDevice/selectAllList'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def nodedevice_selectinterandipcamlist(self, access_token: str):
        """
        查询网络节点和相机节点设备信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/nodeDevice/selectInterAndIpCamList'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def nodedevice_updatestatusbatchbyaddr(self, access_token: str, addrstr: str = '', status: int = ''):
        """
        批量更新节点设备状态
        :param str addrstr: 节点地址（,分割）
    :param int status: 节点设备状态(0 离线  1 在线)
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/nodeDevice/updateStatusBatchByAddr'
        params = {
            'addrstr': addrstr,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_clearcaptureurl(self, access_token: str):
        """
        清除内存中车位对应抓拍信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/clearCaptureUrl'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_enter(self, access_token: str, list: list = '', reqid: str = ''):
        """
        车位入车
        :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/enter'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_faultforfindcar(self, access_token: str, list: list = '', reqid: str = ''):
        """
        故障(找车系统)
        :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/faultForFindCar'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_faultforguidance(self, access_token: str, list: list = '', reqid: str = ''):
        """
        故障(引导系统)
        :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/faultForGuidance'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_freeforfindcar(self, access_token: str, list: list = '', reqid: str = ''):
        """
        无车(找车系统)
        :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/freeForFindCar'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_freeforguidance(self, access_token: str, list: list = '', reqid: str = ''):
        """
        无车(引导系统)
        :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/freeForGuidance'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_getcaptureurl(self, access_token: str):
        """
        获取内存中车位对应抓拍信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/getCaptureUrl'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_getemptycount(self, access_token: str, reqid: str = ''):
        """
        获取空车位数量
        :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/getEmptyCount'
        params = {
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_leave(self, access_token: str, list: list = '', reqid: str = ''):
        """
        车位出车
        :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/leave'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_occupyforfindcar(self, access_token: str, list: list = '', reqid: str = ''):
        """
        有车(找车系统)
        :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/occupyForFindCar'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_occupyforguidance(self, access_token: str, list: list = '', reqid: str = ''):
        """
        有车(引导系统)
        :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/occupyForGuidance'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_pushparkcamera(self, access_token: str):
        """
        下发C++相机抓拍指令
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/pushParkCamera'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_selectparklistbycondition(self, access_token: str, parkaddr: int = '', reqid: str = '', status: int = ''):
        """
        根据条件查询车位信息
        :param int parkaddr: 车位地址
    :param str reqid: 请求唯一id，用于追踪请求
    :param int status: 车位状态  0：空闲  1：占用  2：故障  3：停止服务
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/selectParkListByCondition'
        params = {
            'parkaddr': parkaddr,
            'reqid': reqid,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_snapallbylot(self, access_token: str):
        """
        全场车位相机抓拍指令
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/snapAllByLot'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_test(self, access_token: str):
        """
        test
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/test'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_test2(self, access_token: str):
        """
        test2
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/test2'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_updateallfault(self, access_token: str, reqid: str = ''):
        """
        更新所有车位为故障
        :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/updateAllFault'
        params = {
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_updatecaptureurl(self, access_token: str, parkaddr: str = '', parkingcaptureurl: str = ''):
        """
        更新车位相机抓拍照片路径
        :param str parkaddr: 车位地址(此处为不含后两位相机通道端口的车位地址)
    :param str parkingcaptureurl: 抓拍照片路径
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/updateCaptureUrl'
        params = {
            'parkaddr': parkaddr,
            'parkingcaptureurl': parkingcaptureurl,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_updateplateno(self, access_token: str, list: list = '', reqid: str = ''):
        """
        更新车牌
        :param list list: 更新参数
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/updatePlateNo'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def parkinglight_notice(self, access_token: str, freecolor: int = '', lighttype: int = '', lotid: int = '', noticetype: int = '', occupycolor: int = '', parkaddr: int = '', parkinglightarearelationlist: list = '', reqid: str = '', type: int = '', warningcolor: int = ''):
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
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/parking-light/notice'
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
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def parkinglight_noticeforstopwarn(self, access_token: str, reqid: str = '', screenidlist: list = ''):
        """
        用于终止违停告警的下发灯指令方法
        :param str reqid: 请求id
    :param list screenidlist: 子屏id集合
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/parking-light/noticeForStopWarn'
        params = {
            'reqid': reqid,
            'screenidlist': screenidlist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def parkmall_carend(self, access_token: str, platenumber: str = ''):
        """
        车辆出场上报
        :param str platenumber: 车牌号
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/parkmall/carEnd'
        params = {
            'platenumber': platenumber,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def screen_getalltcpaddr(self, access_token: str, reqid: str = ''):
        """
        获取所有网络屏的子屏地址
        :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/screen/getAllTcpAddr'
        params = {
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def screen_getlcdscreendata(self, access_token: str):
        """
        获取LCD屏下发数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/screen/getLcdScreenData'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def screen_initalloffline(self, access_token: str, reqid: str = ''):
        """
        把所有屏初始化为离线
        :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/screen/initAllOffLine'
        params = {
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def screen_ledpagerefresh(self, access_token: str, reqid: str = '', screenidlist: list = ''):
        """
        LED屏页面刷新
        :param str reqid: No description
    :param list screenidlist: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/screen/ledPageRefresh'
        params = {
            'reqid': reqid,
            'screenidlist': screenidlist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def screen_sendlcdscreendata(self, access_token: str, cmd: str = '', data: str = '', ip: str = '', reqid: str = '', scene: int = '', showtemplate: int = '', ts: int = '', type: int = ''):
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
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/screen/sendLcdScreenData'
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
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def screen_sendlcdscreendefaultdata(self, access_token: str):
        """
        下发LCD屏默认(数据库)数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/screen/sendLcdScreenDefaultData'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def screen_updatestatusbyaddr(self, access_token: str, addr: int = '', reqid: str = '', status: int = ''):
        """
        更新指定的屏为指定状态
        :param int addr: 子屏地址
    :param str reqid: 请求唯一id，用于追踪请求
    :param int status: 状态  1：在线  2：离线
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/screen/updateStatusByAddr'
        params = {
            'addr': addr,
            'reqid': reqid,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def screenrelated_listlcdscreen(self, access_token: str, iplist: list = '', pageindex: int = 1, pagesize: int = 100):
        """
        LCD屏设备列表查询
        :param list iplist: 屏ip集合
    :param int pageindex: 页数
    :param int pagesize: 每页条目数
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/screenRelated/listLcdScreen'
        params = {
            'iplist': iplist,
            'pageindex': pageindex,
            'pagesize': pagesize,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def taskmanage_resetall(self, access_token: str):
        """
        重新加载所有系统定时任务
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/taskManage/resetAll'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_controlhightask(self, access_token: str):
        """
        控制高负载任务(告警 进出车触发屏统计 有车无车上报) 1=开启 0=关闭
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/controlHighTask'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_dealwithgrpccmd(self, access_token: str, areaid: int = '', areaname: str = '', beginareaname: str = '', beginfloorname: str = '', beginspaceno: str = '', cmd: str = '', endareaname: str = '', endfloorname: str = '', endspaceno: str = '', floorid: int = '', floorname: str = '', imgname: str = '', intimeend: str = '', intimestart: str = '', ip: str = '', iplist: list = '', isbind: int = '', lcdcmddata: str = '', lighttype: int = '', nodedeviceaddr: str = '', operatetype: int = '', pageindex: int = 1, pagesize: int = 100, parkschmeparam: list = '', parkupdateparam: list = '', parkupdatestatusdtolist: list = '', plateno: str = '', recognitiontimeend: str = '', recognitiontimestart: str = '', reqid: str = '', spaceno: str = '', spaceschemeparam: list = '', systemtype: int = '', testingbatchid: str = '', warntype: int = ''):
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
    :param str recognitiontimeend: 查询识别记录结束日期
    :param str recognitiontimestart: 查询识别记录开始日期
    :param str reqid: 请求唯一id
    :param str spaceno: 车位编号
    :param list spaceschemeparam: 车位灯指令
    :param int systemtype: 设备类型  0-DSP车位相机   1-NODE节点控制器
    :param str testingbatchid: 质检中心检测批次ID
    :param int warntype: 告警类型  1：车位占用告警   2：车辆违停告警  3：特殊车辆入车  4：特殊车辆出车  5：车辆压线 6：油车违停
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/dealWithGrpcCmd'
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
            'recognitiontimeend': recognitiontimeend,
            'recognitiontimestart': recognitiontimestart,
            'reqid': reqid,
            'spaceno': spaceno,
            'spaceschemeparam': spaceschemeparam,
            'systemtype': systemtype,
            'testingbatchid': testingbatchid,
            'warntype': warntype,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def tool_devicestatustest(self, access_token: str):
        """
        /设备状态测试接口
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/deviceStatusTest'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_sendcommandtoallscreen(self, access_token: str):
        """
        统计所有的屏数据，并下发指令
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/sendCommandToAllScreen'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_sendlightcommandtofindcar(self, access_token: str, cmd: str = '', lighttype: int = '', list: list = '', reqid: str = ''):
        """
        给找车系统发送灯指令
        :param str cmd: No description
    :param int lighttype: No description
    :param list list: No description
    :param str reqid: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/sendLightCommandToFindCar'
        params = {
            'cmd': cmd,
            'lighttype': lighttype,
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def tool_sendlightcommandtoguidance(self, access_token: str, cmd: str = '', lighttype: int = '', list: list = '', reqid: str = ''):
        """
        给引导系统发送灯指令
        :param str cmd: No description
    :param int lighttype: No description
    :param list list: No description
    :param str reqid: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/sendLightCommandToGuidance'
        params = {
            'cmd': cmd,
            'lighttype': lighttype,
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def tool_snap(self, access_token: str):
        """
        质检 - 抓拍
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/snap'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_uniteapipro(self, access_token: str, appid: dict = 11168, appsecret: str = '890539996dc440bbb1151199c79bd3dc', params: dict = '', parkid: dict = 999508322, servicecode: str = 'getFloorList', uri: str = 'GetFloorList', version: str = '1.0.0'):
        """
        测试统一接口（正式环境）
        :param dict appid: 租户id
    :param str appsecret: 租户密钥
    :param dict params: 接口的额外参数 用json字符串传入
    :param dict parkid: 车场id
    :param str servicecode: 代码
    :param str uri: 接口uri
    :param str version: 请求头里的version 一般为1.0.0
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/uniteApiPro'
        params = {
            'appid': appid,
            'appsecret': appsecret,
            'params': params,
            'parkid': parkid,
            'servicecode': servicecode,
            'uri': uri,
            'version': version,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def tool_uniteapitest(self, access_token: str, appid: dict = 11681, appsecret: str = '7a216f04e543418f9b6378dddd1dd9e3', params: dict = '', parkid: dict = 9081, servicecode: str = 'getFloorList', uri: str = 'GetFloorList', version: str = '2.0.0'):
        """
        测试统一接口（测试环境）
        :param dict appid: 租户id
    :param str appsecret: 租户密钥
    :param dict params: 接口的额外参数 用json字符串传入
    :param dict parkid: 车场id
    :param str servicecode: 代码
    :param str uri: 接口uri
    :param str version: 请求头里的version 一般为1.0.0
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/uniteApiTest'
        params = {
            'appid': appid,
            'appsecret': appsecret,
            'params': params,
            'parkid': parkid,
            'servicecode': servicecode,
            'uri': uri,
            'version': version,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def tool_uploadimg(self, access_token: str):
        """
        场端图片统一上云
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/uploadImg'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def warnlog_generatecrossline(self, access_token: str, list: list = '', reqid: str = ''):
        """
        生成压线记录
        :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnLog/generateCrossLine'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def warnlog_stopcrossline(self, access_token: str, list: list = '', reqid: str = ''):
        """
        停止压线告警
        :param list list: 车位地址集合
    :param str reqid: 请求唯一id，用于追踪请求
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnLog/stopCrossLine'
        params = {
            'list': list,
            'reqid': reqid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()



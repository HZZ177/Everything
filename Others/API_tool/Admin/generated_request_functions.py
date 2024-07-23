import requests


class AdminAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def accessconfig_get(self, access_token: str):
        """
        获取配置信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/accessConfig/get'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def accessconfig_update(self, access_token: str, a: int = '', armycar: int = '', b: int = '', baudrate: int = '', broadcastinterval: int = '', broadcasttimes: int = '', c: int = '', channelhttp: str = '', civilcar: int = '', dspport: int = '', embassycar: int = '', farmcar: int = '', frontsavepath: str = '', id: int = '', ippre: str = '', newenergycar: int = '', nodeport: int = '', originalpicturepath: str = '', personalitycar: int = '', policecar: int = '', prnum: int = '', province: str = '', qualityinspectionpicturepath: str = '', recognitionlibpath: str = '', recognitionpath: str = '', recognitionswitch: int = '', regionpicturepath: str = '', serialport: str = '', setlprcs: int = '', setlrnum: int = '', setpriority: int = '', snappicturepath: str = '', switchserialport: int = '', temprcvpath: str = '', typeprnum: int = '', wujingcar: int = ''):
        """
        更新C++重构配置
        :param int a: No description
    :param int armycar: 军车车牌
    :param int b: No description
    :param int baudrate: 波特率
    :param int broadcastinterval: 播放间隔
    :param int broadcasttimes: 广播次数
    :param int c: No description
    :param str channelhttp: channel服务url地址
    :param int civilcar: 民航车牌
    :param int dspport: dsp 连接端口
    :param int embassycar: 大使馆车牌
    :param int farmcar: 农用车牌
    :param str frontsavepath: 前端保存路径
    :param int id: 唯一id
    :param str ippre: tcp地址拼接前缀
    :param int newenergycar: 新能源车牌
    :param int nodeport: node tcp节点连接端口
    :param str originalpicturepath: 原图保存路径
    :param int personalitycar: 个性化车牌
    :param int policecar: 警车车牌
    :param int prnum: 车牌类型长度
    :param str province: 默认省份
    :param str qualityinspectionpicturepath: 质检中心抓拍照片保存路径
    :param str recognitionlibpath: 识别库地址
    :param str recognitionpath: 识别文件路径
    :param int recognitionswitch: 识别库开关，0:关闭 1:开启
    :param str regionpicturepath: 区域相机照片保存路径
    :param str serialport: 串口地址
    :param int setlprcs: 识别种类（0:裁剪，1：A版，2：B版，3：A+B版，4：C版 5：A+C版，6：B+C，7：A+B+C）
    :param int setlrnum: 车牌数组长度
    :param int setpriority: 设置三地车牌输出优先级:1:MO 2:HK 3:CN 4:CN>HK>MO 5:MO>CN>HK 6:MO>HK>CN 7:HK>CN>MO 8:HK>MO>CN other:CN>MO>HK
    :param str snappicturepath: 相机抓拍照片保存路径
    :param int switchserialport: 485节点串口开关（0：关闭  1：开启）
    :param str temprcvpath: 临时文件路径
    :param int typeprnum: 车牌长度
    :param int wujingcar: 武警车牌
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/accessConfig/update'
        params = {
            'a': a,
            'armycar': armycar,
            'b': b,
            'baudrate': baudrate,
            'broadcastinterval': broadcastinterval,
            'broadcasttimes': broadcasttimes,
            'c': c,
            'channelhttp': channelhttp,
            'civilcar': civilcar,
            'dspport': dspport,
            'embassycar': embassycar,
            'farmcar': farmcar,
            'frontsavepath': frontsavepath,
            'id': id,
            'ippre': ippre,
            'newenergycar': newenergycar,
            'nodeport': nodeport,
            'originalpicturepath': originalpicturepath,
            'personalitycar': personalitycar,
            'policecar': policecar,
            'prnum': prnum,
            'province': province,
            'qualityinspectionpicturepath': qualityinspectionpicturepath,
            'recognitionlibpath': recognitionlibpath,
            'recognitionpath': recognitionpath,
            'recognitionswitch': recognitionswitch,
            'regionpicturepath': regionpicturepath,
            'serialport': serialport,
            'setlprcs': setlprcs,
            'setlrnum': setlrnum,
            'setpriority': setpriority,
            'snappicturepath': snappicturepath,
            'switchserialport': switchserialport,
            'temprcvpath': temprcvpath,
            'typeprnum': typeprnum,
            'wujingcar': wujingcar,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def apiaccessinfo_selectlist(self, access_token: str):
        """
        列表查询
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/apiAccessInfo/selectList'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def apiaccessinfo_skipauthbyall(self, access_token: str):
        """
        对全数据(修改全表字段)跳过鉴权
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/apiAccessInfo/skipAuthByAll'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def apiaccessinfo_updatebyid(self, access_token: str, apiperm: str = '', appcode: str = '', createtime: str = '', creator: str = '', deleted: bool = '', id: int = '', secret: str = '', skipauth: bool = '', tenantname: str = '', tenanttel: int = '', updatetime: str = '', updater: str = ''):
        """
        根据id更新配置
        :param str apiperm: 接口权限（逗号隔开）
    :param str appcode: 租户编码
    :param str createtime: 创建时间
    :param str creator: 创建人
    :param bool deleted: 是否删除0未删除1已删除
    :param int id: 主键id
    :param str secret: 秘钥
    :param bool skipauth: 是否跳过鉴权 0-否，1-是
    :param str tenantname: 租户名称
    :param int tenanttel: 租户电话
    :param str updatetime: 更新时间
    :param str updater: 更新人
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/apiAccessInfo/updateById'
        params = {
            'apiperm': apiperm,
            'appcode': appcode,
            'createtime': createtime,
            'creator': creator,
            'deleted': deleted,
            'id': id,
            'secret': secret,
            'skipauth': skipauth,
            'tenantname': tenantname,
            'tenanttel': tenanttel,
            'updatetime': updatetime,
            'updater': updater,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def apireportmanage_getall(self, access_token: str):
        """
        查询上行上报配置
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/apiReportManage/getAll'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def apireportmanage_switchconfig(self, access_token: str, cmd: str = '', otherreportswitch: int = '', unifiedswitch: int = ''):
        """
        上行上报配置开关接口
        :param str cmd: 接口编码标识
    :param int otherreportswitch: 其他平台上报总开关(0关闭，1开启)
    :param int unifiedswitch: 统一平台上报开关(0关闭，1开启)
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/apiReportManage/switchConfig'
        params = {
            'cmd': cmd,
            'otherreportswitch': otherreportswitch,
            'unifiedswitch': unifiedswitch,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def apireportmanage_updateotherreport(self, access_token: str, apipushinfodtolist: list = '', cmd: str = '', name: str = '', otherreportswitch: int = '', unifiedswitch: int = ''):
        """
        更新其他上报地址信息
        :param list apipushinfodtolist: No description
    :param str cmd: No description
    :param str name: No description
    :param int otherreportswitch: No description
    :param int unifiedswitch: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/apiReportManage/updateOtherReport'
        params = {
            'apipushinfodtolist': apipushinfodtolist,
            'cmd': cmd,
            'name': name,
            'otherreportswitch': otherreportswitch,
            'unifiedswitch': unifiedswitch,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areacamera_delete(self, access_token: str, idlist: str = ''):
        """
        删除
        :param str idlist: idList
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaCamera/delete'
        params = {
            'idlist': idlist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areacamera_insert(self, access_token: str, areacamerarelatelist: list = '', cameradirection: int = '', cameraip: str = '', id: int = '', remark: str = ''):
        """
        添加
        :param list areacamerarelatelist: 区域相机关联信息
    :param int cameradirection: 相机方向
    :param str cameraip: 相机ip
    :param int id: 主键
    :param str remark: 备注
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaCamera/insert'
        params = {
            'areacamerarelatelist': areacamerarelatelist,
            'cameradirection': cameradirection,
            'cameraip': cameraip,
            'id': id,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areacamera_selectpagelist(self, access_token: str, areaid: int = '', cameraip: str = '', endtime: str = '', id: int = '', pagenumber: int = 1, pagesize: int = 100, remark: str = '', starttime: str = ''):
        """
        分页查询
        :param int areaid: 区域id
    :param str cameraip: 相机ip
    :param str endtime: 结束时间
    :param int id: 主键
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str remark: 备注
    :param str starttime: 开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaCamera/selectPageList'
        params = {
            'areaid': areaid,
            'cameraip': cameraip,
            'endtime': endtime,
            'id': id,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'remark': remark,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areacamera_update(self, access_token: str, areacamerarelatelist: list = '', cameradirection: int = '', cameraip: str = '', id: int = '', remark: str = ''):
        """
        更新
        :param list areacamerarelatelist: 区域相机关联信息
    :param int cameradirection: 相机方向
    :param str cameraip: 相机ip
    :param int id: 主键
    :param str remark: 备注
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaCamera/update'
        params = {
            'areacamerarelatelist': areacamerarelatelist,
            'cameradirection': cameradirection,
            'cameraip': cameraip,
            'id': id,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areadevice_deletebatch(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaDevice/deleteBatch'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def areadevice_save(self, access_token: str, addr: int = '', areadevicerelations: list = '', id: int = '', remark: str = ''):
        """
        新增
        :param int addr: No description
    :param list areadevicerelations: No description
    :param int id: No description
    :param str remark: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaDevice/save'
        params = {
            'addr': addr,
            'areadevicerelations': areadevicerelations,
            'id': id,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areadevice_selectpagelist(self, access_token: str, addr: int = '', areaids: int = '', endtime: str = '', id: int = '', lotid: int = '', pagenumber: int = 1, pagesize: int = 100, starttime: str = '', status: int = ''):
        """
        分页查询
        :param int addr: 设备地址
    :param int areaids: 关联区域
    :param str endtime: 创建时间 - 结束时间
    :param int id: ID
    :param int lotid: 车场id
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str starttime: 创建时间 - 开始时间
    :param int status: 设备状态
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaDevice/selectPageList'
        params = {
            'addr': addr,
            'areaids': areaids,
            'endtime': endtime,
            'id': id,
            'lotid': lotid,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'starttime': starttime,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areadevice_update(self, access_token: str, addr: int = '', areadevicerelations: list = '', id: int = '', remark: str = ''):
        """
        修改
        :param int addr: No description
    :param list areadevicerelations: No description
    :param int id: No description
    :param str remark: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaDevice/update'
        params = {
            'addr': addr,
            'areadevicerelations': areadevicerelations,
            'id': id,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areainfo_addstereoscopicarea(self, access_token: str, floorid: int = '', id: int = '', lotid: int = '', name: str = '', parkspacecameraip: str = '', x: str = '', y: str = ''):
        """
        立体区域新增接口
        :param int floorid: 楼层id
    :param int id: 主键ID，新增时该值不传，主要用于更新
    :param int lotid: 车场编码
    :param str name: 名称
    :param str parkspacecameraip: 立体车位相机IP
    :param str x: x轴坐标
    :param str y: y轴坐标
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/addStereoscopicArea'
        params = {
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'name': name,
            'parkspacecameraip': parkspacecameraip,
            'x': x,
            'y': y,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areainfo_deletebatchbyid(self, access_token: str):
        """
        删除区域(参数Ids逗号分隔)
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/deleteBatchById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def areainfo_deletestereoscopicarea(self, access_token: str):
        """
        立体区域删除接口(参数Ids逗号分隔)
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/deleteStereoscopicArea'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def areainfo_insert(self, access_token: str, areainoutfreecountnumber: int = '', areaname: str = '', countstatisticstype: int = '', floorid: int = '', lotid: int = '', type: int = '', x: str = '', y: str = ''):
        """
        添加区域
        :param int areainoutfreecountnumber: 设置为区域进出车记录统计时，空闲车位数取值
    :param str areaname: No description
    :param int countstatisticstype: 0-关联车位空闲状态  1-区域进出车记录统计
    :param int floorid: No description
    :param int lotid: No description
    :param int type: 0:普通区域 1:立体车库区域
    :param str x: No description
    :param str y: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/insert'
        params = {
            'areainoutfreecountnumber': areainoutfreecountnumber,
            'areaname': areaname,
            'countstatisticstype': countstatisticstype,
            'floorid': floorid,
            'lotid': lotid,
            'type': type,
            'x': x,
            'y': y,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areainfo_listfloorarea(self, access_token: str):
        """
        遍历指定楼层的所有区域
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/listFloorArea'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def areainfo_saveparkarearelation(self, access_token: str, afterparklist: list = '', areaid: int = '', beforeparklist: list = ''):
        """
        保存车位关联区域关系
        :param list afterparklist: 区域绑定车位修改后列表
    :param int areaid: 车位关联区域id
    :param list beforeparklist: 区域绑定车位修改前列表
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/saveParkAreaRelation'
        params = {
            'afterparklist': afterparklist,
            'areaid': areaid,
            'beforeparklist': beforeparklist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areainfo_selectall(self, access_token: str):
        """
        查询所有区域
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/selectAll'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def areainfo_selectbyid(self, access_token: str):
        """
        区域详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/selectById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def areainfo_selectfloorareabylotid(self, access_token: str):
        """
        查询车场所有楼层 - 区域
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/selectFloorAreaByLotId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def areainfo_selectlistbyfloorid(self, access_token: str):
        """
        根据楼层查询区域列表
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/selectListByFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def areainfo_selectpagelist(self, access_token: str, areaid: int = '', areaname: str = '', endtime: str = '', floorid: int = '', lotid: int = '', pagenumber: int = 1, pagesize: int = 100, starttime: str = '', type: int = ''):
        """
        查询区域列表
        :param int areaid: id
    :param str areaname: 名称
    :param str endtime: 结束时间
    :param int floorid: 楼层id
    :param int lotid: 车场id
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str starttime: 开始时间
    :param int type: 0:普通区域 1:立体车库区域
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/selectPageList'
        params = {
            'areaid': areaid,
            'areaname': areaname,
            'endtime': endtime,
            'floorid': floorid,
            'lotid': lotid,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'starttime': starttime,
            'type': type,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areainfo_selectparklistbyarea(self, access_token: str, areaid: int = '', currentareaid: int = '', floorid: int = ''):
        """
        根据区域查询车位信息及关联区域关系
        :param int areaid: 车位关联区域id
    :param int currentareaid: 当前区域ID
    :param int floorid: 楼层id
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/selectParkListByArea'
        params = {
            'areaid': areaid,
            'currentareaid': currentareaid,
            'floorid': floorid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areainfo_selectstereoscopicpagelist(self, access_token: str, endtime: str = '', floorname: str = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, parkspacecameraip: str = '', parkspacecamerauniqueid: str = '', starttime: str = ''):
        """
        立体区域列表分页查询接口
        :param str endtime: 结束时间
    :param str floorname: 楼层名称
    :param str name: 名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkspacecameraip: 立体车位相机IP
    :param str parkspacecamerauniqueid: 立体车位相机唯一标识
    :param str starttime: 开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/selectStereoscopicPageList'
        params = {
            'endtime': endtime,
            'floorname': floorname,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkspacecameraip': parkspacecameraip,
            'parkspacecamerauniqueid': parkspacecamerauniqueid,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areainfo_updatebyid(self, access_token: str, areainoutfreecountnumber: int = '', areaname: str = '', countstatisticstype: int = '', floorid: int = '', id: int = '', type: int = '', x: str = '', y: str = ''):
        """
        更新区域
        :param int areainoutfreecountnumber: 设置为区域进出车记录统计时，空闲车位数取值
    :param str areaname: No description
    :param int countstatisticstype: 0-关联车位空闲状态  1-区域进出车记录统计
    :param int floorid: No description
    :param int id: No description
    :param int type: No description
    :param str x: No description
    :param str y: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/updateById'
        params = {
            'areainoutfreecountnumber': areainoutfreecountnumber,
            'areaname': areaname,
            'countstatisticstype': countstatisticstype,
            'floorid': floorid,
            'id': id,
            'type': type,
            'x': x,
            'y': y,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def areainfo_updatestereoscopicarea(self, access_token: str, floorid: int = '', id: int = '', lotid: int = '', name: str = '', parkspacecameraip: str = '', x: str = '', y: str = ''):
        """
        立体区域更新接口
        :param int floorid: 楼层id
    :param int id: 主键ID，新增时该值不传，主要用于更新
    :param int lotid: 车场编码
    :param str name: 名称
    :param str parkspacecameraip: 立体车位相机IP
    :param str x: x轴坐标
    :param str y: y轴坐标
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/areaInfo/updateStereoscopicArea'
        params = {
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'name': name,
            'parkspacecameraip': parkspacecameraip,
            'x': x,
            'y': y,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def auth_exttokenlogin(self, access_token: str):
        """
        第三方token登录接口
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/auth/extTokenLogin'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def auth_login(self, access_token: str):
        """
        登录接口
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/auth/login'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def auth_loginbyticket(self, access_token: str):
        """
        通过单车场ticket登录
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/auth/loginByTicket'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def auth_tokenvalid(self, access_token: str):
        """
        判断token是否有效
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/auth/tokenValid'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def auth_verifycode(self, access_token: str):
        """
        生成图形验证码
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/auth/verifyCode'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def berthrate(self, access_token: str):
        """
        泊位率测试接口
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/berthRate'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def berthrate_exportberthrate(self, access_token: str, endtime: str = '', selectberthtype: int = '', starttime: str = ''):
        """
        导出泊位率信息
        :param str endtime: 结束时间
    :param int selectberthtype: 查询泊位率类型，0：查询楼层，1：查询车位类型  默认查询楼层
    :param str starttime: 开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/berthRate/exportBerthRate'
        params = {
            'endtime': endtime,
            'selectberthtype': selectberthtype,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def berthrate_selectberthlist(self, access_token: str, endtime: str = '', selectberthtype: int = '', starttime: str = ''):
        """
        查询泊位率信息
        :param str endtime: 结束时间
    :param int selectberthtype: 查询泊位率类型，0：查询楼层，1：查询车位类型  默认查询楼层
    :param str starttime: 开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/berthRate/selectBerthList'
        params = {
            'endtime': endtime,
            'selectberthtype': selectberthtype,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def carinoutrecord_export(self, access_token: str, areaname: str = '', floorid: int = '', id: int = '', inendtime: str = '', instarttime: str = '', intype: int = '', lotid: int = '', outendtime: str = '', outstarttime: str = '', outtype: int = '', pagenumber: int = 1, pagesize: int = 100, parkno: str = '', plateno: str = ''):
        """
        历史进出车 - excel文件导出
        :param str areaname: 区域名称
    :param int floorid: 楼层id
    :param int id: 记录id
    :param str inendtime: 进车结束时间
    :param str instarttime: 进车开始时间
    :param int intype: 操作类型 0-自动入车 1-手动入车
    :param int lotid: 车场id
    :param str outendtime: 出车结束时间
    :param str outstarttime: 出车开始时间
    :param int outtype: 操作类型 0-自动出车 1-手动出车
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位号
    :param str plateno: 车牌号
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/car-in-out-record/export'
        params = {
            'areaname': areaname,
            'floorid': floorid,
            'id': id,
            'inendtime': inendtime,
            'instarttime': instarttime,
            'intype': intype,
            'lotid': lotid,
            'outendtime': outendtime,
            'outstarttime': outstarttime,
            'outtype': outtype,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkno': parkno,
            'plateno': plateno,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def carinoutrecord_selectpagelist(self, access_token: str, areaname: str = '', floorid: int = '', id: int = '', inendtime: str = '', instarttime: str = '', intype: int = '', lotid: int = '', outendtime: str = '', outstarttime: str = '', outtype: int = '', pagenumber: int = 1, pagesize: int = 100, parkno: str = '', plateno: str = ''):
        """
        分页查询
        :param str areaname: 区域名称
    :param int floorid: 楼层id
    :param int id: 记录id
    :param str inendtime: 进车结束时间
    :param str instarttime: 进车开始时间
    :param int intype: 操作类型 0-自动入车 1-手动入车
    :param int lotid: 车场id
    :param str outendtime: 出车结束时间
    :param str outstarttime: 出车开始时间
    :param int outtype: 操作类型 0-自动出车 1-手动出车
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位号
    :param str plateno: 车牌号
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/car-in-out-record/selectPageList'
        params = {
            'areaname': areaname,
            'floorid': floorid,
            'id': id,
            'inendtime': inendtime,
            'instarttime': instarttime,
            'intype': intype,
            'lotid': lotid,
            'outendtime': outendtime,
            'outstarttime': outstarttime,
            'outtype': outtype,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkno': parkno,
            'plateno': plateno,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def carinoutstatistics_exportbyfloor(self, access_token: str, recordendtime: str = '', recordstarttime: str = '', type: int = ''):
        """
        出入车流量导出（按楼层）
        :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param int type: 统计类型:入车-1 出车-0
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/car-in-out-statistics/exportByFloor'
        params = {
            'recordendtime': recordendtime,
            'recordstarttime': recordstarttime,
            'type': type,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def carinoutstatistics_exportbyspecies(self, access_token: str, recordendtime: str = '', recordstarttime: str = '', type: int = ''):
        """
        出入车流量导出（按车位种类）
        :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param int type: 统计类型:入车-1 出车-0
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/car-in-out-statistics/exportBySpecies'
        params = {
            'recordendtime': recordendtime,
            'recordstarttime': recordstarttime,
            'type': type,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def carinoutstatistics_listmapbyfloor(self, access_token: str, recordendtime: str = '', recordstarttime: str = '', type: int = ''):
        """
        楼层分组查询
        :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param int type: 统计类型:入车-1 出车-0
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/car-in-out-statistics/listMapByFloor'
        params = {
            'recordendtime': recordendtime,
            'recordstarttime': recordstarttime,
            'type': type,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def carinoutstatistics_refreshinoutcarstatistics(self, access_token: str):
        """
        刷新入出车流量报表
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/car-in-out-statistics/refreshInOutCarStatistics'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def carinoutstatistics_selectpagelist(self, access_token: str, pagenumber: int = 1, pagesize: int = 100, recordendtime: str = '', recordstarttime: str = '', type: int = ''):
        """
        分页查询(按车位种类)
        :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param int type: 统计类型:入车-1 出车-0
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/car-in-out-statistics/selectPageList'
        params = {
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'recordendtime': recordendtime,
            'recordstarttime': recordstarttime,
            'type': type,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def carinoutstatistics_sumcarinoutstatistics(self, access_token: str, recordendtime: str = '', recordstarttime: str = '', type: int = ''):
        """
        累计统计时间段的出入车流量
        :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param int type: 统计类型:入车-1 出车-0
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/car-in-out-statistics/sumCarInOutStatistics'
        params = {
            'recordendtime': recordendtime,
            'recordstarttime': recordstarttime,
            'type': type,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def carinoutrecordarea_selectpagelist(self, access_token: str, areaname: str = '', endtime: str = '', floorid: int = '', id: int = '', pagenumber: int = 1, pagesize: int = 100, plateno: str = '', starttime: str = '', type: int = ''):
        """
        分页查询
        :param str areaname: 区域名称
    :param str endtime: 结束时间
    :param int floorid: 楼层id
    :param int id: 主键
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str plateno: 车牌号
    :param str starttime: 开始时间
    :param int type: 事件类型  1：进车   2：出车
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/carInOutRecordArea/selectPageList'
        params = {
            'areaname': areaname,
            'endtime': endtime,
            'floorid': floorid,
            'id': id,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'plateno': plateno,
            'starttime': starttime,
            'type': type,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def colortransparencystyles_batchsave(self, access_token: str, colortransparencystylesaddrequestvolist: str = ''):
        """
        批量保存
        :param str colortransparencystylesaddrequestvolist: colorTransparencyStylesAddRequestVOList
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/color-transparency-styles/batchSave'
        params = {
            'colortransparencystylesaddrequestvolist': colortransparencystylesaddrequestvolist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def column_delete(self, access_token: str):
        """
        删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/column/delete'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def column_deletebyfloorid(self, access_token: str):
        """
        删除某个楼层柱子
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/column/deleteByFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def column_exportdatasynchronization(self, access_token: str):
        """
        数据同步-导出
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/column/exportDataSynchronization'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def column_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/column/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def column_importdatasynchronization(self, access_token: str, multipartfile: str = ''):
        """
        数据同步-导入
        :param str multipartfile: 导入文件
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/column/importDataSynchronization'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def column_selectpagelist(self, access_token: str, control: int = '', elementcustomid: int = '', floorenablestatus: int = '', floorid: int = '', floorname: str = '', floorstatus: int = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, parkaddr: int = '', parkcategory: int = '', parkno: str = '', status: int = '', type: int = '', uniqueidentificationfield: str = ''):
        """
        柱子列表
        :param int control: 车位控制 0-自动控制 1-手动控制
    :param int elementcustomid: 自定义元素的主id
    :param int floorenablestatus: 楼层启用状态，状态 1启用 2停用 空为所有
    :param int floorid: 楼层Id
    :param str floorname: 楼层名称
    :param int floorstatus: 楼层启用状态：状态 1启用 2停用
    :param int id: id
    :param int lotid: 车场Id
    :param str name: 元素名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int parkaddr: 车位地址
    :param int parkcategory: 车位种类 1 为普通车位  2 为新能源车位  3 为立体车位
    :param str parkno: 车位编号
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param int type: 元素类型 元素类型详情见枚举1 地面  2 柱子  3 车位
    :param str uniqueidentificationfield: 车位唯一标识字段
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/column/selectPageList'
        params = {
            'control': control,
            'elementcustomid': elementcustomid,
            'floorenablestatus': floorenablestatus,
            'floorid': floorid,
            'floorname': floorname,
            'floorstatus': floorstatus,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkaddr': parkaddr,
            'parkcategory': parkcategory,
            'parkno': parkno,
            'status': status,
            'type': type,
            'uniqueidentificationfield': uniqueidentificationfield,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def column_update(self, access_token: str, chargingbrand: str = '', chargingtype: int = '', control: int = '', createtime: str = '', deleted: bool = '', devicetype: int = '', enable: int = '', floorid: int = '', id: int = '', lotid: int = '', name: str = '', parkaddr: int = '', parkcategory: int = '', parkno: str = '', parkinglockequipmentno: str = '', parkingpropertyright: str = '', status: int = '', stereoscopicparkcameraaddr: int = '', toward: int = '', type: int = '', updatetime: str = ''):
        """
        更新
        :param str chargingbrand: No description
    :param int chargingtype: No description
    :param int control: 车位控制 0-自动控制 1-手动控制
    :param str createtime: 创建时间
    :param bool deleted: 是否删除0未删除1已删除
    :param int devicetype: No description
    :param int enable: No description
    :param int floorid: 楼层id
    :param int id: 主键
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int parkaddr: 车位地址
    :param int parkcategory: 车位种类  1 为普通车位  2 为新能源车位  3 为立体车位
    :param str parkno: 车位编号
    :param str parkinglockequipmentno: No description
    :param str parkingpropertyright: No description
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param int stereoscopicparkcameraaddr: 立体车位对应的相机地址
    :param int toward: 方向朝向（0-360角度整数存值）
    :param int type: 元素类型详情见枚举
    :param str updatetime: 更新时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/column/update'
        params = {
            'chargingbrand': chargingbrand,
            'chargingtype': chargingtype,
            'control': control,
            'createtime': createtime,
            'deleted': deleted,
            'devicetype': devicetype,
            'enable': enable,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'name': name,
            'parkaddr': parkaddr,
            'parkcategory': parkcategory,
            'parkno': parkno,
            'parkinglockequipmentno': parkinglockequipmentno,
            'parkingpropertyright': parkingpropertyright,
            'status': status,
            'stereoscopicparkcameraaddr': stereoscopicparkcameraaddr,
            'toward': toward,
            'type': type,
            'updatetime': updatetime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def config_getiniconfig(self, access_token: str):
        """
        查询C++参数配置信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/config/getIniConfig'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def config_getregistidentlibinfo(self, access_token: str):
        """
        查询注册识别库信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/config/getRegistIdentlibInfo'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def config_operateregistidentlib(self, access_token: str):
        """
        操作-注册识别库
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/config/operateRegistIdentlib'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def config_saveiniconfig(self, access_token: str, comname: str = '', dsprecog: int = '', picswitch: int = '', province: str = '', ret: int = '', witch: int = ''):
        """
        保存C++参数配置信息
        :param str comname: 连接服务器的端口号 windows下是COM5, linux下是/dev/ttyS0
    :param int dsprecog: 控制软识别与硬识别 0 软识别, 1 硬识别
    :param int picswitch: 是否开启空车牌图片收集功能  1 开启,  0 关闭
    :param str province: 车牌的默认省份(省份简称汉字) 默认为空
    :param int ret: 控制TCP还是485通讯 0 tcp, 1 485
    :param int witch: 控制故障状态的设备的开关 0 关闭， 1 开启
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/config/saveIniConfig'
        params = {
            'comname': comname,
            'dsprecog': dsprecog,
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


    def config_test(self, access_token: str):
        """
        操作-test
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/config/test'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def constant_commonenum(self, access_token: str):
        """
        枚举汇总
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/constant/commonEnum'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def coordinate_getfilestatus(self, access_token: str):
        """
        查询文件状态
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/coordinate/getFileStatus'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def coordinate_selectelementinfo(self, access_token: str, floorid: int = '', idorname: str = '', lotid: int = '', selecttype: int = '', type: int = ''):
        """
        元素按照id/编号精确查询
        :param int floorid: 楼层id
    :param str idorname: 根据id或者元素名称
    :param int lotid: 车场id
    :param int selecttype: 查询方式，0：模糊查询，1：精准查询
    :param int type: 元素类型
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/coordinate/selectElementInfo'
        params = {
            'floorid': floorid,
            'idorname': idorname,
            'lotid': lotid,
            'selecttype': selecttype,
            'type': type,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def coordinate_selectfuzzyelementinfo(self, access_token: str, floorid: int = '', keyword: str = '', lotid: int = '', type: str = ''):
        """
        元素模糊查询
        :param int floorid: 楼层id
    :param str keyword: 关键字
    :param int lotid: 车场id
    :param str type: 元素类型：parkNo parkAddr ibeaconMinor screenAddr machineIp pillarName customName
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/coordinate/selectFuzzyElementInfo'
        params = {
            'floorid': floorid,
            'keyword': keyword,
            'lotid': lotid,
            'type': type,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def coordinate_uploadcolumnfile(self, access_token: str, multipartfile: str = ''):
        """
        上传柱子坐标文件xslx
        :param str multipartfile: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/coordinate/uploadColumnFile'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def coordinate_uploadcustomfile(self, access_token: str, multipartfile: str = ''):
        """
        上传自定义元素坐标文件
        :param str multipartfile: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/coordinate/uploadCustomFile'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def coordinate_uploadgroundfile(self, access_token: str, multipartfile: str = ''):
        """
        上传地面坐标文件
        :param str multipartfile: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/coordinate/uploadGroundFile'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def coordinate_uploadparkfile(self, access_token: str, multipartfile: str = ''):
        """
        上传车位坐标文件xslx
        :param str multipartfile: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/coordinate/uploadParkFile'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def deviceescalation_selectexceptionpagelist(self, access_token: str, pagenumber: int = 1, pagesize: int = 100):
        """
        分页查询设备同步异常信息
        :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceEscalation/selectExceptionPageList'
        params = {
            'pagenumber': pagenumber,
            'pagesize': pagesize,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def deviceescalation_selectpagelist(self, access_token: str, areaname: str = '', deviceip: str = '', exception: int = '', floorname: str = '', pagenumber: int = 1, pagesize: int = 100, parkno: str = ''):
        """
        分页查询
        :param str areaname: 区域名称
    :param str deviceip: 上报设备IP
    :param int exception: 异常问题(0：正常， 1：车位编号重复， 2：无车位编号)
    :param str floorname: 楼层名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位编号
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceEscalation/selectPageList'
        params = {
            'areaname': areaname,
            'deviceip': deviceip,
            'exception': exception,
            'floorname': floorname,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkno': parkno,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def deviceinfo_deletebyids(self, access_token: str):
        """
        设备批量删除（id以英文逗号分隔开）
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceInfo/deleteByIds'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def deviceinfo_devicelistalign(self, access_token: str):
        """
        设备列表校准
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceInfo/deviceListAlign'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def deviceinfo_exportdevicelist(self, access_token: str, deviceaddrip: str = '', devicetype: int = '', id: int = '', nodedeviceaddr: str = '', onlinestatus: int = '', pagenumber: int = 1, pagesize: int = 100, protocoltype: int = '', workingstatus: int = ''):
        """
        设备列表导出
        :param str deviceaddrip: 设备地址（IP或者拨码）
    :param int devicetype: 设备类型 0=未知  1=车位相机  2=超声波探测器  3=LED屏  4=找车机  5=车位灯 6 LCD屏  7节点设备
    :param int id: 主键id
    :param str nodedeviceaddr: 节点设备地址
    :param int onlinestatus: 在线状态  0=离线  1=在线
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int protocoltype: 设备协议类型
    :param int workingstatus: 工作状态  0=故障  1=正常
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceInfo/exportDeviceList'
        params = {
            'deviceaddrip': deviceaddrip,
            'devicetype': devicetype,
            'id': id,
            'nodedeviceaddr': nodedeviceaddr,
            'onlinestatus': onlinestatus,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'protocoltype': protocoltype,
            'workingstatus': workingstatus,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def deviceinfo_getallnodeaddrlist(self, access_token: str):
        """
        获取节点地址列表
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceInfo/getAllNodeAddrList'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def deviceinfo_getallnodedevice(self, access_token: str):
        """
        获取节点设备地址列表
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceInfo/getAllNodeDevice'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def deviceinfo_importdatabyexcel(self, access_token: str, multipartfile: str = ''):
        """
        通过excel导入节点设备
        :param str multipartfile: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceInfo/importDataByExcel'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def deviceinfo_save(self, access_token: str, addr: str = '', devicetype: int = '', floorid: int = '', id: str = '', relateparknum: int = '', remark: str = ''):
        """
        新增 - 节点设备
        :param str addr: 设备ip转化后的数字，用于与设备建立连接
    :param int devicetype: 设备类型
    :param int floorid: 楼层id
    :param str id: id
    :param int relateparknum: 关联车位数
    :param str remark: 备注
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceInfo/save'
        params = {
            'addr': addr,
            'devicetype': devicetype,
            'floorid': floorid,
            'id': id,
            'relateparknum': relateparknum,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def deviceinfo_selectdeviceeventlog(self, access_token: str, deviceaddr: str = '', deviceid: int = '', devicetype: int = '', eventtimeend: str = '', eventtimestart: str = '', eventtype: int = '', pagenumber: int = 1, pagesize: int = 100):
        """
        设备事件日志查询
        :param str deviceaddr: 设备地址（ip或拨码）
    :param int deviceid: 设备id
    :param int devicetype: 设备类型
    :param str eventtimeend: 故障时间-结束
    :param str eventtimestart: 故障时间-开始
    :param int eventtype: 事件类型（1上线，2离线）
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceInfo/selectDeviceEventLog'
        params = {
            'deviceaddr': deviceaddr,
            'deviceid': deviceid,
            'devicetype': devicetype,
            'eventtimeend': eventtimeend,
            'eventtimestart': eventtimestart,
            'eventtype': eventtype,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def deviceinfo_selectpagelist(self, access_token: str, deviceaddrip: str = '', devicetype: int = '', id: int = '', nodedeviceaddr: str = '', onlinestatus: int = '', pagenumber: int = 1, pagesize: int = 100, protocoltype: int = '', workingstatus: int = ''):
        """
        设备列表分页查询
        :param str deviceaddrip: 设备地址（IP或者拨码）
    :param int devicetype: 设备类型 0=未知  1=车位相机  2=超声波探测器  3=LED屏  4=找车机  5=车位灯 6 LCD屏  7节点设备
    :param int id: 主键id
    :param str nodedeviceaddr: 节点设备地址
    :param int onlinestatus: 在线状态  0=离线  1=在线
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int protocoltype: 设备协议类型
    :param int workingstatus: 工作状态  0=故障  1=正常
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceInfo/selectPageList'
        params = {
            'deviceaddrip': deviceaddrip,
            'devicetype': devicetype,
            'id': id,
            'nodedeviceaddr': nodedeviceaddr,
            'onlinestatus': onlinestatus,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'protocoltype': protocoltype,
            'workingstatus': workingstatus,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def deviceinfo_update(self, access_token: str, addr: str = '', devicetype: int = '', floorid: int = '', id: str = '', relateparknum: int = '', remark: str = ''):
        """
        修改 - 节点设备
        :param str addr: 设备ip转化后的数字，用于与设备建立连接
    :param int devicetype: 设备类型
    :param int floorid: 楼层id
    :param str id: id
    :param int relateparknum: 关联车位数
    :param str remark: 备注
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/deviceInfo/update'
        params = {
            'addr': addr,
            'devicetype': devicetype,
            'floorid': floorid,
            'id': id,
            'relateparknum': relateparknum,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementconnector_deletebatchbyids(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-connector/deleteBatchByIds'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementconnector_exportdatasynchronization(self, access_token: str):
        """
        数据同步-导出
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-connector/exportDataSynchronization'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementconnector_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-connector/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementconnector_importdatasynchronization(self, access_token: str, multipartfile: str = ''):
        """
        数据同步-导入
        :param str multipartfile: 导入文件
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-connector/importDataSynchronization'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementconnector_insert(self, access_token: str, associatedconnectorids: str = '', floorid: int = '', lotid: int = '', name: str = '', species: int = '', xpoint: str = '', ypoint: str = ''):
        """
        添加
        :param str associatedconnectorids: 关联设施ids，id之间以,隔开
    :param int floorid: 楼层id
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int species: 种类 1：直梯 2：护梯 3：楼梯 4：出入口 5 车行车场入口 6 车行车场出口 7 车行场内入口 8 车行场内出口
    :param str xpoint: No description
    :param str ypoint: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-connector/insert'
        params = {
            'associatedconnectorids': associatedconnectorids,
            'floorid': floorid,
            'lotid': lotid,
            'name': name,
            'species': species,
            'xpoint': xpoint,
            'ypoint': ypoint,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementconnector_selectbylotid(self, access_token: str):
        """
        查询指定车场所有通行设施
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-connector/selectByLotId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementconnector_selectbylotidandfloorid(self, access_token: str):
        """
        查询指定楼层所有通行设施
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-connector/selectByLotIdAndFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementconnector_selectpagelist(self, access_token: str, associatedconnectorids: str = '', endtime: str = '', floorid: int = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, species: int = '', starttime: str = ''):
        """
        分页查询
        :param str associatedconnectorids: 关联设施ids
    :param str endtime: 结束时间
    :param int floorid: 楼层id
    :param int id: 主键id
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int species: 种类 1：直梯 2：护梯 3：楼梯 4：出入口
    :param str starttime: 开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-connector/selectPageList'
        params = {
            'associatedconnectorids': associatedconnectorids,
            'endtime': endtime,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'species': species,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementconnector_update(self, access_token: str, associatedconnectorids: str = '', floorid: int = '', id: int = '', lotid: int = '', name: str = '', species: int = '', xpoint: str = '', ypoint: str = ''):
        """
        更新
        :param str associatedconnectorids: 关联设施ids
    :param int floorid: 楼层id
    :param int id: 主键id
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int species: 种类 1：直梯 2：护梯 3：楼梯 4：出入口  5 车行车场入口 6 车行车场出口 7 车行场内入口 8 车行场内出口
    :param str xpoint: No description
    :param str ypoint: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-connector/update'
        params = {
            'associatedconnectorids': associatedconnectorids,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'name': name,
            'species': species,
            'xpoint': xpoint,
            'ypoint': ypoint,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementcustomdetail_addbatchcustomelement(self, access_token: str, custompointcontent: list = '', elementcustomid: int = '', floorid: int = '', lotid: int = ''):
        """
        批量添加自定义元素
        :param list custompointcontent: No description
    :param int elementcustomid: No description
    :param int floorid: No description
    :param int lotid: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom-detail/addBatchCustomElement'
        params = {
            'custompointcontent': custompointcontent,
            'elementcustomid': elementcustomid,
            'floorid': floorid,
            'lotid': lotid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementcustomdetail_delete(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom-detail/delete'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementcustomdetail_deletebyfloorid(self, access_token: str):
        """
        自定义元素 - 删除某个楼层数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom-detail/deleteByFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementcustomdetail_export(self, access_token: str, control: int = '', elementcustomid: int = '', floorenablestatus: int = '', floorid: int = '', floorname: str = '', floorstatus: int = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, parkaddr: int = '', parkcategory: int = '', parkno: str = '', status: int = '', type: int = '', uniqueidentificationfield: str = ''):
        """
        导出自定义元素详情列表
        :param int control: 车位控制 0-自动控制 1-手动控制
    :param int elementcustomid: 自定义元素的主id
    :param int floorenablestatus: 楼层启用状态，状态 1启用 2停用 空为所有
    :param int floorid: 楼层Id
    :param str floorname: 楼层名称
    :param int floorstatus: 楼层启用状态：状态 1启用 2停用
    :param int id: id
    :param int lotid: 车场Id
    :param str name: 元素名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int parkaddr: 车位地址
    :param int parkcategory: 车位种类 1 为普通车位  2 为新能源车位  3 为立体车位
    :param str parkno: 车位编号
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param int type: 元素类型 元素类型详情见枚举1 地面  2 柱子  3 车位
    :param str uniqueidentificationfield: 车位唯一标识字段
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom-detail/export'
        params = {
            'control': control,
            'elementcustomid': elementcustomid,
            'floorenablestatus': floorenablestatus,
            'floorid': floorid,
            'floorname': floorname,
            'floorstatus': floorstatus,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkaddr': parkaddr,
            'parkcategory': parkcategory,
            'parkno': parkno,
            'status': status,
            'type': type,
            'uniqueidentificationfield': uniqueidentificationfield,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementcustomdetail_exportdatasynchronization(self, access_token: str):
        """
        数据同步-导出
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom-detail/exportDataSynchronization'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementcustomdetail_importdatasynchronization(self, access_token: str, multipartfile: str = ''):
        """
        数据同步-导入
        :param str multipartfile: 导入文件
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom-detail/importDataSynchronization'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementcustomdetail_insert(self, access_token: str, elementcustomid: int = '', floorid: int = '', lotid: int = '', name: str = ''):
        """
        添加
        :param int elementcustomid: 自定义元素id
    :param int floorid: 楼层Id
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom-detail/insert'
        params = {
            'elementcustomid': elementcustomid,
            'floorid': floorid,
            'lotid': lotid,
            'name': name,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementcustomdetail_selectpagelist(self, access_token: str, control: int = '', elementcustomid: int = '', floorenablestatus: int = '', floorid: int = '', floorname: str = '', floorstatus: int = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, parkaddr: int = '', parkcategory: int = '', parkno: str = '', status: int = '', type: int = '', uniqueidentificationfield: str = ''):
        """
        自定义元素详情列表
        :param int control: 车位控制 0-自动控制 1-手动控制
    :param int elementcustomid: 自定义元素的主id
    :param int floorenablestatus: 楼层启用状态，状态 1启用 2停用 空为所有
    :param int floorid: 楼层Id
    :param str floorname: 楼层名称
    :param int floorstatus: 楼层启用状态：状态 1启用 2停用
    :param int id: id
    :param int lotid: 车场Id
    :param str name: 元素名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int parkaddr: 车位地址
    :param int parkcategory: 车位种类 1 为普通车位  2 为新能源车位  3 为立体车位
    :param str parkno: 车位编号
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param int type: 元素类型 元素类型详情见枚举1 地面  2 柱子  3 车位
    :param str uniqueidentificationfield: 车位唯一标识字段
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom-detail/selectPageList'
        params = {
            'control': control,
            'elementcustomid': elementcustomid,
            'floorenablestatus': floorenablestatus,
            'floorid': floorid,
            'floorname': floorname,
            'floorstatus': floorstatus,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkaddr': parkaddr,
            'parkcategory': parkcategory,
            'parkno': parkno,
            'status': status,
            'type': type,
            'uniqueidentificationfield': uniqueidentificationfield,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementcustomdetail_selectpagelistoffloor(self, access_token: str, control: int = '', elementcustomid: int = '', floorenablestatus: int = '', floorid: int = '', floorname: str = '', floorstatus: int = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, parkaddr: int = '', parkcategory: int = '', parkno: str = '', status: int = '', type: int = '', uniqueidentificationfield: str = ''):
        """
        3D预览自定义元素列表
        :param int control: 车位控制 0-自动控制 1-手动控制
    :param int elementcustomid: 自定义元素的主id
    :param int floorenablestatus: 楼层启用状态，状态 1启用 2停用 空为所有
    :param int floorid: 楼层Id
    :param str floorname: 楼层名称
    :param int floorstatus: 楼层启用状态：状态 1启用 2停用
    :param int id: id
    :param int lotid: 车场Id
    :param str name: 元素名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int parkaddr: 车位地址
    :param int parkcategory: 车位种类 1 为普通车位  2 为新能源车位  3 为立体车位
    :param str parkno: 车位编号
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param int type: 元素类型 元素类型详情见枚举1 地面  2 柱子  3 车位
    :param str uniqueidentificationfield: 车位唯一标识字段
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom-detail/selectPageListOfFloor'
        params = {
            'control': control,
            'elementcustomid': elementcustomid,
            'floorenablestatus': floorenablestatus,
            'floorid': floorid,
            'floorname': floorname,
            'floorstatus': floorstatus,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkaddr': parkaddr,
            'parkcategory': parkcategory,
            'parkno': parkno,
            'status': status,
            'type': type,
            'uniqueidentificationfield': uniqueidentificationfield,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementcustomdetail_update(self, access_token: str, id: int = '', name: str = ''):
        """
        编辑
        :param int id: 自定义元素详情的id
    :param str name: 名称
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom-detail/update'
        params = {
            'id': id,
            'name': name,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementcustom_delete(self, access_token: str):
        """
        删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom/delete'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementcustom_edit(self, access_token: str, height: str = '', id: int = '', name: str = '', suspendheight: str = ''):
        """
        编辑
        :param str height: 高度 默认0.1m
    :param int id: 主键id
    :param str name: 名称
    :param str suspendheight: 离地高度 默认0m
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom/edit'
        params = {
            'height': height,
            'id': id,
            'name': name,
            'suspendheight': suspendheight,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementcustom_insert(self, access_token: str, height: str = '', lotid: int = '', name: str = '', suspendheight: str = ''):
        """
        添加
        :param str height: 高度 默认0.1m
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param str suspendheight: 离地高度 默认0m
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom/insert'
        params = {
            'height': height,
            'lotid': lotid,
            'name': name,
            'suspendheight': suspendheight,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementcustom_listelementcustom(self, access_token: str, lotid: int = ''):
        """
        查询自定义元素列表
        :param int lotid: 车场id
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom/listElementCustom'
        params = {
            'lotid': lotid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementcustom_listelementcustomdetail(self, access_token: str, lotid: int = ''):
        """
        根据车场和楼层查询自定义元素的坐标和高度等信息
        :param int lotid: 车场id
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-custom/listElementCustomDetail'
        params = {
            'lotid': lotid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementmachineconfig_deletemachinerouteinfobyids(self, access_token: str):
        """
        批量删除找车路线信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine-config/deleteMachineRouteInfoByIds'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementmachineconfig_editmachinerouteinfo(self, access_token: str, acrosselevatorid: int = '', acrosselevatorname: str = '', acrosstype: int = '', createtime: str = '', creator: str = '', endid: int = '', endname: str = '', id: int = '', imgsrc: str = '', startid: int = '', startname: str = '', updatetime: str = '', updater: str = ''):
        """
        编辑找车路线信息
        :param int acrosselevatorid: 找车机IP
    :param str acrosselevatorname: 终点层平面
    :param int acrosstype: 跨层类型(0:楼层到楼层 1:查询机到楼层)
    :param str createtime: 创建时间
    :param str creator: 创建人
    :param int endid: 终点层平面
    :param str endname: 起始层平面
    :param int id: 主键
    :param str imgsrc: 提示图片
    :param int startid: 起始层平面
    :param str startname: 找车机IP
    :param str updatetime: 更新时间
    :param str updater: 更新人
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine-config/editMachineRouteInfo'
        params = {
            'acrosselevatorid': acrosselevatorid,
            'acrosselevatorname': acrosselevatorname,
            'acrosstype': acrosstype,
            'createtime': createtime,
            'creator': creator,
            'endid': endid,
            'endname': endname,
            'id': id,
            'imgsrc': imgsrc,
            'startid': startid,
            'startname': startname,
            'updatetime': updatetime,
            'updater': updater,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementmachineconfig_getallmachinerouteinfo(self, access_token: str):
        """
        查询所有找车路线信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine-config/getAllMachineRouteInfo'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementmachineconfig_getconfiginfo(self, access_token: str):
        """
        查询配置信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine-config/getConfigInfo'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementmachineconfig_savemachinerouteinfo(self, access_token: str, acrosselevatorid: int = '', acrosselevatorname: str = '', acrosstype: int = '', createtime: str = '', creator: str = '', endid: int = '', endname: str = '', id: int = '', imgsrc: str = '', startid: int = '', startname: str = '', updatetime: str = '', updater: str = ''):
        """
        保存找车路线信息
        :param int acrosselevatorid: 找车机IP
    :param str acrosselevatorname: 终点层平面
    :param int acrosstype: 跨层类型(0:楼层到楼层 1:查询机到楼层)
    :param str createtime: 创建时间
    :param str creator: 创建人
    :param int endid: 终点层平面
    :param str endname: 起始层平面
    :param int id: 主键
    :param str imgsrc: 提示图片
    :param int startid: 起始层平面
    :param str startname: 找车机IP
    :param str updatetime: 更新时间
    :param str updater: 更新人
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine-config/saveMachineRouteInfo'
        params = {
            'acrosselevatorid': acrosselevatorid,
            'acrosselevatorname': acrosselevatorname,
            'acrosstype': acrosstype,
            'createtime': createtime,
            'creator': creator,
            'endid': endid,
            'endname': endname,
            'id': id,
            'imgsrc': imgsrc,
            'startid': startid,
            'startname': startname,
            'updatetime': updatetime,
            'updater': updater,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementmachineconfig_updateconfiginfo(self, access_token: str, createtime: str = '', creator: str = '', emptyplaterecordcount: int = '', foreginlanguage: str = '', id: int = '', inquireways: list = '', isopenprint: int = '', isopenqrcode: int = '', languagesupport: int = '', machinemapswitch: int = '', parkmaxnum: int = '', platemaxnum: int = '', rotationangle: int = '', rotationswitch: int = '', routeqrswitch: int = '', routeqrtype: int = '', routeqrurl: str = '', scheduleface: int = '', updatetime: str = '', updater: str = ''):
        """
        更新配置信息
        :param str createtime: 创建时间
    :param str creator: 创建人
    :param int emptyplaterecordcount: 空车牌查询显示记录上限
    :param str foreginlanguage: 设置的第三种语言支持 ms:马来西亚 esp:西班牙 未设置则返回空
    :param int id: 主键
    :param list inquireways: 查询方式
    :param int isopenprint: 是否启用停车打印功能 0:不启用 1:启用
    :param int isopenqrcode: 是否显示找车二维码(0：否，1：是)
    :param int languagesupport: 设置要显示的查询机语言版本 0:中文+英文 1:中文 2:英文
    :param int machinemapswitch: 找车机是否开启3D地图(1为开启  0 为关闭)
    :param int parkmaxnum: 车位号输入上限
    :param int platemaxnum: 车牌号输入上限
    :param int rotationangle: 找车机旋转角度，0-360
    :param int rotationswitch: 找车机地图是否根据找车机朝向旋转(0为开启  1为关闭)，默认关闭
    :param int routeqrswitch: 找车路线二维码开关  0=关  1=开
    :param int routeqrtype: 找车路线二维码类型  0=自定义二维码
    :param str routeqrurl: 找车路线二维码图片路径
    :param int scheduleface: 定时给找车机推送车辆出场，删除人脸数据(0为开启  1为关闭)
    :param str updatetime: 更新时间
    :param str updater: 更新人
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine-config/updateConfigInfo'
        params = {
            'createtime': createtime,
            'creator': creator,
            'emptyplaterecordcount': emptyplaterecordcount,
            'foreginlanguage': foreginlanguage,
            'id': id,
            'inquireways': inquireways,
            'isopenprint': isopenprint,
            'isopenqrcode': isopenqrcode,
            'languagesupport': languagesupport,
            'machinemapswitch': machinemapswitch,
            'parkmaxnum': parkmaxnum,
            'platemaxnum': platemaxnum,
            'rotationangle': rotationangle,
            'rotationswitch': rotationswitch,
            'routeqrswitch': routeqrswitch,
            'routeqrtype': routeqrtype,
            'routeqrurl': routeqrurl,
            'scheduleface': scheduleface,
            'updatetime': updatetime,
            'updater': updater,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementmachine_deletebatchbyids(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine/deleteBatchByIds'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementmachine_deletebyfloorid(self, access_token: str):
        """
        找车机-删除某个楼层的找车机
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine/deleteByFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementmachine_exportdatasynchronization(self, access_token: str):
        """
        数据同步-导出
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine/exportDataSynchronization'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementmachine_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementmachine_importdatasynchronization(self, access_token: str, multipartfile: str = ''):
        """
        数据同步-导入
        :param str multipartfile: 导入文件
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine/importDataSynchronization'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementmachine_insert(self, access_token: str, directionnum: int = '', floorid: int = '', ip: str = '', lotid: int = '', name: str = '', species: int = '', xpoint: str = '', ypoint: str = ''):
        """
        添加
        :param int directionnum: 朝向(度数)
    :param int floorid: 楼层id
    :param str ip: 找车机ip
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int species: 种类 1：立式找车机 2：壁式找车机
    :param str xpoint: No description
    :param str ypoint: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine/insert'
        params = {
            'directionnum': directionnum,
            'floorid': floorid,
            'ip': ip,
            'lotid': lotid,
            'name': name,
            'species': species,
            'xpoint': xpoint,
            'ypoint': ypoint,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementmachine_listmachineip(self, access_token: str):
        """
        有效的找车机ip集合
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine/listMachineIp'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementmachine_selectbylotidandfloorid(self, access_token: str):
        """
        查询指定楼层所有的找车机
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine/selectByLotIdAndFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementmachine_selectpagelist(self, access_token: str, endtime: str = '', floorenablestatus: int = '', floorid: int = '', id: int = '', ip: str = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, species: int = '', starttime: str = ''):
        """
        分页查询
        :param str endtime: 结束时间
    :param int floorenablestatus: 楼层启用状态，状态 1启用 2停用 空为所有
    :param int floorid: 楼层id
    :param int id: 主键id
    :param str ip: 找车机ip
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int species: 种类 1：立式找车机 2：壁式找车机
    :param str starttime: 开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine/selectPageList'
        params = {
            'endtime': endtime,
            'floorenablestatus': floorenablestatus,
            'floorid': floorid,
            'id': id,
            'ip': ip,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'species': species,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementmachine_update(self, access_token: str, directionnum: int = '', floorid: int = '', id: int = '', ip: str = '', lotid: int = '', name: str = '', species: int = '', xpoint: str = '', ypoint: str = ''):
        """
        更新
        :param int directionnum: 朝向(度数)
    :param int floorid: 楼层id
    :param int id: 主键id
    :param str ip: 找车机ip
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int species: 种类 1：立式找车机 2：壁式找车机
    :param str xpoint: No description
    :param str ypoint: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-machine/update'
        params = {
            'directionnum': directionnum,
            'floorid': floorid,
            'id': id,
            'ip': ip,
            'lotid': lotid,
            'name': name,
            'species': species,
            'xpoint': xpoint,
            'ypoint': ypoint,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementpath_exporttotxt(self, access_token: str):
        """
        导出文本格式的数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-path/exportToTxt'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementpath_getbylotidandfloorid(self, access_token: str):
        """
        获取指定楼层的路网数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-path/getByLotIdAndFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementpath_importbytxt(self, access_token: str, multipartfile: str = ''):
        """
        通过文本导入数据
        :param str multipartfile: multipartFile
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-path/importByTxt'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementpath_update(self, access_token: str, floorid: int = '', lotid: int = '', pathlist: list = ''):
        """
        更新路网数据
        :param int floorid: 楼层id
    :param int lotid: 车场id
    :param list pathlist: 路网集合
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-path/update'
        params = {
            'floorid': floorid,
            'lotid': lotid,
            'pathlist': pathlist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementscreen_deletebatchbyids(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/deleteBatchByIds'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreen_deletebyfloorid(self, access_token: str):
        """
        屏 - 删除某个楼层数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/deleteByFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreen_downloadlcdlog(self, access_token: str):
        """
        下载LCD日志文件
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/downloadLcdLog'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreen_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreen_getelementscreenwithlcdconfig(self, access_token: str):
        """
        根据主键获取详情(包含LCD屏配置信息)
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/getElementScreenWithLcdConfig'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreen_getelementscreenwithlcdconfigbyip(self, access_token: str):
        """
        根据ip地址获取详情(包含LCD屏配置信息)
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/getElementScreenWithLcdConfigByIp'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreen_getscreenconfigofh5(self, access_token: str):
        """
        H5单页面展示信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/getScreenConfigOfH5'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreen_insert(self, access_token: str, direction: int = '', elementscreenchildrequestvolist: list = '', floorid: int = '', lotid: int = '', name: str = '', screenaddr: int = '', screencategory: int = '', screentype: int = '', species: int = '', subscreennum: int = '', xpoint: str = '', ypoint: str = ''):
        """
        添加
        :param int direction: 屏顺序 1 为递增  -1 为递减
    :param list elementscreenchildrequestvolist: 子屏参数
    :param int floorid: 楼层id
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int screenaddr: 屏地址
    :param int screencategory: No description
    :param int screentype: 屏类型 0=一体屏 1=双拼接屏
    :param int species: 种类 1：LED屏 2：LCD屏
    :param int subscreennum: 子屏数 1：单向屏 2：双向屏 3：三向屏
    :param str xpoint: No description
    :param str ypoint: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/insert'
        params = {
            'direction': direction,
            'elementscreenchildrequestvolist': elementscreenchildrequestvolist,
            'floorid': floorid,
            'lotid': lotid,
            'name': name,
            'screenaddr': screenaddr,
            'screencategory': screencategory,
            'screentype': screentype,
            'species': species,
            'subscreennum': subscreennum,
            'xpoint': xpoint,
            'ypoint': ypoint,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementscreen_ledpagerefresh(self, access_token: str):
        """
        LED屏页面刷新
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/ledPageRefresh'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreen_move(self, access_token: str, direction: int = '', elementscreenchildrequestvolist: list = '', floorid: int = '', id: int = '', lotid: int = '', name: str = '', screenaddr: int = '', screentype: int = '', species: int = '', subscreennum: int = '', xpoint: str = '', ypoint: str = ''):
        """
        移动
        :param int direction: 屏方向（屏顺序配置字段，用来控制屏从左到右地址是递增还是递减）
    :param list elementscreenchildrequestvolist: 子屏参数
    :param int floorid: 楼层id
    :param int id: 主键id
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int screenaddr: 屏地址
    :param int screentype: 屏类型 0=一体屏 1=双拼接屏
    :param int species: 种类 1：LED屏 2：LCD屏
    :param int subscreennum: 子屏数 1：单向屏 2：双向屏 3：三向屏
    :param str xpoint: No description
    :param str ypoint: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/move'
        params = {
            'direction': direction,
            'elementscreenchildrequestvolist': elementscreenchildrequestvolist,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'name': name,
            'screenaddr': screenaddr,
            'screentype': screentype,
            'species': species,
            'subscreennum': subscreennum,
            'xpoint': xpoint,
            'ypoint': ypoint,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementscreen_savelcdconfig(self, access_token: str, createtime: str = '', creator: str = '', deleted: bool = '', direction: int = '', floorid: int = '', id: int = '', lcdscreenconfiglist: list = '', lotid: int = '', name: str = '', onlinestatus: list = '', refreshflag: bool = '', remark: str = '', screenaddr: int = '', screentype: int = '', showtemplate: int = '', species: int = '', subscreennum: int = '', updatetime: str = '', updater: str = '', xpoint: str = '', ypoint: str = ''):
        """
        保存LCD屏配置
        :param str createtime: 创建时间
    :param str creator: 创建人
    :param bool deleted: 是否删除 0未删除 1已删除
    :param int direction: 屏方向（屏顺序配置字段，用来控制屏从左到右地址是递增还是递减）
    :param int floorid: 楼层id
    :param int id: 主屏id
    :param list lcdscreenconfiglist: LCD屏配置集合
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param list onlinestatus: No description
    :param bool refreshflag: No description
    :param str remark: 备注
    :param int screenaddr: 屏地址
    :param int screentype: 屏类型 0=一体屏 1=双拼接屏
    :param int showtemplate: 展示模板
    :param int species: 种类 1：LED屏 2：LCD屏
    :param int subscreennum: 子屏数 1：单向屏 2：双向屏 3：三向屏
    :param str updatetime: 更新时间
    :param str updater: 更新人
    :param str xpoint: No description
    :param str ypoint: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/saveLcdConfig'
        params = {
            'createtime': createtime,
            'creator': creator,
            'deleted': deleted,
            'direction': direction,
            'floorid': floorid,
            'id': id,
            'lcdscreenconfiglist': lcdscreenconfiglist,
            'lotid': lotid,
            'name': name,
            'onlinestatus': onlinestatus,
            'refreshflag': refreshflag,
            'remark': remark,
            'screenaddr': screenaddr,
            'screentype': screentype,
            'showtemplate': showtemplate,
            'species': species,
            'subscreennum': subscreennum,
            'updatetime': updatetime,
            'updater': updater,
            'xpoint': xpoint,
            'ypoint': ypoint,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementscreen_selectbylotidandfloorid(self, access_token: str):
        """
        查询指定楼层所有屏
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/selectByLotIdAndFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreen_selectpagelist(self, access_token: str, endtime: str = '', floorenablestatus: int = '', floorid: int = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, screenaddr: int = '', species: int = '', starttime: str = '', subscreennum: int = ''):
        """
        分页查询
        :param str endtime: 结束时间
    :param int floorenablestatus: 楼层启用状态，状态 1启用 2停用 空为所有
    :param int floorid: 楼层id
    :param int id: 主键id
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int screenaddr: 屏地址
    :param int species: 种类 1：LED屏 2：LCD屏
    :param str starttime: 开始时间
    :param int subscreennum: 子屏数 1：单向屏 2：双向屏 3：三向屏
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/selectPageList'
        params = {
            'endtime': endtime,
            'floorenablestatus': floorenablestatus,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'screenaddr': screenaddr,
            'species': species,
            'starttime': starttime,
            'subscreennum': subscreennum,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementscreen_selectscreenlistbypage(self, access_token: str, endtime: str = '', floorenablestatus: int = '', floorid: int = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, screenaddr: int = '', species: int = '', starttime: str = '', subscreennum: int = ''):
        """
        分页查询屏设备列表
        :param str endtime: 结束时间
    :param int floorenablestatus: 楼层启用状态，状态 1启用 2停用 空为所有
    :param int floorid: 楼层id
    :param int id: 主键id
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int screenaddr: 屏地址
    :param int species: 种类 1：LED屏 2：LCD屏
    :param str starttime: 开始时间
    :param int subscreennum: 子屏数 1：单向屏 2：双向屏 3：三向屏
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/selectScreenListByPage'
        params = {
            'endtime': endtime,
            'floorenablestatus': floorenablestatus,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'screenaddr': screenaddr,
            'species': species,
            'starttime': starttime,
            'subscreennum': subscreennum,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementscreen_sendlcdscreencmd(self, access_token: str, cmd: str = '', data: str = '', ip: str = '', reqid: str = '', scene: str = '', screenaddr: int = '', showtemplate: int = '', ts: int = '', type: int = ''):
        """
        LCD屏设备指令下发
        :param str cmd: pageUpdate页面更新;dataUpdate数据更新;temporaryPush临时推送;scriptExecution脚本执行;
    :param str data: 数据体
    :param str ip: lcd屏ip
    :param str reqid: 请求ID(不传入时，系统内部会随机生成默认值)
    :param str scene: 场景:1标准引导;999非标页面,默认：1标准引导
    :param int screenaddr: lcd屏地址
    :param int showtemplate: 展示模板  0=非标模板 1=模板一
    :param int ts: 时间戳(不传入时，系统内部会根据当前时间生成默认值)
    :param int type: 屏标识(0:一体屏,1:双拼接屏左屏,2:双拼接屏右屏)
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/sendLcdScreenCmd'
        params = {
            'cmd': cmd,
            'data': data,
            'ip': ip,
            'reqid': reqid,
            'scene': scene,
            'screenaddr': screenaddr,
            'showtemplate': showtemplate,
            'ts': ts,
            'type': type,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementscreen_update(self, access_token: str, direction: int = '', elementscreenchildrequestvolist: list = '', floorid: int = '', id: int = '', lotid: int = '', name: str = '', screenaddr: int = '', screentype: int = '', species: int = '', subscreennum: int = '', xpoint: str = '', ypoint: str = ''):
        """
        更新
        :param int direction: 屏方向（屏顺序配置字段，用来控制屏从左到右地址是递增还是递减）
    :param list elementscreenchildrequestvolist: 子屏参数
    :param int floorid: 楼层id
    :param int id: 主键id
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int screenaddr: 屏地址
    :param int screentype: 屏类型 0=一体屏 1=双拼接屏
    :param int species: 种类 1：LED屏 2：LCD屏
    :param int subscreennum: 子屏数 1：单向屏 2：双向屏 3：三向屏
    :param str xpoint: No description
    :param str ypoint: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element-screen/update'
        params = {
            'direction': direction,
            'elementscreenchildrequestvolist': elementscreenchildrequestvolist,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'name': name,
            'screenaddr': screenaddr,
            'screentype': screentype,
            'species': species,
            'subscreennum': subscreennum,
            'xpoint': xpoint,
            'ypoint': ypoint,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def element3dmodel_deletebyid(self, access_token: str):
        """
        删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element3dModel/deleteById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def element3dmodel_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element3dModel/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def element3dmodel_insert(self, access_token: str, createtime: str = '', creator: str = '', elementname: str = '', elementtype: int = '', floorid: int = '', id: int = '', lotid: int = '', rotationangle: str = '', scale: str = '', suspendheight: str = '', updatetime: str = '', updater: str = '', xpoint: int = '', ypoint: int = ''):
        """
        添加
        :param str createtime: No description
    :param str creator: No description
    :param str elementname: 元素名称
    :param int elementtype: 元素类型 1楼梯  2 直梯  3扶梯
    :param int floorid: 楼层id
    :param int id: id
    :param int lotid: 车场id
    :param str rotationangle: 模型的朝向设置（0~360），实时预览，默认为0
    :param str scale: 缩放比例，模型的大小控制（0.5-2），实时预览，默认为1
    :param str suspendheight: 离地高度，模型底面离地面上表面的距离（0-10.0），默认为0
    :param str updatetime: No description
    :param str updater: No description
    :param int xpoint: No description
    :param int ypoint: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element3dModel/insert'
        params = {
            'createtime': createtime,
            'creator': creator,
            'elementname': elementname,
            'elementtype': elementtype,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'rotationangle': rotationangle,
            'scale': scale,
            'suspendheight': suspendheight,
            'updatetime': updatetime,
            'updater': updater,
            'xpoint': xpoint,
            'ypoint': ypoint,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def element3dmodel_selectlist(self, access_token: str):
        """
        根据车场id和楼层id查询3D模型信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element3dModel/selectList'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def element3dmodel_update(self, access_token: str, createtime: str = '', creator: str = '', elementname: str = '', elementtype: int = '', floorid: int = '', id: int = '', lotid: int = '', rotationangle: str = '', scale: str = '', suspendheight: str = '', updatetime: str = '', updater: str = '', xpoint: int = '', ypoint: int = ''):
        """
        更新
        :param str createtime: No description
    :param str creator: No description
    :param str elementname: 元素名称
    :param int elementtype: 元素类型 1楼梯  2 直梯  3扶梯
    :param int floorid: 楼层id
    :param int id: id
    :param int lotid: 车场id
    :param str rotationangle: 模型的朝向设置（0~360），实时预览，默认为0
    :param str scale: 缩放比例，模型的大小控制（0.5-2），实时预览，默认为1
    :param str suspendheight: 离地高度，模型底面离地面上表面的距离（0-10.0），默认为0
    :param str updatetime: No description
    :param str updater: No description
    :param int xpoint: No description
    :param int ypoint: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/element3dModel/update'
        params = {
            'createtime': createtime,
            'creator': creator,
            'elementname': elementname,
            'elementtype': elementtype,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'rotationangle': rotationangle,
            'scale': scale,
            'suspendheight': suspendheight,
            'updatetime': updatetime,
            'updater': updater,
            'xpoint': xpoint,
            'ypoint': ypoint,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_deletebatchbyids(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/deleteBatchByIds'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_deletebyfloorid(self, access_token: str):
        """
        批量删除某个楼层数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/deleteByFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_exportbeaconexcel(self, access_token: str, floorid: int = '', id: int = '', lotid: int = '', major: str = '', minor: str = '', name: str = '', uuid: str = ''):
        """
        导出数据
        :param int floorid: 楼层id
    :param int id: 主键id
    :param int lotid: 车场id lot_info id
    :param str major: 蓝牙信标的major
    :param str minor: 蓝牙信标的minor
    :param str name: 名称
    :param str uuid: 蓝牙信标的uuid
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/exportBeaconExcel'
        params = {
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'major': major,
            'minor': minor,
            'name': name,
            'uuid': uuid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_getbeaconbylotid(self, access_token: str):
        """
        根据车场id查询蓝牙设备列表
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/getBeaconByLotId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_importcoordinatebyexcel(self, access_token: str, multipartfile: str = ''):
        """
        通过excel导入坐标
        :param str multipartfile: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/importCoordinateByExcel'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_importdatabyexcel(self, access_token: str, multipartfile: str = ''):
        """
        通过excel导入数据
        :param str multipartfile: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/importDataByExcel'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_importdatabylotid(self, access_token: str, multipartfile: str = ''):
        """
        导入蓝牙数据（全覆盖）
        :param str multipartfile: multipartFile
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/importDataByLotId'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_importpointcoordinatesbyexcel(self, access_token: str, multipartfile: str = ''):
        """
        通过excel导入点位坐标
        :param str multipartfile: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/importPointCoordinatesByExcel'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_insert(self, access_token: str, floorid: int = '', id: int = '', lotid: int = '', major: str = '', minor: str = '', name: str = '', uuid: str = '', xpoint: str = '', ypoint: str = ''):
        """
        添加
        :param int floorid: 楼层id
    :param int id: 主键id
    :param int lotid: 车场id lot_info id
    :param str major: 蓝牙信标的major
    :param str minor: 蓝牙信标的minor
    :param str name: 名称
    :param str uuid: 蓝牙信标的uuid
    :param str xpoint: No description
    :param str ypoint: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/insert'
        params = {
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'major': major,
            'minor': minor,
            'name': name,
            'uuid': uuid,
            'xpoint': xpoint,
            'ypoint': ypoint,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_insertbatch(self, access_token: str, multipartfile: str = ''):
        """
        批量保存蓝牙数据,文件为txt格式
        :param str multipartfile: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/insertBatch'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_selectbylotidandfloorid(self, access_token: str):
        """
        查询指定楼层所有的蓝牙信标
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/selectByLotIdAndFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_selectpagelist(self, access_token: str, floorenablestatus: int = '', floorid: int = '', id: int = '', isinput: bool = '', lotid: int = '', major: str = '', minor: str = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, uuid: str = ''):
        """
        分页查询
        :param int floorenablestatus: 楼层启用状态，状态 1启用 2停用
    :param int floorid: 楼层id
    :param int id: 主键id
    :param bool isinput: 蓝牙信标是否录入，true：已录入，false：未录入
    :param int lotid: 车场id lot_info id
    :param str major: 蓝牙信标的major
    :param str minor: 蓝牙信标的minor
    :param str name: 名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str uuid: 蓝牙信标的uuid
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/selectPageList'
        params = {
            'floorenablestatus': floorenablestatus,
            'floorid': floorid,
            'id': id,
            'isinput': isinput,
            'lotid': lotid,
            'major': major,
            'minor': minor,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'uuid': uuid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementbeacon_update(self, access_token: str, floorid: int = '', id: int = '', lotid: int = '', major: str = '', minor: str = '', name: str = '', uuid: str = '', xpoint: str = '', ypoint: str = ''):
        """
        更新
        :param int floorid: 楼层id
    :param int id: 主键id
    :param int lotid: 车场id lot_info id
    :param str major: 蓝牙信标的major
    :param str minor: 蓝牙信标的minor
    :param str name: 名称
    :param str uuid: 蓝牙信标的uuid
    :param str xpoint: No description
    :param str ypoint: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementBeacon/update'
        params = {
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'major': major,
            'minor': minor,
            'name': name,
            'uuid': uuid,
            'xpoint': xpoint,
            'ypoint': ypoint,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementimpassablepath_batchsave(self, access_token: str, floorid: int = '', lotid: int = '', pathlist: list = ''):
        """
        批量保存不可通行路网
        :param int floorid: 楼层id
    :param int lotid: 车场id
    :param list pathlist: 路网集合
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementImpassablePath/batchSave'
        params = {
            'floorid': floorid,
            'lotid': lotid,
            'pathlist': pathlist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementimpassablepath_deletebatchbyids(self, access_token: str, ids: str = ''):
        """
        批量删除
        :param str ids: ids
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementImpassablePath/deleteBatchByIds'
        params = {
            'ids': ids,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementimpassablepath_deletebyid(self, access_token: str):
        """
        删除不可通行路网数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementImpassablePath/deleteById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementimpassablepath_exportimpassablepath(self, access_token: str):
        """
        数据同步-导出
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementImpassablePath/exportImpassablePath'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementimpassablepath_getbylotidandfloorid(self, access_token: str):
        """
        获取指定楼层的不可通行路网数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementImpassablePath/getByLotIdAndFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementimpassablepath_importimpassablepath(self, access_token: str, multipartfile: str = ''):
        """
        数据同步-导入
        :param str multipartfile: 导入文件
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementImpassablePath/importImpassablePath'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementimpassablepath_save(self, access_token: str, floorid: int = '', lotid: int = '', pathlist: list = ''):
        """
        保存不可通行路网
        :param int floorid: 楼层id
    :param int lotid: 车场id
    :param list pathlist: 路网集合
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementImpassablePath/save'
        params = {
            'floorid': floorid,
            'lotid': lotid,
            'pathlist': pathlist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementimpassablepath_selectallbylotid(self, access_token: str):
        """
        获取车场所有不可通行路网数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementImpassablePath/selectALLByLotId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreenchild_getall(self, access_token: str):
        """
        获取所有子屏数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementScreenChild/getAll'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreenchild_getbyfloorid(self, access_token: str):
        """
        获取指定楼层的子屏
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementScreenChild/getByFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreenchild_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementScreenChild/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreenchild_getelementscreenchildcollection(self, access_token: str):
        """
        获取指定楼层整理后，子屏数据集合
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementScreenChild/getElementScreenChildCollection'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreenchild_listbyelementscreenid(self, access_token: str):
        """
        根据主屏Id获取子屏信息(用于选择框)
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementScreenChild/listByElementScreenId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreenchild_update(self, access_token: str, arrowdirection: int = '', arrowposition: int = '', constantnum: int = '', criticalnum: int = '', description: str = '', id: int = '', parktype: int = '', relationareaidlist: str = '', revisenum: int = '', screenaddr: int = '', screencategory: int = '', screenspecies: int = '', screentype: int = '', showcolor: int = '', showtype: int = ''):
        """
        更新
        :param int arrowdirection: 箭头方向   0：右   1：左   2：上   3：下
    :param int arrowposition: 箭头位置   0：右   1：左
    :param int constantnum: 固定显示数值
    :param int criticalnum: 临界值（小于临界值直接输出0）
    :param str description: 描述
    :param int id: 主键
    :param int parktype: 车位类型   0：正常、1：残障
    :param str relationareaidlist: 子屏关联区域id集合信息，以英文,分隔开
    :param int revisenum: 校正数值 （结果数值加上这个值）
    :param int screenaddr: 屏地址
    :param int screencategory: 屏类别   1：LED网络屏、  2：485总屏、3：485子屏
    :param int screenspecies: 屏种类 1：LED屏 2：LCD屏
    :param int screentype: 屏类型   1：普通屏、2：总屏
    :param int showcolor: 显示颜色   0：红   1：橙   2：绿   3：根据数值
    :param int showtype: 展示内容   1：关联车位空车位数、2：关联车位占用车位数、3：车场总空车位数、4：车位总占用车位数、5：固定显示数值 6：第三方屏控制 7：关联区域剩余车位数
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementScreenChild/update'
        params = {
            'arrowdirection': arrowdirection,
            'arrowposition': arrowposition,
            'constantnum': constantnum,
            'criticalnum': criticalnum,
            'description': description,
            'id': id,
            'parktype': parktype,
            'relationareaidlist': relationareaidlist,
            'revisenum': revisenum,
            'screenaddr': screenaddr,
            'screencategory': screencategory,
            'screenspecies': screenspecies,
            'screentype': screentype,
            'showcolor': showcolor,
            'showtype': showtype,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementscreenchild_updatebatch(self, access_token: str, vo: str = ''):
        """
        更新
        :param str vo: vo
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementScreenChild/updateBatch'
        params = {
            'vo': vo,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def elementscreenparkrelation_getparkidbyscreenid(self, access_token: str):
        """
        根据屏id获取对应的车位id
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementScreenParkRelation/getParkIdByScreenId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreenparkrelation_selectrelatepark(self, access_token: str):
        """
        查询可选车位和已选车位
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementScreenParkRelation/selectRelatePark'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def elementscreenparkrelation_update(self, access_token: str, parkidlist: list = '', screenid: int = ''):
        """
        更新
        :param list parkidlist: 车位id集合
    :param int screenid: 子屏id
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/elementScreenParkRelation/update'
        params = {
            'parkidlist': parkidlist,
            'screenid': screenid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def floorinfo_createflooruniqueidentification(self, access_token: str):
        """
        楼层唯一标识为空的生成唯一标识
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/floorInfo/createFloorUniqueIdentification'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def floorinfo_delete(self, access_token: str):
        """
        删除楼层
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/floorInfo/delete'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def floorinfo_flooruniquesynchronization(self, access_token: str, floorinfosynchronizationrequestvolist: str = ''):
        """
        云端和场端楼层唯一标识同步
        :param str floorinfosynchronizationrequestvolist: floorInfoSynchronizationRequestVOList
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/floorInfo/floorUniqueSynchronization'
        params = {
            'floorinfosynchronizationrequestvolist': floorinfosynchronizationrequestvolist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def floorinfo_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/floorInfo/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def floorinfo_insert(self, access_token: str, floorname: str = '', lotid: int = '', remark: str = '', sort: int = ''):
        """
        添加
        :param str floorname: 楼层名称
    :param int lotid: 车场id lot_info id
    :param str remark: 备注
    :param int sort: 楼层顺序（数字越大，楼层越高）
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/floorInfo/insert'
        params = {
            'floorname': floorname,
            'lotid': lotid,
            'remark': remark,
            'sort': sort,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def floorinfo_selectflooruniquebyother(self, access_token: str):
        """
        查询云端楼层唯一标识
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/floorInfo/selectFloorUniqueByOther'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def floorinfo_selectpagelist(self, access_token: str, endtime: str = '', floorname: str = '', flooruniqueidentification: str = '', id: int = '', lotid: int = '', pagenumber: int = 1, pagesize: int = 100, sort: int = '', starttime: str = '', status: int = ''):
        """
        分页查询
        :param str endtime: 开始时间
    :param str floorname: 楼层名称
    :param str flooruniqueidentification: 楼层唯一标识字段
    :param int id: 楼层id
    :param int lotid: 车场id
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int sort: 楼层顺序
    :param str starttime: 开始时间
    :param int status: 启用状态 1启用 2停用
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/floorInfo/selectPageList'
        params = {
            'endtime': endtime,
            'floorname': floorname,
            'flooruniqueidentification': flooruniqueidentification,
            'id': id,
            'lotid': lotid,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'sort': sort,
            'starttime': starttime,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def floorinfo_update(self, access_token: str, floorname: str = '', id: int = '', lotid: int = '', remark: str = '', sort: int = '', status: int = ''):
        """
        更新
        :param str floorname: 楼层名称
    :param int id: 楼层id
    :param int lotid: 场端楼层id
    :param str remark: 备注
    :param int sort: 楼层顺序（数字越大，楼层越高）
    :param int status: 状态 1启用 2停用
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/floorInfo/update'
        params = {
            'floorname': floorname,
            'id': id,
            'lotid': lotid,
            'remark': remark,
            'sort': sort,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def floorinfo_updatescrollratio(self, access_token: str, id: int = '', scrollratio: int = ''):
        """
        更新缩放比例
        :param int id: 楼层id
    :param int scrollratio: 缩放比例（%）
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/floorInfo/updateScrollRatio'
        params = {
            'id': id,
            'scrollratio': scrollratio,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def generalconfig_getall(self, access_token: str):
        """
        获取所有配置信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/generalConfig/getAll'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def generalconfig_getconfigbycode(self, access_token: str):
        """
        根据code获取配置
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/generalConfig/getConfigByCode'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def generalconfig_insert(self, access_token: str, configkey: str = '', configvalue: str = '', createtime: str = '', description: str = '', id: int = '', updatetime: str = ''):
        """
        新增配置信息
        :param str configkey: 字段唯一标识，禁止重复
    :param str configvalue: 字段具体配置信息
    :param str createtime: 创建时间
    :param str description: 字段详细作用描述
    :param int id: 主键id
    :param str updatetime: 更新时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/generalConfig/insert'
        params = {
            'configkey': configkey,
            'configvalue': configvalue,
            'createtime': createtime,
            'description': description,
            'id': id,
            'updatetime': updatetime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def generalconfig_updatebyid(self, access_token: str, configkey: str = '', configvalue: str = '', createtime: str = '', description: str = '', id: int = '', updatetime: str = ''):
        """
        根据ID修改对应配置
        :param str configkey: 字段唯一标识，禁止重复
    :param str configvalue: 字段具体配置信息
    :param str createtime: 创建时间
    :param str description: 字段详细作用描述
    :param int id: 主键id
    :param str updatetime: 更新时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/generalConfig/updateById'
        params = {
            'configkey': configkey,
            'configvalue': configvalue,
            'createtime': createtime,
            'description': description,
            'id': id,
            'updatetime': updatetime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def generalconfig_updateconfigbycode(self, access_token: str, configkey: str = '', configvalue: str = ''):
        """
        根据code修改配置
        :param str configkey: 配置key
    :param str configvalue: 配置value
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/generalConfig/updateConfigByCode'
        params = {
            'configkey': configkey,
            'configvalue': configvalue,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def ground_delete(self, access_token: str):
        """
        删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/ground/delete'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def ground_deletebyfloorid(self, access_token: str):
        """
        地面 - 删除某个楼层地面
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/ground/deleteByFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def ground_exportground(self, access_token: str):
        """
        数据同步-导出
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/ground/exportGround'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def ground_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/ground/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def ground_importground(self, access_token: str, multipartfile: str = ''):
        """
        数据同步-导入
        :param str multipartfile: 导入文件
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/ground/importGround'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def ground_selectpagelist(self, access_token: str, control: int = '', elementcustomid: int = '', floorenablestatus: int = '', floorid: int = '', floorname: str = '', floorstatus: int = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, parkaddr: int = '', parkcategory: int = '', parkno: str = '', status: int = '', type: int = '', uniqueidentificationfield: str = ''):
        """
        地面列表
        :param int control: 车位控制 0-自动控制 1-手动控制
    :param int elementcustomid: 自定义元素的主id
    :param int floorenablestatus: 楼层启用状态，状态 1启用 2停用 空为所有
    :param int floorid: 楼层Id
    :param str floorname: 楼层名称
    :param int floorstatus: 楼层启用状态：状态 1启用 2停用
    :param int id: id
    :param int lotid: 车场Id
    :param str name: 元素名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int parkaddr: 车位地址
    :param int parkcategory: 车位种类 1 为普通车位  2 为新能源车位  3 为立体车位
    :param str parkno: 车位编号
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param int type: 元素类型 元素类型详情见枚举1 地面  2 柱子  3 车位
    :param str uniqueidentificationfield: 车位唯一标识字段
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/ground/selectPageList'
        params = {
            'control': control,
            'elementcustomid': elementcustomid,
            'floorenablestatus': floorenablestatus,
            'floorid': floorid,
            'floorname': floorname,
            'floorstatus': floorstatus,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkaddr': parkaddr,
            'parkcategory': parkcategory,
            'parkno': parkno,
            'status': status,
            'type': type,
            'uniqueidentificationfield': uniqueidentificationfield,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def ground_update(self, access_token: str, chargingbrand: str = '', chargingtype: int = '', control: int = '', createtime: str = '', deleted: bool = '', devicetype: int = '', enable: int = '', floorid: int = '', id: int = '', lotid: int = '', name: str = '', parkaddr: int = '', parkcategory: int = '', parkno: str = '', parkinglockequipmentno: str = '', parkingpropertyright: str = '', status: int = '', stereoscopicparkcameraaddr: int = '', toward: int = '', type: int = '', updatetime: str = ''):
        """
        更新
        :param str chargingbrand: No description
    :param int chargingtype: No description
    :param int control: 车位控制 0-自动控制 1-手动控制
    :param str createtime: 创建时间
    :param bool deleted: 是否删除0未删除1已删除
    :param int devicetype: No description
    :param int enable: No description
    :param int floorid: 楼层id
    :param int id: 主键
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int parkaddr: 车位地址
    :param int parkcategory: 车位种类  1 为普通车位  2 为新能源车位  3 为立体车位
    :param str parkno: 车位编号
    :param str parkinglockequipmentno: No description
    :param str parkingpropertyright: No description
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param int stereoscopicparkcameraaddr: 立体车位对应的相机地址
    :param int toward: 方向朝向（0-360角度整数存值）
    :param int type: 元素类型详情见枚举
    :param str updatetime: 更新时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/ground/update'
        params = {
            'chargingbrand': chargingbrand,
            'chargingtype': chargingtype,
            'control': control,
            'createtime': createtime,
            'deleted': deleted,
            'devicetype': devicetype,
            'enable': enable,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'name': name,
            'parkaddr': parkaddr,
            'parkcategory': parkcategory,
            'parkno': parkno,
            'parkinglockequipmentno': parkinglockequipmentno,
            'parkingpropertyright': parkingpropertyright,
            'status': status,
            'stereoscopicparkcameraaddr': stereoscopicparkcameraaddr,
            'toward': toward,
            'type': type,
            'updatetime': updatetime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def ground_updategroundcoordinate(self, access_token: str, floorid: int = '', groundcontent: list = '', lotid: int = ''):
        """
        更新地面坐标信息
        :param int floorid: 楼层id
    :param list groundcontent: 坐标列表
    :param int lotid: 车场id
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/ground/updateGroundCoordinate'
        params = {
            'floorid': floorid,
            'groundcontent': groundcontent,
            'lotid': lotid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
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


    def imagestyles_insert(self, access_token: str, escalatorconnector: str = '', id: int = '', isshownameconnector: bool = '', isshownamemachine: bool = '', mapstylesid: int = '', norecordbeacon: str = '', passagewayconnector: str = '', recordbeacon: str = '', screenlcdurl: str = '', screenledurl: str = '', stairsconnector: str = '', verticalladderconnector: str = '', verticalmachine: str = '', wallmachine: str = ''):
        """
        添加
        :param str escalatorconnector: 扶梯图标url
    :param int id: 主键id
    :param bool isshownameconnector: 通行设施是否显示元素名称  0：不显示  1：显示
    :param bool isshownamemachine: 找车机是否显示元素名称  0：不显示  1：显示
    :param int mapstylesid: 地图样式id
    :param str norecordbeacon: 未录入蓝牙图标url
    :param str passagewayconnector: 出入口图标url
    :param str recordbeacon: 已录入蓝牙图标url
    :param str screenlcdurl: LCD屏图标URL
    :param str screenledurl: LED屏图标URL
    :param str stairsconnector: 楼梯图标url
    :param str verticalladderconnector: 直梯图标url
    :param str verticalmachine: 立式找车机图标url
    :param str wallmachine: 壁挂式找车机图标url
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/image-styles/insert'
        params = {
            'escalatorconnector': escalatorconnector,
            'id': id,
            'isshownameconnector': isshownameconnector,
            'isshownamemachine': isshownamemachine,
            'mapstylesid': mapstylesid,
            'norecordbeacon': norecordbeacon,
            'passagewayconnector': passagewayconnector,
            'recordbeacon': recordbeacon,
            'screenlcdurl': screenlcdurl,
            'screenledurl': screenledurl,
            'stairsconnector': stairsconnector,
            'verticalladderconnector': verticalladderconnector,
            'verticalmachine': verticalmachine,
            'wallmachine': wallmachine,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def imagestyles_update(self, access_token: str, escalatorconnector: str = '', id: int = '', isshownameconnector: bool = '', isshownamemachine: bool = '', mapstylesid: int = '', norecordbeacon: str = '', passagewayconnector: str = '', recordbeacon: str = '', screenlcdurl: str = '', screenledurl: str = '', stairsconnector: str = '', verticalladderconnector: str = '', verticalmachine: str = '', wallmachine: str = ''):
        """
        编辑
        :param str escalatorconnector: 扶梯图标url
    :param int id: 主键id
    :param bool isshownameconnector: 通行设施是否显示元素名称  0：不显示  1：显示
    :param bool isshownamemachine: 找车机是否显示元素名称  0：不显示  1：显示
    :param int mapstylesid: 地图样式id
    :param str norecordbeacon: 未录入蓝牙图标url
    :param str passagewayconnector: 出入口图标url
    :param str recordbeacon: 已录入蓝牙图标url
    :param str screenlcdurl: LCD屏图标URL
    :param str screenledurl: LED屏图标URL
    :param str stairsconnector: 楼梯图标url
    :param str verticalladderconnector: 直梯图标url
    :param str verticalmachine: 立式找车机图标url
    :param str wallmachine: 壁挂式找车机图标url
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/image-styles/update'
        params = {
            'escalatorconnector': escalatorconnector,
            'id': id,
            'isshownameconnector': isshownameconnector,
            'isshownamemachine': isshownamemachine,
            'mapstylesid': mapstylesid,
            'norecordbeacon': norecordbeacon,
            'passagewayconnector': passagewayconnector,
            'recordbeacon': recordbeacon,
            'screenlcdurl': screenlcdurl,
            'screenledurl': screenledurl,
            'stairsconnector': stairsconnector,
            'verticalladderconnector': verticalladderconnector,
            'verticalmachine': verticalmachine,
            'wallmachine': wallmachine,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def importolddata_machine(self, access_token: str, file: str = ''):
        """
        导入找车机数据
        :param str file: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/importOldData/machine'
        params = {
            'file': file,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def importolddata_screen(self, access_token: str, file: str = ''):
        """
        导入主屏数据
        :param str file: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/importOldData/screen'
        params = {
            'file': file,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def importolddata_screenchild(self, access_token: str, file: str = ''):
        """
        导入子屏数据
        :param str file: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/importOldData/screenChild'
        params = {
            'file': file,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def internationalization_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/internationalization/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def internationalization_insert(self, access_token: str, chinese: str = '', code: str = '', description: str = '', english: str = '', id: int = '', other1: str = '', other2: str = '', other3: str = '', other4: str = ''):
        """
        添加
        :param str chinese: 简体中文
    :param str code: 代码，前缀是front.的为前端，前缀是server.的为后端
    :param str description: 描述
    :param str english: 英文
    :param int id: 主键
    :param str other1: 其他语言1，预留字段
    :param str other2: 其他语言2，预留字段
    :param str other3: 其他语言3，预留字段
    :param str other4: 其他语言4，预留字段
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/internationalization/insert'
        params = {
            'chinese': chinese,
            'code': code,
            'description': description,
            'english': english,
            'id': id,
            'other1': other1,
            'other2': other2,
            'other3': other3,
            'other4': other4,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def internationalization_selectallfront(self, access_token: str):
        """
        获取属于前端的国际化数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/internationalization/selectAllFront'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def internationalization_selectpagelist(self, access_token: str, chinese: str = '', code: str = '', complete: bool = '', description: str = '', english: str = '', id: int = '', other1: str = '', other2: str = '', other3: str = '', other4: str = '', pagenumber: int = 1, pagesize: int = 100):
        """
        分页查询
        :param str chinese: 简体中文
    :param str code: 代码，前缀是front.的为前端，前缀是server.的为后端
    :param bool complete: 数据完整性， 1：完整  0：不完整
    :param str description: 描述
    :param str english: 英文
    :param int id: 主键
    :param str other1: 其他语言1，预留字段
    :param str other2: 其他语言2，预留字段
    :param str other3: 其他语言3，预留字段
    :param str other4: 其他语言4，预留字段
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/internationalization/selectPageList'
        params = {
            'chinese': chinese,
            'code': code,
            'complete': complete,
            'description': description,
            'english': english,
            'id': id,
            'other1': other1,
            'other2': other2,
            'other3': other3,
            'other4': other4,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def internationalization_update(self, access_token: str, chinese: str = '', code: str = '', description: str = '', english: str = '', id: int = '', other1: str = '', other2: str = '', other3: str = '', other4: str = ''):
        """
        更新
        :param str chinese: 简体中文
    :param str code: 代码，前缀是front.的为前端，前缀是server.的为后端
    :param str description: 描述
    :param str english: 英文
    :param int id: 主键
    :param str other1: 其他语言1，预留字段
    :param str other2: 其他语言2，预留字段
    :param str other3: 其他语言3，预留字段
    :param str other4: 其他语言4，预留字段
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/internationalization/update'
        params = {
            'chinese': chinese,
            'code': code,
            'description': description,
            'english': english,
            'id': id,
            'other1': other1,
            'other2': other2,
            'other3': other3,
            'other4': other4,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def internationalizationrelation_controlstatus(self, access_token: str):
        """
        启用/关闭语言
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/internationalizationRelation/controlStatus'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def internationalizationrelation_exportinternational(self, access_token: str):
        """
        国际化数据excel文件导出
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/internationalizationRelation/exportInternational'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def internationalizationrelation_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/internationalizationRelation/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def internationalizationrelation_selectall(self, access_token: str):
        """
        查询所有记录
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/internationalizationRelation/selectAll'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def internationalizationrelation_selectenable(self, access_token: str):
        """
        查询启用状态的语言
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/internationalizationRelation/selectEnable'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def internationalizationrelation_update(self, access_token: str, field: str = '', id: int = '', name: str = '', shorthand: str = '', sort: int = '', status: bool = ''):
        """
        更新
        :param str field: internationalization表的字段名
    :param int id: 主键id
    :param str name: 语言名称，用于显示在前端用于选择语言
    :param str shorthand: 语言简称，用于前端组件自带的国际化，如：zh_CN：简体中文  en_GB：英语
    :param int sort: 排序
    :param bool status: 状态  0：未启用   1：启用
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/internationalizationRelation/update'
        params = {
            'field': field,
            'id': id,
            'name': name,
            'shorthand': shorthand,
            'sort': sort,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lcdadvertisementconfig_batchdelete(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lcd-advertisement-config/batchDelete'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def lcdadvertisementconfig_insert(self, access_token: str, filename: str = '', lcdadvertisementschemeid: int = '', playsort: int = '', remark: str = ''):
        """
        添加
        :param str filename: 文件名
    :param int lcdadvertisementschemeid: LCD屏广告方案id
    :param int playsort: 播放顺序
    :param str remark: 备注
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lcd-advertisement-config/insert'
        params = {
            'filename': filename,
            'lcdadvertisementschemeid': lcdadvertisementschemeid,
            'playsort': playsort,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lcdadvertisementconfig_selectpagelist(self, access_token: str, lcdadvertisementschemeid: int = '', pagenumber: int = 1, pagesize: int = 100):
        """
        查看方案的广告配置
        :param int lcdadvertisementschemeid: 广告方案id
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lcd-advertisement-config/selectPageList'
        params = {
            'lcdadvertisementschemeid': lcdadvertisementschemeid,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lcdadvertisementconfig_update(self, access_token: str, filename: str = '', id: int = '', lcdadvertisementschemeid: int = '', playsort: int = '', remark: str = ''):
        """
        编辑
        :param str filename: 文件名
    :param int id: 主键id
    :param int lcdadvertisementschemeid: LCD屏广告方案id
    :param int playsort: 播放顺序
    :param str remark: 备注
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lcd-advertisement-config/update'
        params = {
            'filename': filename,
            'id': id,
            'lcdadvertisementschemeid': lcdadvertisementschemeid,
            'playsort': playsort,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lcdadvertisementscheme_batchdelete(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lcd-advertisement-scheme/batchDelete'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def lcdadvertisementscheme_insert(self, access_token: str, carouselseconds: int = '', name: str = '', species: int = ''):
        """
        添加
        :param int carouselseconds: 轮播时间 单位s(秒)
    :param str name: 方案名称
    :param int species: 类型 1：图片 2：视频
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lcd-advertisement-scheme/insert'
        params = {
            'carouselseconds': carouselseconds,
            'name': name,
            'species': species,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lcdadvertisementscheme_selectpagelist(self, access_token: str, endtime: str = '', id: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, species: int = '', starttime: str = ''):
        """
        分页查询
        :param str endtime: 结束时间
    :param int id: 主键id
    :param str name: 方案名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int species: 类型 1：图片 2：视频
    :param str starttime: 开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lcd-advertisement-scheme/selectPageList'
        params = {
            'endtime': endtime,
            'id': id,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'species': species,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lcdadvertisementscheme_update(self, access_token: str, carouselseconds: int = '', id: int = '', name: str = '', species: int = ''):
        """
        编辑
        :param int carouselseconds: 轮播时间 单位s(秒)
    :param int id: 主键id
    :param str name: 方案名称
    :param int species: 类型 1：图片 2：视频
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lcd-advertisement-scheme/update'
        params = {
            'carouselseconds': carouselseconds,
            'id': id,
            'name': name,
            'species': species,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lcdscreenconfig_exchangeorder(self, access_token: str):
        """
        对调屏顺序（目前只针对于双拼接屏）
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lcd-screen-config/exchangeOrder'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lcdscreenconfig_getall(self, access_token: str):
        """
        查询车场所有屏信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lcd-screen-config/getAll'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def lcdscreenconfig_noticetest(self, access_token: str):
        """
        全场屏指令下发测试接口
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lcd-screen-config/noticeTest'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def lightschemecontroller_cancel(self, access_token: str):
        """
        取消车位灯方案
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lightSchemeController/cancel'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def lightschemecontroller_copy(self, access_token: str, id: int = ''):
        """
        复制车位灯方案
        :param int id: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lightSchemeController/copy'
        params = {
            'id': id,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lightschemecontroller_insert(self, access_token: str, elementparkids: list = '', freecolor: int = '', issuancetype: int = '', lightaddr: int = '', lightschemenname: str = '', lighttype: int = '', occupycolor: int = '', sendtime: str = '', systemtype: int = '', warningcolor: int = ''):
        """
        新增车位灯方案
        :param list elementparkids: 关联车位id集合
    :param int freecolor: 空闲颜色
    :param int issuancetype: 下发类型 0：修改车位的车位灯方案 1：修改设备的车位灯方案
    :param int lightaddr: 车位灯地址
    :param str lightschemenname: 方案名称
    :param int lighttype: 灯类型   1-有线多彩灯  2-有线双色灯
    :param int occupycolor: 占用颜色
    :param str sendtime: 生效时间
    :param int systemtype: 设备类型  0-DSP车位相机   1-NODE节点控制器
    :param int warningcolor: 告警颜色
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lightSchemeController/insert'
        params = {
            'elementparkids': elementparkids,
            'freecolor': freecolor,
            'issuancetype': issuancetype,
            'lightaddr': lightaddr,
            'lightschemenname': lightschemenname,
            'lighttype': lighttype,
            'occupycolor': occupycolor,
            'sendtime': sendtime,
            'systemtype': systemtype,
            'warningcolor': warningcolor,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lightschemecontroller_selectpagelist(self, access_token: str, endcreatetime: str = '', endsendtime: str = '', id: int = '', lightaddr: int = '', lighttype: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, parkno: str = '', startcreatetime: str = '', startsendtime: str = '', status: int = '', systemtype: int = ''):
        """
        车位灯方案下发记录
        :param str endcreatetime: 创建时间-结束时间
    :param str endsendtime: 生效时间-结束时间
    :param int id: ID
    :param int lightaddr: 车位灯地址
    :param int lighttype: 灯类型   1-有线多彩灯  2-有线双色灯
    :param str name: 方案名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位编号
    :param str startcreatetime: 创建时间-开始时间
    :param str startsendtime: 生效时间-开始时间
    :param int status: 下发状态  1-未生效  2-下发成功  3-下发失败  4-取消
    :param int systemtype: 系统类型  0-引导   1-找车  2-引导和找车
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lightSchemeController/selectPageList'
        params = {
            'endcreatetime': endcreatetime,
            'endsendtime': endsendtime,
            'id': id,
            'lightaddr': lightaddr,
            'lighttype': lighttype,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkno': parkno,
            'startcreatetime': startcreatetime,
            'startsendtime': startsendtime,
            'status': status,
            'systemtype': systemtype,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lightschemecontroller_update(self, access_token: str, elementparkids: list = '', freecolor: int = '', issuancetype: int = '', lightaddr: int = '', lightschemenname: str = '', lighttype: int = '', occupycolor: int = '', sendtime: str = '', systemtype: int = '', warningcolor: int = ''):
        """
        更新车位灯方案
        :param list elementparkids: 关联车位id集合
    :param int freecolor: 空闲颜色
    :param int issuancetype: 下发类型 0：修改车位的车位灯方案 1：修改设备的车位灯方案
    :param int lightaddr: 车位灯地址
    :param str lightschemenname: 方案名称
    :param int lighttype: 灯类型   1-有线多彩灯  2-有线双色灯
    :param int occupycolor: 占用颜色
    :param str sendtime: 生效时间
    :param int systemtype: 设备类型  0-DSP车位相机   1-NODE节点控制器
    :param int warningcolor: 告警颜色
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lightSchemeController/update'
        params = {
            'elementparkids': elementparkids,
            'freecolor': freecolor,
            'issuancetype': issuancetype,
            'lightaddr': lightaddr,
            'lightschemenname': lightschemenname,
            'lighttype': lighttype,
            'occupycolor': occupycolor,
            'sendtime': sendtime,
            'systemtype': systemtype,
            'warningcolor': warningcolor,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lightschemegroup_deletebatch(self, access_token: str, idlist: str = ''):
        """
        批量删除
        :param str idlist: idList
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lightSchemeGroup/deleteBatch'
        params = {
            'idlist': idlist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lightschemegroup_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lightSchemeGroup/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def lightschemegroup_insert(self, access_token: str, cameraip: str = '', detectordevicetype: int = '', detectordsp: int = '', detectorip: str = '', detectornodedsp: int = '', devicetype: int = '', freecolor: int = '', groupname: str = '', id: int = '', lightaddr: int = '', lighttype: int = '', occupycolor: int = ''):
        """
        添加
        :param str cameraip: 车位相机ip
    :param int detectordevicetype: 超声波设备类型  1-TCP  2-485
    :param int detectordsp: 超声波探测器拨码
    :param str detectorip: 超声波探测器ip
    :param int detectornodedsp: 超声波节点拨码
    :param int devicetype: 设备类型  0-车位相机灯  1-超声波探测器灯
    :param int freecolor: 空闲颜色
    :param str groupname: 分组名称
    :param int id: 主键
    :param int lightaddr: 车位灯地址（转化后）
    :param int lighttype: 车位灯类型 1-有线多彩灯 2-有线双色灯
    :param int occupycolor: 占用颜色
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lightSchemeGroup/insert'
        params = {
            'cameraip': cameraip,
            'detectordevicetype': detectordevicetype,
            'detectordsp': detectordsp,
            'detectorip': detectorip,
            'detectornodedsp': detectornodedsp,
            'devicetype': devicetype,
            'freecolor': freecolor,
            'groupname': groupname,
            'id': id,
            'lightaddr': lightaddr,
            'lighttype': lighttype,
            'occupycolor': occupycolor,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lightschemegroup_selectpagelist(self, access_token: str, endtime: str = '', groupname: str = '', lightaddr: int = '', pagenumber: int = 1, pagesize: int = 100, starttime: str = ''):
        """
        分页查询
        :param str endtime: 创建时间-结束时间
    :param str groupname: 分组名称
    :param int lightaddr: 车位灯地址
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str starttime: 创建时间-开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lightSchemeGroup/selectPageList'
        params = {
            'endtime': endtime,
            'groupname': groupname,
            'lightaddr': lightaddr,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lightschemegroup_selectrelatepark(self, access_token: str):
        """
        查询可选车位和已选车位
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lightSchemeGroup/selectRelatePark'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def lightschemegroup_update(self, access_token: str, cameraip: str = '', detectordevicetype: int = '', detectordsp: int = '', detectorip: str = '', detectornodedsp: int = '', devicetype: int = '', freecolor: int = '', groupname: str = '', id: int = '', lightaddr: int = '', lighttype: int = '', occupycolor: int = ''):
        """
        更新
        :param str cameraip: 车位相机ip
    :param int detectordevicetype: 超声波设备类型  1-TCP  2-485
    :param int detectordsp: 超声波探测器拨码
    :param str detectorip: 超声波探测器ip
    :param int detectornodedsp: 超声波节点拨码
    :param int devicetype: 设备类型  0-车位相机灯  1-超声波探测器灯
    :param int freecolor: 空闲颜色
    :param str groupname: 分组名称
    :param int id: 主键
    :param int lightaddr: 车位灯地址（转化后）
    :param int lighttype: 车位灯类型 1-有线多彩灯 2-有线双色灯
    :param int occupycolor: 占用颜色
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lightSchemeGroup/update'
        params = {
            'cameraip': cameraip,
            'detectordevicetype': detectordevicetype,
            'detectordsp': detectordsp,
            'detectorip': detectorip,
            'detectornodedsp': detectornodedsp,
            'devicetype': devicetype,
            'freecolor': freecolor,
            'groupname': groupname,
            'id': id,
            'lightaddr': lightaddr,
            'lighttype': lighttype,
            'occupycolor': occupycolor,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lightschemegroup_updateparkrelate(self, access_token: str, lightschemegroupid: int = '', parkidlist: list = ''):
        """
        更新车位关联信息
        :param int lightschemegroupid: 分组车位灯方案id
    :param list parkidlist: 车位id集合
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lightSchemeGroup/updateParkRelate'
        params = {
            'lightschemegroupid': lightschemegroupid,
            'parkidlist': parkidlist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def loginlog_selectpagelist(self, access_token: str, endtime: str = '', loginip: str = '', pagenumber: int = 1, pagesize: int = 100, starttime: str = '', useraccount: str = '', username: str = '', userphone: str = ''):
        """
        分页查询
        :param str endtime: 结束时间
    :param str loginip: 登陆ip
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str starttime: 开始时间
    :param str useraccount: 用户账号
    :param str username: 用户名
    :param str userphone: 用户电话
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/login-log/selectPageList'
        params = {
            'endtime': endtime,
            'loginip': loginip,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'starttime': starttime,
            'useraccount': useraccount,
            'username': username,
            'userphone': userphone,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lotinfo_deletebatch(self, access_token: str):
        """
        多车场 - 删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lot-info/deleteBatch'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def lotinfo_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lot-info/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def lotinfo_getmsg(self, access_token: str):
        """
        获取车场信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lot-info/getMsg'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def lotinfo_insert(self, access_token: str, addr: str = '', decodingstatus: int = '', deviceid: str = '', deviceipprefix: str = '', id: int = '', lisenceauthorizecode: str = '', lisencetrialperiod: str = '', lotcode: str = '', lotname: str = '', machinedebug: int = '', maptype: int = '', parkrepeatswitch: int = '', secret: str = '', serverip: str = '', systemtype: int = '', tel: str = ''):
        """
        多车场 - 保存
        :param str addr: 车场地址
    :param int decodingstatus: Lisence解码是否异常，0：正常  1：异常
    :param str deviceid: 场端deviceId
    :param str deviceipprefix: 设备IP网段前缀
    :param int id: 主键
    :param str lisenceauthorizecode: Lisence授权码
    :param str lisencetrialperiod: Lisence首次默认30天试用期(寻车服务首次启动时，开始生效)，到期时间
    :param str lotcode: 车场编码
    :param str lotname: 车场名称
    :param int machinedebug: 找车机地图是否开启调试模式 0 关闭 1 开启
    :param int maptype: 地图类型 0:2D地图 1:3D地图
    :param int parkrepeatswitch: 车位编号限制 0:不允许重复的车位编号  1:允许重复车位编号
    :param str secret: 密钥（接口加密使用）
    :param str serverip: 服务器IP
    :param int systemtype: C++端部署形式  1:引导系统  2:找车系统  3:引导系统和找车系统同时部署
    :param str tel: 联系电话
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lot-info/insert'
        params = {
            'addr': addr,
            'decodingstatus': decodingstatus,
            'deviceid': deviceid,
            'deviceipprefix': deviceipprefix,
            'id': id,
            'lisenceauthorizecode': lisenceauthorizecode,
            'lisencetrialperiod': lisencetrialperiod,
            'lotcode': lotcode,
            'lotname': lotname,
            'machinedebug': machinedebug,
            'maptype': maptype,
            'parkrepeatswitch': parkrepeatswitch,
            'secret': secret,
            'serverip': serverip,
            'systemtype': systemtype,
            'tel': tel,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lotinfo_lotinfocheck(self, access_token: str):
        """
        车场配置检测
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lot-info/lotInfoCheck'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def lotinfo_save(self, access_token: str, addr: str = '', deviceipprefix: str = '', id: int = '', lotcode: str = '', lotname: str = '', maptype: int = '', parkrepeatswitch: int = '', serverip: str = '', systemtype: int = '', tel: str = ''):
        """
        保存
        :param str addr: 车场地址
    :param str deviceipprefix: 设备IP网段前缀
    :param int id: 楼层id
    :param str lotcode: 车场编码
    :param str lotname: 车场名称
    :param int maptype: 地图类型 0:2D地图 1:3D地图
    :param int parkrepeatswitch: 车位编号限制 0:不允许重复的车位编号  1:允许重复车位编号
    :param str serverip: 服务器IP
    :param int systemtype: C++端部署形式  1:引导系统  2:找车系统  3:引导系统和找车系统同时部署
    :param str tel: 联系电话
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lot-info/save'
        params = {
            'addr': addr,
            'deviceipprefix': deviceipprefix,
            'id': id,
            'lotcode': lotcode,
            'lotname': lotname,
            'maptype': maptype,
            'parkrepeatswitch': parkrepeatswitch,
            'serverip': serverip,
            'systemtype': systemtype,
            'tel': tel,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lotinfo_selectlist(self, access_token: str, createenddatetime: str = '', createstartdatetime: str = '', lotcode: int = '', lotname: str = '', pagenumber: int = 1, pagesize: int = 100, status: int = ''):
        """
        多车场 - 分页查询
        :param str createenddatetime: 创建时间结束时间
    :param str createstartdatetime: 创建时间开始时间
    :param int lotcode: 车场编码
    :param str lotname: 车场名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int status: 启用状态 0 未启用  1 启用
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lot-info/selectList'
        params = {
            'createenddatetime': createenddatetime,
            'createstartdatetime': createstartdatetime,
            'lotcode': lotcode,
            'lotname': lotname,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lotinfo_update(self, access_token: str, addr: str = '', decodingstatus: int = '', deviceid: str = '', deviceipprefix: str = '', id: int = '', lisenceauthorizecode: str = '', lisencetrialperiod: str = '', lotcode: str = '', lotname: str = '', machinedebug: int = '', maptype: int = '', parkrepeatswitch: int = '', secret: str = '', serverip: str = '', systemtype: int = '', tel: str = ''):
        """
        多车场 - 更新
        :param str addr: 车场地址
    :param int decodingstatus: Lisence解码是否异常，0：正常  1：异常
    :param str deviceid: 场端deviceId
    :param str deviceipprefix: 设备IP网段前缀
    :param int id: 主键
    :param str lisenceauthorizecode: Lisence授权码
    :param str lisencetrialperiod: Lisence首次默认30天试用期(寻车服务首次启动时，开始生效)，到期时间
    :param str lotcode: 车场编码
    :param str lotname: 车场名称
    :param int machinedebug: 找车机地图是否开启调试模式 0 关闭 1 开启
    :param int maptype: 地图类型 0:2D地图 1:3D地图
    :param int parkrepeatswitch: 车位编号限制 0:不允许重复的车位编号  1:允许重复车位编号
    :param str secret: 密钥（接口加密使用）
    :param str serverip: 服务器IP
    :param int systemtype: C++端部署形式  1:引导系统  2:找车系统  3:引导系统和找车系统同时部署
    :param str tel: 联系电话
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lot-info/update'
        params = {
            'addr': addr,
            'decodingstatus': decodingstatus,
            'deviceid': deviceid,
            'deviceipprefix': deviceipprefix,
            'id': id,
            'lisenceauthorizecode': lisenceauthorizecode,
            'lisencetrialperiod': lisencetrialperiod,
            'lotcode': lotcode,
            'lotname': lotname,
            'machinedebug': machinedebug,
            'maptype': maptype,
            'parkrepeatswitch': parkrepeatswitch,
            'secret': secret,
            'serverip': serverip,
            'systemtype': systemtype,
            'tel': tel,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def lotinfo_updateauthorizecode(self, access_token: str):
        """
        更新当前车场授权码(返回true为保存成功，返回false为保存失败)
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/lot-info/updateAuthorizeCode'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def machineadvertisementconfig_batchdelete(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/machine-advertisement-config/batchDelete'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def machineadvertisementconfig_savemachineadvertisementconfig(self, access_token: str, id: int = '', machineadschemeid: int = '', machineip: str = '', screenadschemeid: int = '', type: int = ''):
        """
        保存
        :param int id: 主键id
    :param int machineadschemeid: 找车机广告方案id
    :param str machineip: 找车机ip
    :param int screenadschemeid: 广告屏广告方案id
    :param int type: 类型 0-全局 1-单独配置
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/machine-advertisement-config/saveMachineAdvertisementConfig'
        params = {
            'id': id,
            'machineadschemeid': machineadschemeid,
            'machineip': machineip,
            'screenadschemeid': screenadschemeid,
            'type': type,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def machineadvertisementconfig_selectpagelist(self, access_token: str, machineadschemeid: int = '', machineip: str = '', pagenumber: int = 1, pagesize: int = 100, screenadschemeid: int = '', type: int = ''):
        """
        分页查询
        :param int machineadschemeid: 找车机广告方案id
    :param str machineip: 找车机ip
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int screenadschemeid: 广告屏广告方案id
    :param int type: 类型 0-全局 1-单独配置
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/machine-advertisement-config/selectPageList'
        params = {
            'machineadschemeid': machineadschemeid,
            'machineip': machineip,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'screenadschemeid': screenadschemeid,
            'type': type,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def mapstyles_batchdelete(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/map-styles/batchDelete'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def mapstyles_batchdisable(self, access_token: str):
        """
        批量禁用、启用
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/map-styles/batchDisable'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def mapstyles_copy(self, access_token: str):
        """
        复制
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/map-styles/copy'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def mapstyles_exporttotxt(self, access_token: str):
        """
        导出文本格式的数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/map-styles/exportToTxt'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def mapstyles_generatemapstylefile(self, access_token: str):
        """
        生成地图样式json文件到指定目录
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/map-styles/generateMapStyleFile'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def mapstyles_getmapstylesdetail(self, access_token: str):
        """
        根据mystyleId获取地图样式的详细信息，当id为null返回默认样式
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/map-styles/getMapStylesDetail'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def mapstyles_importbytxt(self, access_token: str, multipartfile: str = ''):
        """
        通过文本导入数据
        :param str multipartfile: multipartFile
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/map-styles/importByTxt'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def mapstyles_insert(self, access_token: str, lotid: int = '', name: str = '', remark: str = ''):
        """
        添加
        :param int lotid: 车场id
    :param str name: 样式名称
    :param str remark: 备注
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/map-styles/insert'
        params = {
            'lotid': lotid,
            'name': name,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def mapstyles_selectisshowcontrol(self, access_token: str):
        """
        找车机 - 控制是否显示名称
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/map-styles/selectIsShowControl'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def mapstyles_selectpagelist(self, access_token: str, deleted: bool = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, remark: str = ''):
        """
        分页查询
        :param bool deleted: 是否禁用（0：禁用，1：启用）
    :param int id: 主键id
    :param int lotid: 车场编码
    :param str name: 样式名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str remark: 备注
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/map-styles/selectPageList'
        params = {
            'deleted': deleted,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def mapstyles_update(self, access_token: str, id: int = '', name: str = '', remark: str = ''):
        """
        编辑
        :param int id: 主键id
    :param str name: 样式名称
    :param str remark: 备注
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/map-styles/update'
        params = {
            'id': id,
            'name': name,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def mapinfo_backupmap(self, access_token: str):
        """
        场端地图备份
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/mapInfo/backupMap'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def mapinfo_exportmap(self, access_token: str):
        """
        场端地图数据导出（云端导入用）
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/mapInfo/exportMap'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def mapinfo_exportmapdata(self, access_token: str):
        """
        场端地图导出
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/mapInfo/exportMapData'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def mapinfo_getallfloordata(self, access_token: str):
        """
        场端管理后台实时获取地图数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/mapInfo/getAllFloorData'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def mapinfo_getmachineallfloordata(self, access_token: str):
        """
        找车机获取地图数据（优先内存获取,对外提供参数用lotCode）
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/mapInfo/getMachineAllFloorData'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def mapinfo_refreshmapdata(self, access_token: str):
        """
        刷新地图数据到内存（提供给找车机）
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/mapInfo/refreshMapData'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def mapinfo_restoremap(self, access_token: str, multipartfile: str = ''):
        """
        场端地图数据还原
        :param str multipartfile: multipartFile
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/mapInfo/restoreMap'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def nodedevice_deletebatch(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/nodeDevice/deleteBatch'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def nodedevice_deletebyfloorid(self, access_token: str):
        """
        节点设备 - 清空列表数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/nodeDevice/deleteByFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def nodedevice_importdatabyexcel(self, access_token: str, multipartfile: str = ''):
        """
        通过excel导入数据
        :param str multipartfile: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/nodeDevice/importDataByExcel'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def nodedevice_save(self, access_token: str, addr: str = '', devicetype: int = '', floorid: int = '', id: str = '', relateparknum: int = '', remark: str = ''):
        """
        新增
        :param str addr: 设备ip转化后的数字，用于与设备建立连接
    :param int devicetype: 设备类型
    :param int floorid: 楼层id
    :param str id: id
    :param int relateparknum: 关联车位数
    :param str remark: 备注
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/nodeDevice/save'
        params = {
            'addr': addr,
            'devicetype': devicetype,
            'floorid': floorid,
            'id': id,
            'relateparknum': relateparknum,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def nodedevice_selectpagelist(self, access_token: str, addr: int = '', devicetype: int = '', endtime: str = '', floorid: int = '', id: int = '', lotid: int = '', pagenumber: int = 1, pagesize: int = 100, starttime: str = '', status: int = ''):
        """
        节点设备管理 - 分页查询
        :param int addr: 节点设备地址
    :param int devicetype: 节点设备类型
    :param str endtime: 结束时间
    :param int floorid: 楼层id
    :param int id: No description
    :param int lotid: 车场id
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str starttime: 开始时间
    :param int status: 节点设备状态
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/nodeDevice/selectPageList'
        params = {
            'addr': addr,
            'devicetype': devicetype,
            'endtime': endtime,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'starttime': starttime,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def nodedevice_update(self, access_token: str, addr: str = '', devicetype: int = '', floorid: int = '', id: str = '', relateparknum: int = '', remark: str = ''):
        """
        修改
        :param str addr: 设备ip转化后的数字，用于与设备建立连接
    :param int devicetype: 设备类型
    :param int floorid: 楼层id
    :param str id: id
    :param int relateparknum: 关联车位数
    :param str remark: 备注
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/nodeDevice/update'
        params = {
            'addr': addr,
            'devicetype': devicetype,
            'floorid': floorid,
            'id': id,
            'relateparknum': relateparknum,
            'remark': remark,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def overnight_export(self, access_token: str, areaidlist: list = '', flooridlist: list = '', pagenumber: int = 1, pagesize: int = 100, parkno: str = '', recordendtime: str = '', recordstarttime: str = ''):
        """
        过夜车数据导出
        :param list areaidlist: 区域ID集合
    :param list flooridlist: 楼层ID集合
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位编号
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/overnight/export'
        params = {
            'areaidlist': areaidlist,
            'flooridlist': flooridlist,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkno': parkno,
            'recordendtime': recordendtime,
            'recordstarttime': recordstarttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def overnight_getdatabyarea(self, access_token: str, areaidlist: list = '', recordendtime: str = '', recordstarttime: str = ''):
        """
        按照区域分组查询
        :param list areaidlist: 区域ID集合
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/overnight/getDataByArea'
        params = {
            'areaidlist': areaidlist,
            'recordendtime': recordendtime,
            'recordstarttime': recordstarttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def overnight_getdatabyfloor(self, access_token: str, recordendtime: str = '', recordstarttime: str = ''):
        """
        按照楼层分组查询
        :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/overnight/getDataByFloor'
        params = {
            'recordendtime': recordendtime,
            'recordstarttime': recordstarttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def overnight_selectpagelist(self, access_token: str, areaidlist: list = '', flooridlist: list = '', pagenumber: int = 1, pagesize: int = 100, parkno: str = '', recordendtime: str = '', recordstarttime: str = ''):
        """
        分页查询过夜车数据
        :param list areaidlist: 区域ID集合
    :param list flooridlist: 楼层ID集合
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位编号
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/overnight/selectPageList'
        params = {
            'areaidlist': areaidlist,
            'flooridlist': flooridlist,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkno': parkno,
            'recordendtime': recordendtime,
            'recordstarttime': recordstarttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_addbatchpark(self, access_token: str, floorid: int = '', lotid: int = '', parkcontent: list = ''):
        """
        批量新增车位
        :param int floorid: No description
    :param int lotid: No description
    :param list parkcontent: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/addBatchPark'
        params = {
            'floorid': floorid,
            'lotid': lotid,
            'parkcontent': parkcontent,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_createparkuniqueidentification(self, access_token: str):
        """
        车位唯一标识为空的生成唯一标识
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/createParkUniqueIdentification'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_delete(self, access_token: str):
        """
        删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/delete'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_deletebyfloorid(self, access_token: str):
        """
        删除楼层全部车位信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/deleteByFloorId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_deletepresentcarandupdatestatus(self, access_token: str):
        """
        清除当前车位的车辆信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/deletePresentCarAndUpdateStatus'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_exportdatasynchronization(self, access_token: str):
        """
        数据同步-导出
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/exportDataSynchronization'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_exportparkinglot(self, access_token: str, control: int = '', elementcustomid: int = '', floorenablestatus: int = '', floorid: int = '', floorname: str = '', floorstatus: int = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, parkaddr: int = '', parkcategory: int = '', parkno: str = '', status: int = '', type: int = '', uniqueidentificationfield: str = ''):
        """
        车位数据excel文件导出
        :param int control: 车位控制 0-自动控制 1-手动控制
    :param int elementcustomid: 自定义元素的主id
    :param int floorenablestatus: 楼层启用状态，状态 1启用 2停用 空为所有
    :param int floorid: 楼层Id
    :param str floorname: 楼层名称
    :param int floorstatus: 楼层启用状态：状态 1启用 2停用
    :param int id: id
    :param int lotid: 车场Id
    :param str name: 元素名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int parkaddr: 车位地址
    :param int parkcategory: 车位种类 1 为普通车位  2 为新能源车位  3 为立体车位
    :param str parkno: 车位编号
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param int type: 元素类型 元素类型详情见枚举1 地面  2 柱子  3 车位
    :param str uniqueidentificationfield: 车位唯一标识字段
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/exportParkingLot'
        params = {
            'control': control,
            'elementcustomid': elementcustomid,
            'floorenablestatus': floorenablestatus,
            'floorid': floorid,
            'floorname': floorname,
            'floorstatus': floorstatus,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkaddr': parkaddr,
            'parkcategory': parkcategory,
            'parkno': parkno,
            'status': status,
            'type': type,
            'uniqueidentificationfield': uniqueidentificationfield,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_getallparkinfo(self, access_token: str):
        """
        获取车位-楼层-区域信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/getAllParkInfo'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_getallparkinfowithoutstereoscopic(self, access_token: str):
        """
        获取所有车位数据(过滤已绑定立体车位)
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/getAllParkInfoWithOutStereoscopic'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_getelementparkandpresentcarinfo(self, access_token: str):
        """
        得到车位和当前车辆的信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/getElementParkAndPresentCarInfo'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_getparkinfo(self, access_token: str):
        """
        根据车位编号查询车位信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/getParkInfo'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_getparktotalusagerate(self, access_token: str):
        """
        大屏-车场总泊位使用率
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/getParkTotalUsageRate'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_getparkingcapture(self, access_token: str):
        """
        根据车位地址查询车位相机抓拍内容
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/getParkingCapture'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_importdatasynchronization(self, access_token: str, multipartfile: str = ''):
        """
        数据同步-导入
        :param str multipartfile: 导入文件
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/importDataSynchronization'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_importparkinglot(self, access_token: str, multipartfile: str = ''):
        """
        车位数据excel文件导入
        :param str multipartfile: 导入文件
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/importParkingLot'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_initpostparkingspaceinfo(self, access_token: str):
        """
        initPostParkingSpaceInfo
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/initPostParkingSpaceInfo'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_listelementpark(self, access_token: str, chargingbrand: str = '', chargingtype: int = '', control: int = '', createtime: str = '', deleted: bool = '', devicetype: int = '', enable: int = '', floorid: int = '', id: int = '', lotid: int = '', name: str = '', parkaddr: int = '', parkcategory: int = '', parkno: str = '', parkinglockequipmentno: str = '', parkingpropertyright: str = '', status: int = '', stereoscopicparkcameraaddr: int = '', toward: int = '', type: int = '', updatetime: str = ''):
        """
        大屏-得到车位信息集合
        :param str chargingbrand: No description
    :param int chargingtype: No description
    :param int control: 车位控制 0-自动控制 1-手动控制
    :param str createtime: 创建时间
    :param bool deleted: 是否删除0未删除1已删除
    :param int devicetype: No description
    :param int enable: No description
    :param int floorid: 楼层id
    :param int id: 主键
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int parkaddr: 车位地址
    :param int parkcategory: 车位种类  1 为普通车位  2 为新能源车位  3 为立体车位
    :param str parkno: 车位编号
    :param str parkinglockequipmentno: No description
    :param str parkingpropertyright: No description
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param int stereoscopicparkcameraaddr: 立体车位对应的相机地址
    :param int toward: 方向朝向（0-360角度整数存值）
    :param int type: 元素类型详情见枚举
    :param str updatetime: 更新时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/listElementPark'
        params = {
            'chargingbrand': chargingbrand,
            'chargingtype': chargingtype,
            'control': control,
            'createtime': createtime,
            'deleted': deleted,
            'devicetype': devicetype,
            'enable': enable,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'name': name,
            'parkaddr': parkaddr,
            'parkcategory': parkcategory,
            'parkno': parkno,
            'parkinglockequipmentno': parkinglockequipmentno,
            'parkingpropertyright': parkingpropertyright,
            'status': status,
            'stereoscopicparkcameraaddr': stereoscopicparkcameraaddr,
            'toward': toward,
            'type': type,
            'updatetime': updatetime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_listelementparkusagerate(self, access_token: str):
        """
        大屏-车位占用率集合
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/listElementParkUsageRate'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_movepark(self, access_token: str, id: int = '', pointdtos: list = ''):
        """
        2D地图编辑 - 移动车位
        :param int id: 车位id
    :param list pointdtos: 移动后新的车位坐标
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/movePark'
        params = {
            'id': id,
            'pointdtos': pointdtos,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_parkrelatearea(self, access_token: str, areaid: int = '', relateparkids: list = '', unrelateparkids: list = ''):
        """
        车位关联 - 取消关联区域
        :param int areaid: No description
    :param list relateparkids: No description
    :param list unrelateparkids: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/parkRelateArea'
        params = {
            'areaid': areaid,
            'relateparkids': relateparkids,
            'unrelateparkids': unrelateparkids,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_pushparkcamera(self, access_token: str):
        """
        车位相机照片抓拍指令下发
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


    def park_selectfaultpark(self, access_token: str):
        """
        查询故障的车位id
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/selectFaultPark'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_selectofflinepark(self, access_token: str):
        """
        查询掉线的车位
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/selectOffLinePark'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_selectpagelist(self, access_token: str, control: int = '', elementcustomid: int = '', floorenablestatus: int = '', floorid: int = '', floorname: str = '', floorstatus: int = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, parkaddr: int = '', parkcategory: int = '', parkno: str = '', status: int = '', type: int = '', uniqueidentificationfield: str = ''):
        """
        车位元素列表
        :param int control: 车位控制 0-自动控制 1-手动控制
    :param int elementcustomid: 自定义元素的主id
    :param int floorenablestatus: 楼层启用状态，状态 1启用 2停用 空为所有
    :param int floorid: 楼层Id
    :param str floorname: 楼层名称
    :param int floorstatus: 楼层启用状态：状态 1启用 2停用
    :param int id: id
    :param int lotid: 车场Id
    :param str name: 元素名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int parkaddr: 车位地址
    :param int parkcategory: 车位种类 1 为普通车位  2 为新能源车位  3 为立体车位
    :param str parkno: 车位编号
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param int type: 元素类型 元素类型详情见枚举1 地面  2 柱子  3 车位
    :param str uniqueidentificationfield: 车位唯一标识字段
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/selectPageList'
        params = {
            'control': control,
            'elementcustomid': elementcustomid,
            'floorenablestatus': floorenablestatus,
            'floorid': floorid,
            'floorname': floorname,
            'floorstatus': floorstatus,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkaddr': parkaddr,
            'parkcategory': parkcategory,
            'parkno': parkno,
            'status': status,
            'type': type,
            'uniqueidentificationfield': uniqueidentificationfield,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_selectpagetidylist(self, access_token: str, control: int = '', elementcustomid: int = '', floorenablestatus: int = '', floorid: int = '', floorname: str = '', floorstatus: int = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, parkaddr: int = '', parkcategory: int = '', parkno: str = '', status: int = '', type: int = '', uniqueidentificationfield: str = ''):
        """
        下拉列表联动前模糊分页查询
        :param int control: 车位控制 0-自动控制 1-手动控制
    :param int elementcustomid: 自定义元素的主id
    :param int floorenablestatus: 楼层启用状态，状态 1启用 2停用 空为所有
    :param int floorid: 楼层Id
    :param str floorname: 楼层名称
    :param int floorstatus: 楼层启用状态：状态 1启用 2停用
    :param int id: id
    :param int lotid: 车场Id
    :param str name: 元素名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int parkaddr: 车位地址
    :param int parkcategory: 车位种类 1 为普通车位  2 为新能源车位  3 为立体车位
    :param str parkno: 车位编号
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param int type: 元素类型 元素类型详情见枚举1 地面  2 柱子  3 车位
    :param str uniqueidentificationfield: 车位唯一标识字段
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/selectPageTidyList'
        params = {
            'control': control,
            'elementcustomid': elementcustomid,
            'floorenablestatus': floorenablestatus,
            'floorid': floorid,
            'floorname': floorname,
            'floorstatus': floorstatus,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkaddr': parkaddr,
            'parkcategory': parkcategory,
            'parkno': parkno,
            'status': status,
            'type': type,
            'uniqueidentificationfield': uniqueidentificationfield,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_selectwarningpark(self, access_token: str):
        """
        查询正在告警的车位id
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/selectWarningPark'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def park_synchronousparkaddr(self, access_token: str):
        """
        同步相机上报车位信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/synchronousParkAddr'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
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


    def park_update(self, access_token: str, chargingbrand: str = '', chargingtype: int = '', control: int = '', createtime: str = '', deleted: bool = '', devicetype: int = '', enable: int = '', floorid: int = '', id: int = '', lotid: int = '', name: str = '', parkaddr: int = '', parkcategory: int = '', parkno: str = '', parkinglockequipmentno: str = '', parkingpropertyright: str = '', status: int = '', stereoscopicparkcameraaddr: int = '', toward: int = '', type: int = '', updatetime: str = ''):
        """
        更新
        :param str chargingbrand: No description
    :param int chargingtype: No description
    :param int control: 车位控制 0-自动控制 1-手动控制
    :param str createtime: 创建时间
    :param bool deleted: 是否删除0未删除1已删除
    :param int devicetype: No description
    :param int enable: No description
    :param int floorid: 楼层id
    :param int id: 主键
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int parkaddr: 车位地址
    :param int parkcategory: 车位种类  1 为普通车位  2 为新能源车位  3 为立体车位
    :param str parkno: 车位编号
    :param str parkinglockequipmentno: No description
    :param str parkingpropertyright: No description
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param int stereoscopicparkcameraaddr: 立体车位对应的相机地址
    :param int toward: 方向朝向（0-360角度整数存值）
    :param int type: 元素类型详情见枚举
    :param str updatetime: 更新时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/update'
        params = {
            'chargingbrand': chargingbrand,
            'chargingtype': chargingtype,
            'control': control,
            'createtime': createtime,
            'deleted': deleted,
            'devicetype': devicetype,
            'enable': enable,
            'floorid': floorid,
            'id': id,
            'lotid': lotid,
            'name': name,
            'parkaddr': parkaddr,
            'parkcategory': parkcategory,
            'parkno': parkno,
            'parkinglockequipmentno': parkinglockequipmentno,
            'parkingpropertyright': parkingpropertyright,
            'status': status,
            'stereoscopicparkcameraaddr': stereoscopicparkcameraaddr,
            'toward': toward,
            'type': type,
            'updatetime': updatetime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_updatebatch(self, access_token: str, params: str = ''):
        """
        根据id批量更新车位编号/车位地址
        :param str params: params
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/updateBatch'
        params = {
            'params': params,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_updateelementparkcontrolandstatus(self, access_token: str, areaid: int = '', control: int = '', floorid: int = '', id: int = '', intime: str = '', lotid: int = '', parkaddr: int = '', plateno: str = '', presentcarrecordid: int = '', status: int = ''):
        """
        更新车位控制状态
        :param int areaid: 区域Id
    :param int control: 车位控制 0-自动控制 1-手动控制
    :param int floorid: 楼层id
    :param int id: 车位信息表主键id
    :param str intime: 进车时间
    :param int lotid: 车场Id
    :param int parkaddr: 车位地址
    :param str plateno: 车牌号码
    :param int presentcarrecordid: 在场车辆停车记录id
    :param int status: 车位状态 0-空闲 1-占用 2-故障 3-停止服务
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/updateElementParkControlAndStatus'
        params = {
            'areaid': areaid,
            'control': control,
            'floorid': floorid,
            'id': id,
            'intime': intime,
            'lotid': lotid,
            'parkaddr': parkaddr,
            'plateno': plateno,
            'presentcarrecordid': presentcarrecordid,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_updatepark(self, access_token: str, areaid: int = '', id: int = '', parkcategory: int = '', parkno: str = ''):
        """
        车场大屏-修改车位信息
        :param int areaid: No description
    :param int id: No description
    :param int parkcategory: No description
    :param str parkno: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/updatePark'
        params = {
            'areaid': areaid,
            'id': id,
            'parkcategory': parkcategory,
            'parkno': parkno,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def park_updateparkingcapture(self, access_token: str):
        """
        清理车位相机抓拍内容
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/park/updateParkingCapture'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def parkconfig_syncparkconfig(self, access_token: str, file: str = ''):
        """
        旧版寻车厂配置转换新版寻车配置
        :param str file: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/parkConfig/syncParkConfig'
        params = {
            'file': file,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def parkinglightscheme_batchdelete(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/parking-light-scheme/batchDelete'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def parkinglightscheme_insert(self, access_token: str, freecolor: int = '', lighttype: int = '', lotid: int = '', name: str = '', occupycolor: int = '', parkinglightarearelationlist: list = '', type: int = '', warningcolor: int = ''):
        """
        添加
        :param int freecolor: 空闲颜色
    :param int lighttype: 灯类型 1-有线多彩灯  2-有线双色灯
    :param int lotid: 车场id
    :param str name: 名称
    :param int occupycolor: 占用颜色
    :param list parkinglightarearelationlist: 车位灯方案和区域的关系列表
    :param int type: 设备类型  0-DSP车位相机   1-NODE节点控制器
    :param int warningcolor: 告警颜色
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/parking-light-scheme/insert'
        params = {
            'freecolor': freecolor,
            'lighttype': lighttype,
            'lotid': lotid,
            'name': name,
            'occupycolor': occupycolor,
            'parkinglightarearelationlist': parkinglightarearelationlist,
            'type': type,
            'warningcolor': warningcolor,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def parkinglightscheme_listrelatedarea(self, access_token: str):
        """
        关联区域集合
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/parking-light-scheme/listRelatedArea'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def parkinglightscheme_selectpagelist(self, access_token: str, endtime: str = '', id: int = '', lotid: int = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, parkinglightarearelationlist: list = '', starttime: str = ''):
        """
        分页查询
        :param str endtime: 结束时间
    :param int id: id
    :param int lotid: 车场id
    :param str name: 名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param list parkinglightarearelationlist: 车位灯方案和区域的关系列表
    :param str starttime: 开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/parking-light-scheme/selectPageList'
        params = {
            'endtime': endtime,
            'id': id,
            'lotid': lotid,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkinglightarearelationlist': parkinglightarearelationlist,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def parkinglightscheme_update(self, access_token: str, freecolor: int = '', id: int = '', lighttype: int = '', lotid: int = '', name: str = '', occupycolor: int = '', parkinglightarearelationlist: list = '', type: int = '', warningcolor: int = ''):
        """
        编辑
        :param int freecolor: 空闲颜色
    :param int id: id
    :param int lighttype: 灯类型 1-有线多彩灯  2-有线双色灯
    :param int lotid: 车场id
    :param str name: 名称
    :param int occupycolor: 占用颜色
    :param list parkinglightarearelationlist: 车位灯方案和区域的关系列表
    :param int type: 设备类型  0-DSP车位相机   1-NODE节点控制器
    :param int warningcolor: 告警颜色
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/parking-light-scheme/update'
        params = {
            'freecolor': freecolor,
            'id': id,
            'lighttype': lighttype,
            'lotid': lotid,
            'name': name,
            'occupycolor': occupycolor,
            'parkinglightarearelationlist': parkinglightarearelationlist,
            'type': type,
            'warningcolor': warningcolor,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def permissions_disable(self, access_token: str):
        """
        关闭菜单
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/permissions/disable'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def permissions_enable(self, access_token: str):
        """
        打开菜单
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/permissions/enable'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def permissions_insert(self, access_token: str, icon: str = '', id: int = '', internationalizationcode: str = '', linkway: int = '', menutype: int = '', name: str = '', router: str = '', sort: int = '', status: int = ''):
        """
        添加
        :param str icon: 图标
    :param int id: 主键
    :param str internationalizationcode: 值
    :param int linkway: 跳转方式(0:站内跳转，1:站外跳转)
    :param int menutype: 菜单类型(0:内部链接，1:外部链接)
    :param str name: 菜单名称
    :param str router: 路由
    :param int sort: 排序
    :param int status: 显示开关
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/permissions/insert'
        params = {
            'icon': icon,
            'id': id,
            'internationalizationcode': internationalizationcode,
            'linkway': linkway,
            'menutype': menutype,
            'name': name,
            'router': router,
            'sort': sort,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def permissions_insertchildmenu(self, access_token: str, id: int = '', internationalizationcode: str = '', linkway: int = '', menutype: int = '', name: str = '', parentid: int = '', router: str = '', sort: int = '', status: int = ''):
        """
        新增子菜单
        :param int id: id
    :param str internationalizationcode: 值
    :param int linkway: 跳转方式(0:站内跳转，1:站外跳转)
    :param int menutype: 菜单类型(0:内部链接，1:外部链接)
    :param str name: 菜单名称
    :param int parentid: 上级菜单
    :param str router: 链接
    :param int sort: 排序
    :param int status: 状态 开1，关0
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/permissions/insertChildMenu'
        params = {
            'id': id,
            'internationalizationcode': internationalizationcode,
            'linkway': linkway,
            'menutype': menutype,
            'name': name,
            'parentid': parentid,
            'router': router,
            'sort': sort,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def permissions_querypermission(self, access_token: str, name: str = '', router: str = ''):
        """
        条件查询
        :param str name: No description
    :param str router: No description
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/permissions/queryPermission'
        params = {
            'name': name,
            'router': router,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def permissions_selectenablemenu(self, access_token: str):
        """
        查询所有开启的菜单
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/permissions/selectEnableMenu'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def permissions_selectlist(self, access_token: str):
        """
        查询
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/permissions/selectList'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def permissions_update(self, access_token: str, icon: str = '', id: int = '', internationalizationcode: str = '', linkway: int = '', menutype: int = '', name: str = '', router: str = '', sort: int = '', status: int = ''):
        """
        更新
        :param str icon: 图标
    :param int id: 主键
    :param str internationalizationcode: 值
    :param int linkway: 跳转方式(0:站内跳转，1:站外跳转)
    :param int menutype: 菜单类型(0:内部链接，1:外部链接)
    :param str name: 菜单名称
    :param str router: 路由
    :param int sort: 排序
    :param int status: 显示开关
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/permissions/update'
        params = {
            'icon': icon,
            'id': id,
            'internationalizationcode': internationalizationcode,
            'linkway': linkway,
            'menutype': menutype,
            'name': name,
            'router': router,
            'sort': sort,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def permissions_updatechildmenu(self, access_token: str, id: int = '', internationalizationcode: str = '', linkway: int = '', menutype: int = '', name: str = '', parentid: int = '', router: str = '', sort: int = '', status: int = ''):
        """
        修改子菜单
        :param int id: id
    :param str internationalizationcode: 值
    :param int linkway: 跳转方式(0:站内跳转，1:站外跳转)
    :param int menutype: 菜单类型(0:内部链接，1:外部链接)
    :param str name: 菜单名称
    :param int parentid: 上级菜单
    :param str router: 链接
    :param int sort: 排序
    :param int status: 状态 开1，关0
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/permissions/updateChildMenu'
        params = {
            'id': id,
            'internationalizationcode': internationalizationcode,
            'linkway': linkway,
            'menutype': menutype,
            'name': name,
            'parentid': parentid,
            'router': router,
            'sort': sort,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def presentcarplaterecord_listpresentcarplatebyid(self, access_token: str):
        """
        在场车辆车牌记录列表
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/present-car-plate-record/listPresentCarPlateById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def presentcarrecord_export(self, access_token: str, areaname: str = '', elementparkcontrol: int = '', floorid: int = '', inendtime: str = '', instarttime: str = '', intype: int = '', lotid: int = '', pagenumber: int = 1, pagesize: int = 100, parkaddr: str = '', parkno: str = '', parkstatus: int = '', plateno: str = '', specialdata: int = ''):
        """
        实时车位报表 - excel文件导出
        :param str areaname: 区域名称
    :param int elementparkcontrol: 车位控制状态 默认为空查全部，下拉选择： 0 自动控制、1 手动控制
    :param int floorid: 楼层id
    :param str inendtime: 进车结束时间
    :param str instarttime: 进车开始时间
    :param int intype: 操作类型 0-系统进车 1-手动进车
    :param int lotid: 车场id
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkaddr: 车位地址
    :param str parkno: 车位号
    :param int parkstatus: 车位状态
    :param str plateno: 车牌号
    :param int specialdata: 特殊数据筛选查询，默认为空查全部，下拉选择：1:编号重复车位（查询系统内楼层-区域-编号重复的车位）；2:地址重复车位（查询系统车位地址重复的车位）；3:车牌识别失败车位（系统进车，占用状态但车牌为空）
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/present-car-record/export'
        params = {
            'areaname': areaname,
            'elementparkcontrol': elementparkcontrol,
            'floorid': floorid,
            'inendtime': inendtime,
            'instarttime': instarttime,
            'intype': intype,
            'lotid': lotid,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkaddr': parkaddr,
            'parkno': parkno,
            'parkstatus': parkstatus,
            'plateno': plateno,
            'specialdata': specialdata,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def presentcarrecord_listpresentcar(self, access_token: str, areaname: str = '', elementparkcontrol: int = '', floorid: int = '', inendtime: str = '', instarttime: str = '', intype: int = '', lotid: int = '', pagenumber: int = 1, pagesize: int = 100, parkaddr: str = '', parkno: str = '', parkstatus: int = '', plateno: str = '', specialdata: int = ''):
        """
        大屏-最新进车记录查询
        :param str areaname: 区域名称
    :param int elementparkcontrol: 车位控制状态 默认为空查全部，下拉选择： 0 自动控制、1 手动控制
    :param int floorid: 楼层id
    :param str inendtime: 进车结束时间
    :param str instarttime: 进车开始时间
    :param int intype: 操作类型 0-系统进车 1-手动进车
    :param int lotid: 车场id
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkaddr: 车位地址
    :param str parkno: 车位号
    :param int parkstatus: 车位状态
    :param str plateno: 车牌号
    :param int specialdata: 特殊数据筛选查询，默认为空查全部，下拉选择：1:编号重复车位（查询系统内楼层-区域-编号重复的车位）；2:地址重复车位（查询系统车位地址重复的车位）；3:车牌识别失败车位（系统进车，占用状态但车牌为空）
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/present-car-record/listPresentCar'
        params = {
            'areaname': areaname,
            'elementparkcontrol': elementparkcontrol,
            'floorid': floorid,
            'inendtime': inendtime,
            'instarttime': instarttime,
            'intype': intype,
            'lotid': lotid,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkaddr': parkaddr,
            'parkno': parkno,
            'parkstatus': parkstatus,
            'plateno': plateno,
            'specialdata': specialdata,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def presentcarrecord_selectpagelist(self, access_token: str, areaname: str = '', elementparkcontrol: int = '', floorid: int = '', inendtime: str = '', instarttime: str = '', intype: int = '', lotid: int = '', pagenumber: int = 1, pagesize: int = 100, parkaddr: str = '', parkno: str = '', parkstatus: int = '', plateno: str = '', specialdata: int = ''):
        """
        分页查询 - 实时车位报表
        :param str areaname: 区域名称
    :param int elementparkcontrol: 车位控制状态 默认为空查全部，下拉选择： 0 自动控制、1 手动控制
    :param int floorid: 楼层id
    :param str inendtime: 进车结束时间
    :param str instarttime: 进车开始时间
    :param int intype: 操作类型 0-系统进车 1-手动进车
    :param int lotid: 车场id
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkaddr: 车位地址
    :param str parkno: 车位号
    :param int parkstatus: 车位状态
    :param str plateno: 车牌号
    :param int specialdata: 特殊数据筛选查询，默认为空查全部，下拉选择：1:编号重复车位（查询系统内楼层-区域-编号重复的车位）；2:地址重复车位（查询系统车位地址重复的车位）；3:车牌识别失败车位（系统进车，占用状态但车牌为空）
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/present-car-record/selectPageList'
        params = {
            'areaname': areaname,
            'elementparkcontrol': elementparkcontrol,
            'floorid': floorid,
            'inendtime': inendtime,
            'instarttime': instarttime,
            'intype': intype,
            'lotid': lotid,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkaddr': parkaddr,
            'parkno': parkno,
            'parkstatus': parkstatus,
            'plateno': plateno,
            'specialdata': specialdata,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def presentcarrecordarea_selectpagelist(self, access_token: str, areaname: str = '', endtime: str = '', floorid: int = '', id: int = '', pagenumber: int = 1, pagesize: int = 100, plateno: str = '', starttime: str = ''):
        """
        分页查询
        :param str areaname: 区域名称
    :param str endtime: 结束时间
    :param int floorid: 楼层id
    :param int id: 主键
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str plateno: 车牌号
    :param str starttime: 开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/presentCarRecordArea/selectPageList'
        params = {
            'areaname': areaname,
            'endtime': endtime,
            'floorid': floorid,
            'id': id,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'plateno': plateno,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def role_deletesoftinids(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/role/deleteSoftInIds'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def role_disable(self, access_token: str):
        """
        禁用
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/role/disable'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def role_enable(self, access_token: str):
        """
        启用
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/role/enable'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def role_getall(self, access_token: str):
        """
        查询所有记录
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/role/getAll'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def role_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/role/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def role_insert(self, access_token: str, description: str = '', id: int = '', name: str = ''):
        """
        添加
        :param str description: 备注
    :param int id: 主键
    :param str name: 角色名称
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/role/insert'
        params = {
            'description': description,
            'id': id,
            'name': name,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def role_update(self, access_token: str, description: str = '', id: int = '', name: str = ''):
        """
        更新
        :param str description: 备注
    :param int id: 主键
    :param str name: 角色名称
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/role/update'
        params = {
            'description': description,
            'id': id,
            'name': name,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def rolepermissionrelation_setpermissions(self, access_token: str, menuidlist: list = '', roleid: int = ''):
        """
        设置权限
        :param list menuidlist: 菜单id集合
    :param int roleid: 角色id
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/rolePermissionRelation/setPermissions'
        params = {
            'menuidlist': menuidlist,
            'roleid': roleid,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def schedule_getconfig(self, access_token: str):
        """
        参数配置 - 查询
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/schedule/getConfig'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def schedule_parkinitreport(self, access_token: str):
        """
        车位状态初始化上报
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/schedule/parkInitReport'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def schedule_saveconfig(self, access_token: str, areaparkimgduration: int = '', areapushswitch: int = '', cleanareapicture: int = '', cleanrecognitiontable: int = '', cleanstereoscopicparkduration: int = '', cleantemppicture: int = '', emptyparkpushlot: str = '', emptyparkpushswitch: int = '', emptyparkpushurl: str = '', freespacenumswitch: int = '', lightschemeduration: int = '', parkchangepushlot: str = '', parkchangepushswitch: int = '', parkchangepushurl: str = '', parkimgduration: int = '', platematchrule: int = '', postbaseinfo: list = '', postbusinout: int = '', postnodedevicestatus: int = '', postnodedeviceurl: str = '', queryrecognizerecord: int = '', tankwarnpushswitch: int = ''):
        """
        参数配置 - 保存
        :param int areaparkimgduration: 区域在场车辆定时清理(天)
    :param int areapushswitch: 区域进出车上报开关 0:开启  1:关闭
    :param int cleanareapicture: 区域照片文件定时清理（单位：天）
    :param int cleanrecognitiontable: 车牌识别日志表定时清理（单位：天）
    :param int cleanstereoscopicparkduration: 清理立体车位的车牌识别记录(天)
    :param int cleantemppicture: 清理n天以前的临时识别文件
    :param str emptyparkpushlot: 空车位上报车场id，逗号,隔开
    :param int emptyparkpushswitch: 空车位上报，0开启，1关闭
    :param str emptyparkpushurl: 空车位上报url,多个;隔开
    :param int freespacenumswitch: 实时剩余车位数本地文件对接开关，0开启，1关闭
    :param int lightschemeduration: 车位灯方案下发定时清理(天)
    :param str parkchangepushlot: 车位状态变更上报车场id，逗号,隔开
    :param int parkchangepushswitch: 车位状态变更上报，0开启，1关闭
    :param str parkchangepushurl: 车位状态变更上报url,多个;隔开
    :param int parkimgduration: 车位照片定时清理（天）
    :param int platematchrule: 车牌匹配规则（0 【完全匹配】只返回除汉字部分完全一致的车牌）;1 【全匹配】 查2222可能返回12222或22221
    :param list postbaseinfo: 标准上报接口配置(车位进出车、区域进出车、油车告警 这个三个标准上报接口)
    :param int postbusinout: 上报出入车 0:开启  1:关闭
    :param int postnodedevicestatus: 节点设备状态变更上报 0:开启  1:关闭
    :param str postnodedeviceurl: 节点设备状态变更上报url  多个url直接用英语逗号隔开
    :param int queryrecognizerecord: 是否查询识别记录 0:开启  1:关闭（开启查询识别记录，关闭查询实时在场车）
    :param int tankwarnpushswitch: 油车告警上报开关 0:开启  1:关闭
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/schedule/saveConfig'
        params = {
            'areaparkimgduration': areaparkimgduration,
            'areapushswitch': areapushswitch,
            'cleanareapicture': cleanareapicture,
            'cleanrecognitiontable': cleanrecognitiontable,
            'cleanstereoscopicparkduration': cleanstereoscopicparkduration,
            'cleantemppicture': cleantemppicture,
            'emptyparkpushlot': emptyparkpushlot,
            'emptyparkpushswitch': emptyparkpushswitch,
            'emptyparkpushurl': emptyparkpushurl,
            'freespacenumswitch': freespacenumswitch,
            'lightschemeduration': lightschemeduration,
            'parkchangepushlot': parkchangepushlot,
            'parkchangepushswitch': parkchangepushswitch,
            'parkchangepushurl': parkchangepushurl,
            'parkimgduration': parkimgduration,
            'platematchrule': platematchrule,
            'postbaseinfo': postbaseinfo,
            'postbusinout': postbusinout,
            'postnodedevicestatus': postnodedevicestatus,
            'postnodedeviceurl': postnodedeviceurl,
            'queryrecognizerecord': queryrecognizerecord,
            'tankwarnpushswitch': tankwarnpushswitch,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def serverlog_downloadlog(self, access_token: str):
        """
        下载日志
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/server-log/downloadLog'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def serverlog_refreshserverlog(self, access_token: str):
        """
        刷新服务日志
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/server-log/refreshServerLog'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def serverlog_selectpagelist(self, access_token: str, endtime: str = '', filename: str = '', logtime: str = '', pagenumber: int = 1, pagesize: int = 100, starttime: str = ''):
        """
        分页查询
        :param str endtime: 结束时间
    :param str filename: 文件名
    :param str logtime: 日志时间
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str starttime: 开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/server-log/selectPageList'
        params = {
            'endtime': endtime,
            'filename': filename,
            'logtime': logtime,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def sync_convertcoordinate(self, access_token: str, multipartfile: str = ''):
        """
        上传excel，返回转化后的坐标
        :param str multipartfile: multipartFile
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/sync/convertCoordinate'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def sync_downloadtemplate(self, access_token: str):
        """
        下载excel模板
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/sync/downloadTemplate'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def sync_test(self, access_token: str, list: str = ''):
        """
        转换坐标 南昌用
        :param str list: list
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/sync/test'
        params = {
            'list': list,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def sync_test1(self, access_token: str):
        """
        转换坐标 鄱阳湖 顺时针90度
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/sync/test1'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def sync_uploadmessage(self, access_token: str, multipartfile: str = ''):
        """
        上传excel，把excel里的数据更新到对应车位
        :param str multipartfile: multipartFile
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/sync/uploadMessage'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def taskmanage_resetall(self, access_token: str):
        """
        重新加载所有定时任务
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


    def tool_checkunifiedinterstatus(self, access_token: str):
        """
        检查统一接口链接状态；1为连通
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/checkUnifiedInterStatus'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_clearareaenterparkrecord(self, access_token: str):
        """
        清除区域进出车记录
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/clearAreaEnterParkRecord'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_clearareapicture(self, access_token: str):
        """
        区域照片清理定时接口
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/clearAreaPicture'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_clearlightschemehistoryrecord(self, access_token: str):
        """
        清除车位灯方案记录
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/clearLightSchemeHistoryRecord'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_clearparkimg(self, access_token: str):
        """
        清除车位图片
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/clearParkImg'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_getcarinout(self, access_token: str):
        """
        进出车流量接口测试
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/getCarInOut'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_getfindcarmachinelist(self, access_token: str):
        """
        获取找车机设备状态信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/getFindCarMachineList'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_getovernight(self, access_token: str):
        """
        过夜车数据统计接口测试
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/getOvernight'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_getsign(self, access_token: str):
        """
        获取单车场接口签名
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/getSign'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_getts(self, access_token: str):
        """
        获取当前时间戳
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/getTS'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_pushallversioninfo(self, access_token: str):
        """
        寻车各个服务版本信息上传redis
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/pushAllVersionInfo'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_pushlotinfo(self, access_token: str):
        """
        上传车场基本信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/pushLotInfo'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_rebootdevice(self, access_token: str):
        """
        找车机设备（找车机程序会下发指令给主板）重启指令下发
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/rebootDevice'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_rebootmachine(self, access_token: str):
        """
        找车机程序重启指令下发
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/rebootMachine'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_refreshserverlog(self, access_token: str):
        """
        刷新运行日志
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/refreshServerLog'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_syncstereoscopicareahistory(self, access_token: str):
        """
        同步立体车位区域关联车位历史数据
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/syncStereoscopicAreaHistory'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_tableorganization(self, access_token: str):
        """
        表整理以及归档
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/tableOrganization'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def tool_uploadmachineinfo(self, access_token: str):
        """
        uploadMachineInfo
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/tool/uploadMachineInfo'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def upload_awsenableswitch(self, access_token: str):
        """
        是否上传车场问题图片到ai中心 0:开启  1:关闭
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/awsEnableSwitch'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def upload_channelswaggerswitch(self, access_token: str):
        """
        channel_service服务swagger配置开关 0:开启  1:关闭
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/channelSwaggerSwitch'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def upload_chunkupload(self, access_token: str):
        """
        广告-视频上传
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/chunkUpload'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def upload_downloadstylec(self, access_token: str):
        """
        下载识别文件
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/downloadStyleC'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def upload_getconfig(self, access_token: str):
        """
        获取系统参数配置信息
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/getConfig'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def upload_guidanceswaggerswitch(self, access_token: str):
        """
        parking_guidance服务swagger配置开关 0:开启  1:关闭
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/guidanceSwaggerSwitch'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def upload_replacelib(self, access_token: str, multipartfile: str = ''):
        """
        替换识别库
        :param str multipartfile: multipartFile
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/replaceLib'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def upload_uploadad(self, access_token: str, file: str = ''):
        """
        广告-图片上传
        :param str file: 文件
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/uploadAd'
        params = {
            'file': file,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def upload_uploadfloorcapture(self, access_token: str, floorcapture: str = ''):
        """
        上传楼层底图截图照片
        :param str floorcapture: 楼层截图照片
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/uploadFloorCapture'
        params = {
            'floorcapture': floorcapture,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def upload_uploadicon(self, access_token: str, iconimage: str = ''):
        """
        上传图标
        :param str iconimage: 文件
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/uploadIcon'
        params = {
            'iconimage': iconimage,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def upload_uploadimagemap(self, access_token: str, imagemap: str = ''):
        """
        上传找车机路线指引图片
        :param str imagemap: 指引图片
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/uploadImageMap'
        params = {
            'imagemap': imagemap,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def upload_uploadimgaws(self, access_token: str):
        """
        AWS上传车牌识别异常图片 - 手动触发接口
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/uploadImgAws'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def upload_uploadrouteqr(self, access_token: str, file: str = ''):
        """
        上传找车路线二维码图片
        :param str file: 文件
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/uploadRouteQr'
        params = {
            'file': file,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def upload_uploadstylec(self, access_token: str, multipartfile: str = ''):
        """
        上传识别文件
        :param str multipartfile: multipartFile
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/upload/uploadStyleC'
        params = {
            'multipartfile': multipartfile,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def user_changepassword(self, access_token: str, id: int = '', newpassword: str = '', oldpassword: str = ''):
        """
        修改密码
        :param int id: 主键
    :param str newpassword: 新密码
    :param str oldpassword: 旧密码
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/user/changePassword'
        params = {
            'id': id,
            'newpassword': newpassword,
            'oldpassword': oldpassword,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def user_deletesoftinids(self, access_token: str):
        """
        批量逻辑删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/user/deleteSoftInIds'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def user_getbyid(self, access_token: str):
        """
        根据主键获取详情
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/user/getById'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def user_insert(self, access_token: str, account: str = '', id: int = '', name: str = '', password: str = '', phone: str = '', remark: str = '', roleid: int = '', status: bool = ''):
        """
        添加
        :param str account: 账号
    :param int id: 主键id
    :param str name: 用户名
    :param str password: 密码
    :param str phone: 联系电话
    :param str remark: 备注
    :param int roleid: 角色id
    :param bool status: 状态 1 启用  0 禁用
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/user/insert'
        params = {
            'account': account,
            'id': id,
            'name': name,
            'password': password,
            'phone': phone,
            'remark': remark,
            'roleid': roleid,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def user_resetpassword(self, access_token: str, id: int = '', password: str = ''):
        """
        重置密码
        :param int id: 主键
    :param str password: 密码
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/user/resetPassword'
        params = {
            'id': id,
            'password': password,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def user_selectpagelist(self, access_token: str, account: str = '', endtime: str = '', name: str = '', pagenumber: int = 1, pagesize: int = 100, phone: str = '', remark: str = '', roleid: int = '', starttime: str = '', status: bool = ''):
        """
        分页查询
        :param str account: 账号
    :param str endtime: 结束时间
    :param str name: 用户名
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str phone: 手机号
    :param str remark: 备注
    :param int roleid: 角色id
    :param str starttime: 开始时间
    :param bool status: 状态 0禁用 1启用
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/user/selectPageList'
        params = {
            'account': account,
            'endtime': endtime,
            'name': name,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'phone': phone,
            'remark': remark,
            'roleid': roleid,
            'starttime': starttime,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def user_update(self, access_token: str, account: str = '', id: int = '', name: str = '', password: str = '', phone: str = '', remark: str = '', roleid: int = '', status: bool = ''):
        """
        更新
        :param str account: 账号
    :param int id: 主键id
    :param str name: 用户名
    :param str password: 密码
    :param str phone: 联系电话
    :param str remark: 备注
    :param int roleid: 角色id
    :param bool status: 状态 1 启用  0 禁用
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/user/update'
        params = {
            'account': account,
            'id': id,
            'name': name,
            'password': password,
            'phone': phone,
            'remark': remark,
            'roleid': roleid,
            'status': status,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def open_getspacebyplate(self, access_token: str, parkcode: str = '', platenum: str = ''):
        """
        按车牌号查询泊位信息接口
        :param str parkcode: 停车场 ID
    :param str platenum: 车牌号
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/v2/open/getSpaceByPlate'
        params = {
            'parkcode': parkcode,
            'platenum': platenum,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def open_getspaceinfo(self, access_token: str, parkcode: str = '', spacenum: str = ''):
        """
        按泊位号查询泊位信息接口
        :param str parkcode: 停车场 ID
    :param str spacenum: 车位编号
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/v2/open/getSpaceInfo'
        params = {
            'parkcode': parkcode,
            'spacenum': spacenum,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def open_parkingspaceinfo(self, access_token: str, parkcode: str = ''):
        """
        车位信息列表接口
        :param str parkcode: 停车场 ID
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/v2/open/parkingSpaceInfo'
        params = {
            'parkcode': parkcode,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def warnillegalpark_deleteinids(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnIllegalPark/deleteInIds'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def warnillegalpark_insert(self, access_token: str, bindtype: int = '', parkareaidlist: list = '', plateno: str = '', warntimelist: list = ''):
        """
        添加
        :param int bindtype: 绑定类型  1：绑定车位  2：绑定区域
    :param list parkareaidlist: 车位或区域id
    :param str plateno: 车牌号
    :param list warntimelist: 告警时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnIllegalPark/insert'
        params = {
            'bindtype': bindtype,
            'parkareaidlist': parkareaidlist,
            'plateno': plateno,
            'warntimelist': warntimelist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def warnillegalpark_selectpagelist(self, access_token: str, endtime: str = '', id: int = '', pagenumber: int = 1, pagesize: int = 100, parkareaname: str = '', plateno: str = '', starttime: str = ''):
        """
        分页查询
        :param str endtime: 结束时间
    :param int id: 主键
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkareaname: 车位或区域的名称
    :param str plateno: 车牌号
    :param str starttime: 开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnIllegalPark/selectPageList'
        params = {
            'endtime': endtime,
            'id': id,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkareaname': parkareaname,
            'plateno': plateno,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def warnillegalpark_update(self, access_token: str, bindtype: int = '', id: int = '', parkareaidlist: list = '', plateno: str = '', warntimelist: list = ''):
        """
        更新
        :param int bindtype: 绑定类型  1：绑定车位  2：绑定区域
    :param int id: 主键
    :param list parkareaidlist: 车位或区域id
    :param str plateno: 车牌号
    :param list warntimelist: 告警时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnIllegalPark/update'
        params = {
            'bindtype': bindtype,
            'id': id,
            'parkareaidlist': parkareaidlist,
            'plateno': plateno,
            'warntimelist': warntimelist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def warnlog_selectpagelist(self, access_token: str, endtime: str = '', id: int = '', pagenumber: int = 1, pagesize: int = 100, parkno: str = '', parkplateno: str = '', starttime: str = '', warnstatus: int = '', warntype: int = ''):
        """
        分页查询
        :param str endtime: 结束时间
    :param int id: 主键
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位编号
    :param str parkplateno: 违停车牌
    :param str starttime: 开始时间
    :param int warnstatus: 告警状态  1：告警中  2：手动停止  3：自动停止
    :param int warntype: 告警类型  1：车位占用告警   2：车辆违停告警  3：特殊车辆入车  4：特殊车辆出车  5：车辆压线 
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnLog/selectPageList'
        params = {
            'endtime': endtime,
            'id': id,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkno': parkno,
            'parkplateno': parkplateno,
            'starttime': starttime,
            'warnstatus': warnstatus,
            'warntype': warntype,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def warnlog_stopwarn(self, access_token: str):
        """
        停止告警
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnLog/stopWarn'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def warnspaceoccupy_deletebyelementparkid(self, access_token: str):
        """
        删除指定车位id的记录
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnSpaceOccupy/deleteByElementParkId'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def warnspaceoccupy_deleteinids(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnSpaceOccupy/deleteInIds'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def warnspaceoccupy_insert(self, access_token: str, parkid: int = '', plateno: str = '', warntimelist: list = ''):
        """
        添加
        :param int parkid: 车位id
    :param str plateno: 车牌号
    :param list warntimelist: 告警时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnSpaceOccupy/insert'
        params = {
            'parkid': parkid,
            'plateno': plateno,
            'warntimelist': warntimelist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def warnspaceoccupy_selectpagelist(self, access_token: str, endtime: str = '', id: int = '', pagenumber: int = 1, pagesize: int = 100, parkno: str = '', plateno: str = '', starttime: str = ''):
        """
        分页查询
        :param str endtime: 结束时间
    :param int id: 主键
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位号
    :param str plateno: 绑定车牌号，多个车牌号中间用英文分号隔开
    :param str starttime: 开始时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnSpaceOccupy/selectPageList'
        params = {
            'endtime': endtime,
            'id': id,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'parkno': parkno,
            'plateno': plateno,
            'starttime': starttime,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def warnspaceoccupy_update(self, access_token: str, id: int = '', parkid: int = '', plateno: str = '', warntimelist: list = ''):
        """
        更新
        :param int id: 主键
    :param int parkid: 车位id
    :param str plateno: 绑定车牌号，多个车牌号中间用英文分号隔开
    :param list warntimelist: 告警时间
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnSpaceOccupy/update'
        params = {
            'id': id,
            'parkid': parkid,
            'plateno': plateno,
            'warntimelist': warntimelist,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def warnspecialcar_deleteinids(self, access_token: str):
        """
        批量删除
        :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnSpecialCar/deleteInIds'
        params = {
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('GET', url, json=params, headers=headers)
        return response.json()


    def warnspecialcar_insert(self, access_token: str, lightwarnwitch: bool = '', plateno: str = '', remark: str = '', warntimelist: list = '', warntype: int = ''):
        """
        添加
        :param bool lightwarnwitch: 车位灯告警开关   1：开  0：关
    :param str plateno: 车牌号
    :param str remark: 备注
    :param list warntimelist: 告警时间
    :param int warntype: 告警类型  1：入车告警  2：出车告警  3：入车和出车都告警
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnSpecialCar/insert'
        params = {
            'lightwarnwitch': lightwarnwitch,
            'plateno': plateno,
            'remark': remark,
            'warntimelist': warntimelist,
            'warntype': warntype,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def warnspecialcar_selectpagelist(self, access_token: str, endtime: str = '', id: int = '', lightwarnwitch: bool = '', pagenumber: int = 1, pagesize: int = 100, plateno: str = '', remark: str = '', starttime: str = '', warntype: int = ''):
        """
        分页查询
        :param str endtime: 结束时间
    :param int id: 主键
    :param bool lightwarnwitch: 车位灯告警开关   1：开  0：关
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str plateno: 车牌号
    :param str remark: 备注
    :param str starttime: 开始时间
    :param int warntype: 告警类型  1：入车告警  2：出车告警  3：入车和出车都告警
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnSpecialCar/selectPageList'
        params = {
            'endtime': endtime,
            'id': id,
            'lightwarnwitch': lightwarnwitch,
            'pagenumber': pagenumber,
            'pagesize': pagesize,
            'plateno': plateno,
            'remark': remark,
            'starttime': starttime,
            'warntype': warntype,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()


    def warnspecialcar_update(self, access_token: str, id: int = '', lightwarnwitch: bool = '', plateno: str = '', remark: str = '', warntimelist: list = '', warntype: int = ''):
        """
        更新
        :param int id: 主键
    :param bool lightwarnwitch: 车位灯告警开关   1：开  0：关
    :param str plateno: 车牌号
    :param str remark: 备注
    :param list warntimelist: 告警时间
    :param int warntype: 告警类型  1：入车告警  2：出车告警  3：入车和出车都告警
    :param str access_token: The access token for authentication
        """
        url = self.base_url + '/warnSpecialCar/update'
        params = {
            'id': id,
            'lightwarnwitch': lightwarnwitch,
            'plateno': plateno,
            'remark': remark,
            'warntimelist': warntimelist,
            'warntype': warntype,
        }
        headers = {
            'Accesstoken': f'{access_token}'
        }
        response = requests.request('POST', url, json=params, headers=headers)
        return response.json()



import requests

#############################


def accessconfig_get():
    """
    获取配置信息
    
    """
    url = 'http://192.168.21.249:8083' + '/accessConfig/get'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def accessconfig_update(a: int, armycar: int, b: int, baudrate: int, broadcastinterval: int, broadcasttimes: int, c: int, channelhttp: str, civilcar: int, dspport: int, embassycar: int, farmcar: int, frontsavepath: str, id: int, ippre: str, newenergycar: int, nodeport: int, originalpicturepath: str, personalitycar: int, policecar: int, prnum: int, province: str, qualityinspectionpicturepath: str, recognitionlibpath: str, recognitionpath: str, recognitionswitch: int, regionpicturepath: str, serialport: str, setlprcs: int, setlrnum: int, setpriority: int, snappicturepath: str, switchserialport: int, temprcvpath: str, typeprnum: int, wujingcar: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/accessConfig/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def apiaccessinfo_selectlist():
    """
    列表查询
    
    """
    url = 'http://192.168.21.249:8083' + '/apiAccessInfo/selectList'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def apiaccessinfo_skipauthbyall(skipauth: bool):
    """
    对全数据(修改全表字段)跳过鉴权
    :param bool skipauth: skipAuth
    """
    url = 'http://192.168.21.249:8083' + '/apiAccessInfo/skipAuthByAll'
    params = {
        'skipauth': skipauth,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def apiaccessinfo_updatebyid(apiperm: str, appcode: str, createtime: str, creator: str, deleted: bool, id: int, secret: str, skipauth: bool, tenantname: str, tenanttel: int, updatetime: str, updater: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/apiAccessInfo/updateById'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def apireportmanage_getall():
    """
    查询上行上报配置
    
    """
    url = 'http://192.168.21.249:8083' + '/apiReportManage/getAll'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def apireportmanage_switchconfig(cmd: str, otherreportswitch: int, unifiedswitch: int):
    """
    上行上报配置开关接口
    :param str cmd: 接口编码标识
    :param int otherreportswitch: 其他平台上报总开关(0关闭，1开启)
    :param int unifiedswitch: 统一平台上报开关(0关闭，1开启)
    """
    url = 'http://192.168.21.249:8083' + '/apiReportManage/switchConfig'
    params = {
        'cmd': cmd,
        'otherreportswitch': otherreportswitch,
        'unifiedswitch': unifiedswitch,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def apireportmanage_updateotherreport(apipushinfodtolist: list, cmd: str, name: str, otherreportswitch: int, unifiedswitch: int):
    """
    更新其他上报地址信息
    :param list apipushinfodtolist: No description
    :param str cmd: No description
    :param str name: No description
    :param int otherreportswitch: No description
    :param int unifiedswitch: No description
    """
    url = 'http://192.168.21.249:8083' + '/apiReportManage/updateOtherReport'
    params = {
        'apipushinfodtolist': apipushinfodtolist,
        'cmd': cmd,
        'name': name,
        'otherreportswitch': otherreportswitch,
        'unifiedswitch': unifiedswitch,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def areacamera_delete(idlist: str):
    """
    删除
    :param str idlist: idList
    """
    url = 'http://192.168.21.249:8083' + '/areaCamera/delete'
    params = {
        'idlist': idlist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def areacamera_insert(areacamerarelatelist: list, cameradirection: int, cameraip: str, id: int, remark: str):
    """
    添加
    :param list areacamerarelatelist: 区域相机关联信息
    :param int cameradirection: 相机方向
    :param str cameraip: 相机ip
    :param int id: 主键
    :param str remark: 备注
    """
    url = 'http://192.168.21.249:8083' + '/areaCamera/insert'
    params = {
        'areacamerarelatelist': areacamerarelatelist,
        'cameradirection': cameradirection,
        'cameraip': cameraip,
        'id': id,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def areacamera_selectpagelist(areaid: int, cameraip: str, endtime: str, id: int, pagenumber: int, pagesize: int, remark: str, starttime: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/areaCamera/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def areacamera_update(areacamerarelatelist: list, cameradirection: int, cameraip: str, id: int, remark: str):
    """
    更新
    :param list areacamerarelatelist: 区域相机关联信息
    :param int cameradirection: 相机方向
    :param str cameraip: 相机ip
    :param int id: 主键
    :param str remark: 备注
    """
    url = 'http://192.168.21.249:8083' + '/areaCamera/update'
    params = {
        'areacamerarelatelist': areacamerarelatelist,
        'cameradirection': cameradirection,
        'cameraip': cameraip,
        'id': id,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def areadevice_deletebatch(ids: str):
    """
    批量删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/areaDevice/deleteBatch'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def areadevice_save(addr: int, areadevicerelations: list, id: int, remark: str):
    """
    新增
    :param int addr: No description
    :param list areadevicerelations: No description
    :param int id: No description
    :param str remark: No description
    """
    url = 'http://192.168.21.249:8083' + '/areaDevice/save'
    params = {
        'addr': addr,
        'areadevicerelations': areadevicerelations,
        'id': id,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def areadevice_selectpagelist(addr: int, areaids: int, endtime: str, id: int, lotid: int, pagenumber: int, pagesize: int, starttime: str, status: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/areaDevice/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def areadevice_update(addr: int, areadevicerelations: list, id: int, remark: str):
    """
    修改
    :param int addr: No description
    :param list areadevicerelations: No description
    :param int id: No description
    :param str remark: No description
    """
    url = 'http://192.168.21.249:8083' + '/areaDevice/update'
    params = {
        'addr': addr,
        'areadevicerelations': areadevicerelations,
        'id': id,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def areainfo_addstereoscopicarea(floorid: int, id: int, lotid: int, name: str, parkspacecameraip: str, x: str, y: str):
    """
    立体区域新增接口
    :param int floorid: 楼层id
    :param int id: 主键ID，新增时该值不传，主要用于更新
    :param int lotid: 车场编码
    :param str name: 名称
    :param str parkspacecameraip: 立体车位相机IP
    :param str x: x轴坐标
    :param str y: y轴坐标
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/addStereoscopicArea'
    params = {
        'floorid': floorid,
        'id': id,
        'lotid': lotid,
        'name': name,
        'parkspacecameraip': parkspacecameraip,
        'x': x,
        'y': y,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def areainfo_deletebatchbyid(areaids: str):
    """
    删除区域(参数Ids逗号分隔)
    :param str areaids: areaIds
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/deleteBatchById'
    params = {
        'areaids': areaids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def areainfo_deletestereoscopicarea(areaids: str):
    """
    立体区域删除接口(参数Ids逗号分隔)
    :param str areaids: 参数Ids逗号分隔
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/deleteStereoscopicArea'
    params = {
        'areaids': areaids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def areainfo_insert(areainoutfreecountnumber: int, areaname: str, countstatisticstype: int, floorid: int, lotid: int, type: int, x: str, y: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def areainfo_listfloorarea(flooid: int):
    """
    遍历指定楼层的所有区域
    :param int flooid: 楼层id
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/listFloorArea'
    params = {
        'flooid': flooid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def areainfo_saveparkarearelation(afterparklist: list, areaid: int, beforeparklist: list):
    """
    保存车位关联区域关系
    :param list afterparklist: 区域绑定车位修改后列表
    :param int areaid: 车位关联区域id
    :param list beforeparklist: 区域绑定车位修改前列表
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/saveParkAreaRelation'
    params = {
        'afterparklist': afterparklist,
        'areaid': areaid,
        'beforeparklist': beforeparklist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def areainfo_selectall():
    """
    查询所有区域
    
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/selectAll'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def areainfo_selectbyid(id: int):
    """
    区域详情
    :param int id: id
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/selectById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def areainfo_selectfloorareabylotid(lotid: int):
    """
    查询车场所有楼层 - 区域
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/selectFloorAreaByLotId'
    params = {
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def areainfo_selectlistbyfloorid(floorid: int):
    """
    根据楼层查询区域列表
    :param int floorid: floorId
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/selectListByFloorId'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def areainfo_selectpagelist(areaid: int, areaname: str, endtime: str, floorid: int, lotid: int, pagenumber: int, pagesize: int, starttime: str, type: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def areainfo_selectparklistbyarea(areaid: int, currentareaid: int, floorid: int):
    """
    根据区域查询车位信息及关联区域关系
    :param int areaid: 车位关联区域id
    :param int currentareaid: 当前区域ID
    :param int floorid: 楼层id
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/selectParkListByArea'
    params = {
        'areaid': areaid,
        'currentareaid': currentareaid,
        'floorid': floorid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def areainfo_selectstereoscopicpagelist(endtime: str, floorname: str, name: str, pagenumber: int, pagesize: int, parkspacecameraip: str, parkspacecamerauniqueid: str, starttime: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/selectStereoscopicPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def areainfo_updatebyid(areainoutfreecountnumber: int, areaname: str, countstatisticstype: int, floorid: int, id: int, type: int, x: str, y: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/updateById'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def areainfo_updatestereoscopicarea(floorid: int, id: int, lotid: int, name: str, parkspacecameraip: str, x: str, y: str):
    """
    立体区域更新接口
    :param int floorid: 楼层id
    :param int id: 主键ID，新增时该值不传，主要用于更新
    :param int lotid: 车场编码
    :param str name: 名称
    :param str parkspacecameraip: 立体车位相机IP
    :param str x: x轴坐标
    :param str y: y轴坐标
    """
    url = 'http://192.168.21.249:8083' + '/areaInfo/updateStereoscopicArea'
    params = {
        'floorid': floorid,
        'id': id,
        'lotid': lotid,
        'name': name,
        'parkspacecameraip': parkspacecameraip,
        'x': x,
        'y': y,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def auth_exttokenlogin(token: str):
    """
    第三方token登录接口
    :param str token: token
    """
    url = 'http://192.168.21.249:8083' + '/auth/extTokenLogin'
    params = {
        'token': token,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def auth_login(account: str, password: str, verifycode: str):
    """
    登录接口
    :param str account: account
    :param str password: password
    :param str verifycode: verifyCode
    """
    url = 'http://192.168.21.249:8083' + '/auth/login'
    params = {
        'account': account,
        'password': password,
        'verifycode': verifycode,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def auth_loginbyticket(ticket: str):
    """
    通过单车场ticket登录
    :param str ticket: ticket
    """
    url = 'http://192.168.21.249:8083' + '/auth/loginByTicket'
    params = {
        'ticket': ticket,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def auth_tokenvalid():
    """
    判断token是否有效
    
    """
    url = 'http://192.168.21.249:8083' + '/auth/tokenValid'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def auth_verifycode():
    """
    生成图形验证码
    
    """
    url = 'http://192.168.21.249:8083' + '/auth/verifyCode'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def berthrate():
    """
    泊位率测试接口
    
    """
    url = 'http://192.168.21.249:8083' + '/berthRate'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def berthrate_exportberthrate(endtime: str, selectberthtype: int, starttime: str):
    """
    导出泊位率信息
    :param str endtime: 结束时间
    :param int selectberthtype: 查询泊位率类型，0：查询楼层，1：查询车位类型  默认查询楼层
    :param str starttime: 开始时间
    """
    url = 'http://192.168.21.249:8083' + '/berthRate/exportBerthRate'
    params = {
        'endtime': endtime,
        'selectberthtype': selectberthtype,
        'starttime': starttime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def berthrate_selectberthlist(endtime: str, selectberthtype: int, starttime: str):
    """
    查询泊位率信息
    :param str endtime: 结束时间
    :param int selectberthtype: 查询泊位率类型，0：查询楼层，1：查询车位类型  默认查询楼层
    :param str starttime: 开始时间
    """
    url = 'http://192.168.21.249:8083' + '/berthRate/selectBerthList'
    params = {
        'endtime': endtime,
        'selectberthtype': selectberthtype,
        'starttime': starttime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def carinoutrecord_export(areaname: str, floorid: int, id: int, inendtime: str, instarttime: str, intype: int, lotid: int, outendtime: str, outstarttime: str, outtype: int, pagenumber: int, pagesize: int, parkno: str, plateno: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/car-in-out-record/export'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def carinoutrecord_selectpagelist(areaname: str, floorid: int, id: int, inendtime: str, instarttime: str, intype: int, lotid: int, outendtime: str, outstarttime: str, outtype: int, pagenumber: int, pagesize: int, parkno: str, plateno: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/car-in-out-record/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def carinoutstatistics_exportbyfloor(recordendtime: str, recordstarttime: str, type: int):
    """
    出入车流量导出（按楼层）
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param int type: 统计类型:入车-1 出车-0
    """
    url = 'http://192.168.21.249:8083' + '/car-in-out-statistics/exportByFloor'
    params = {
        'recordendtime': recordendtime,
        'recordstarttime': recordstarttime,
        'type': type,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def carinoutstatistics_exportbyspecies(recordendtime: str, recordstarttime: str, type: int):
    """
    出入车流量导出（按车位种类）
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param int type: 统计类型:入车-1 出车-0
    """
    url = 'http://192.168.21.249:8083' + '/car-in-out-statistics/exportBySpecies'
    params = {
        'recordendtime': recordendtime,
        'recordstarttime': recordstarttime,
        'type': type,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def carinoutstatistics_listmapbyfloor(recordendtime: str, recordstarttime: str, type: int):
    """
    楼层分组查询
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param int type: 统计类型:入车-1 出车-0
    """
    url = 'http://192.168.21.249:8083' + '/car-in-out-statistics/listMapByFloor'
    params = {
        'recordendtime': recordendtime,
        'recordstarttime': recordstarttime,
        'type': type,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def carinoutstatistics_refreshinoutcarstatistics(endtime: str, starttime: str):
    """
    刷新入出车流量报表
    :param str endtime: endTime
    :param str starttime: startTime
    """
    url = 'http://192.168.21.249:8083' + '/car-in-out-statistics/refreshInOutCarStatistics'
    params = {
        'endtime': endtime,
        'starttime': starttime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def carinoutstatistics_selectpagelist(pagenumber: int, pagesize: int, recordendtime: str, recordstarttime: str, type: int):
    """
    分页查询(按车位种类)
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param int type: 统计类型:入车-1 出车-0
    """
    url = 'http://192.168.21.249:8083' + '/car-in-out-statistics/selectPageList'
    params = {
        'pagenumber': pagenumber,
        'pagesize': pagesize,
        'recordendtime': recordendtime,
        'recordstarttime': recordstarttime,
        'type': type,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def carinoutstatistics_sumcarinoutstatistics(recordendtime: str, recordstarttime: str, type: int):
    """
    累计统计时间段的出入车流量
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    :param int type: 统计类型:入车-1 出车-0
    """
    url = 'http://192.168.21.249:8083' + '/car-in-out-statistics/sumCarInOutStatistics'
    params = {
        'recordendtime': recordendtime,
        'recordstarttime': recordstarttime,
        'type': type,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def carinoutrecordarea_selectpagelist(areaname: str, endtime: str, floorid: int, id: int, pagenumber: int, pagesize: int, plateno: str, starttime: str, type: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/carInOutRecordArea/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def colortransparencystyles_batchsave(colortransparencystylesaddrequestvolist: str):
    """
    批量保存
    :param str colortransparencystylesaddrequestvolist: colorTransparencyStylesAddRequestVOList
    """
    url = 'http://192.168.21.249:8083' + '/color-transparency-styles/batchSave'
    params = {
        'colortransparencystylesaddrequestvolist': colortransparencystylesaddrequestvolist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def column_delete(ids: str):
    """
    删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/column/delete'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def column_deletebyfloorid(floorid: int):
    """
    删除某个楼层柱子
    :param int floorid: floorId
    """
    url = 'http://192.168.21.249:8083' + '/column/deleteByFloorId'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def column_exportdatasynchronization():
    """
    数据同步-导出
    
    """
    url = 'http://192.168.21.249:8083' + '/column/exportDataSynchronization'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def column_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/column/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def column_importdatasynchronization(multipartfile: str):
    """
    数据同步-导入
    :param str multipartfile: 导入文件
    """
    url = 'http://192.168.21.249:8083' + '/column/importDataSynchronization'
    params = {
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def column_selectpagelist(control: int, elementcustomid: int, floorenablestatus: int, floorid: int, floorname: str, floorstatus: int, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, parkaddr: int, parkcategory: int, parkno: str, status: int, type: int, uniqueidentificationfield: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/column/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def column_update(chargingbrand: str, chargingtype: int, control: int, createtime: str, deleted: bool, devicetype: int, enable: int, floorid: int, id: int, lotid: int, name: str, parkaddr: int, parkcategory: int, parkno: str, parkinglockequipmentno: str, parkingpropertyright: str, status: int, stereoscopicparkcameraaddr: int, toward: int, type: int, updatetime: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/column/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def config_getiniconfig():
    """
    查询C++参数配置信息
    
    """
    url = 'http://192.168.21.249:8083' + '/config/getIniConfig'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def config_getregistidentlibinfo():
    """
    查询注册识别库信息
    
    """
    url = 'http://192.168.21.249:8083' + '/config/getRegistIdentlibInfo'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def config_operateregistidentlib(type: str):
    """
    操作-注册识别库
    :param str type: type
    """
    url = 'http://192.168.21.249:8083' + '/config/operateRegistIdentlib'
    params = {
        'type': type,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def config_saveiniconfig(comname: str, dsprecog: int, picswitch: int, province: str, ret: int, witch: int):
    """
    保存C++参数配置信息
    :param str comname: 连接服务器的端口号 windows下是COM5, linux下是/dev/ttyS0
    :param int dsprecog: 控制软识别与硬识别 0 软识别, 1 硬识别
    :param int picswitch: 是否开启空车牌图片收集功能  1 开启,  0 关闭
    :param str province: 车牌的默认省份(省份简称汉字) 默认为空
    :param int ret: 控制TCP还是485通讯 0 tcp, 1 485
    :param int witch: 控制故障状态的设备的开关 0 关闭， 1 开启
    """
    url = 'http://192.168.21.249:8083' + '/config/saveIniConfig'
    params = {
        'comname': comname,
        'dsprecog': dsprecog,
        'picswitch': picswitch,
        'province': province,
        'ret': ret,
        'witch': witch,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def config_test(cmd: str):
    """
    操作-test
    :param str cmd: cmd
    """
    url = 'http://192.168.21.249:8083' + '/config/test'
    params = {
        'cmd': cmd,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def constant_commonenum():
    """
    枚举汇总
    
    """
    url = 'http://192.168.21.249:8083' + '/constant/commonEnum'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def coordinate_getfilestatus(floorid: int, lotid: int, type: int):
    """
    查询文件状态
    :param int floorid: floorId
    :param int lotid: lotId
    :param int type: type
    """
    url = 'http://192.168.21.249:8083' + '/coordinate/getFileStatus'
    params = {
        'floorid': floorid,
        'lotid': lotid,
        'type': type,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def coordinate_selectelementinfo(floorid: int, idorname: str, lotid: int, selecttype: int, type: int):
    """
    元素按照id/编号精确查询
    :param int floorid: 楼层id
    :param str idorname: 根据id或者元素名称
    :param int lotid: 车场id
    :param int selecttype: 查询方式，0：模糊查询，1：精准查询
    :param int type: 元素类型
    """
    url = 'http://192.168.21.249:8083' + '/coordinate/selectElementInfo'
    params = {
        'floorid': floorid,
        'idorname': idorname,
        'lotid': lotid,
        'selecttype': selecttype,
        'type': type,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def coordinate_selectfuzzyelementinfo(floorid: int, keyword: str, lotid: int, type: str):
    """
    元素模糊查询
    :param int floorid: 楼层id
    :param str keyword: 关键字
    :param int lotid: 车场id
    :param str type: 元素类型：parkNo parkAddr ibeaconMinor screenAddr machineIp pillarName customName
    """
    url = 'http://192.168.21.249:8083' + '/coordinate/selectFuzzyElementInfo'
    params = {
        'floorid': floorid,
        'keyword': keyword,
        'lotid': lotid,
        'type': type,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def coordinate_uploadcolumnfile(multipartfile: str, floorid: int, lotid: int):
    """
    上传柱子坐标文件xslx
    :param str multipartfile: No description
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/coordinate/uploadColumnFile'
    params = {
        'multipartfile': multipartfile,
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def coordinate_uploadcustomfile(multipartfile: str, elementcustomid: int, floorid: int, lotid: int):
    """
    上传自定义元素坐标文件
    :param str multipartfile: No description
    :param int elementcustomid: elementCustomId
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/coordinate/uploadCustomFile'
    params = {
        'multipartfile': multipartfile,
        'elementcustomid': elementcustomid,
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def coordinate_uploadgroundfile(multipartfile: str, floorid: int, lotid: int):
    """
    上传地面坐标文件
    :param str multipartfile: No description
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/coordinate/uploadGroundFile'
    params = {
        'multipartfile': multipartfile,
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def coordinate_uploadparkfile(multipartfile: str, floorid: int, lotid: int):
    """
    上传车位坐标文件xslx
    :param str multipartfile: No description
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/coordinate/uploadParkFile'
    params = {
        'multipartfile': multipartfile,
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def deviceescalation_selectexceptionpagelist(pagenumber: int, pagesize: int):
    """
    分页查询设备同步异常信息
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    """
    url = 'http://192.168.21.249:8083' + '/deviceEscalation/selectExceptionPageList'
    params = {
        'pagenumber': pagenumber,
        'pagesize': pagesize,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def deviceescalation_selectpagelist(areaname: str, deviceip: str, exception: int, floorname: str, pagenumber: int, pagesize: int, parkno: str):
    """
    分页查询
    :param str areaname: 区域名称
    :param str deviceip: 上报设备IP
    :param int exception: 异常问题(0：正常， 1：车位编号重复， 2：无车位编号)
    :param str floorname: 楼层名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位编号
    """
    url = 'http://192.168.21.249:8083' + '/deviceEscalation/selectPageList'
    params = {
        'areaname': areaname,
        'deviceip': deviceip,
        'exception': exception,
        'floorname': floorname,
        'pagenumber': pagenumber,
        'pagesize': pagesize,
        'parkno': parkno,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def deviceinfo_deletebyids(ids: str):
    """
    设备批量删除（id以英文逗号分隔开）
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/deviceInfo/deleteByIds'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def deviceinfo_devicelistalign():
    """
    设备列表校准
    
    """
    url = 'http://192.168.21.249:8083' + '/deviceInfo/deviceListAlign'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def deviceinfo_exportdevicelist(deviceaddrip: str, devicetype: int, id: int, nodedeviceaddr: str, onlinestatus: int, pagenumber: int, pagesize: int, protocoltype: int, workingstatus: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/deviceInfo/exportDeviceList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def deviceinfo_getallnodeaddrlist():
    """
    获取节点地址列表
    
    """
    url = 'http://192.168.21.249:8083' + '/deviceInfo/getAllNodeAddrList'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def deviceinfo_getallnodedevice():
    """
    获取节点设备地址列表
    
    """
    url = 'http://192.168.21.249:8083' + '/deviceInfo/getAllNodeDevice'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def deviceinfo_importdatabyexcel(multipartfile: str):
    """
    通过excel导入节点设备
    :param str multipartfile: No description
    """
    url = 'http://192.168.21.249:8083' + '/deviceInfo/importDataByExcel'
    params = {
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def deviceinfo_save(addr: str, devicetype: int, floorid: int, id: str, relateparknum: int, remark: str):
    """
    新增 - 节点设备
    :param str addr: 设备ip转化后的数字，用于与设备建立连接
    :param int devicetype: 设备类型
    :param int floorid: 楼层id
    :param str id: id
    :param int relateparknum: 关联车位数
    :param str remark: 备注
    """
    url = 'http://192.168.21.249:8083' + '/deviceInfo/save'
    params = {
        'addr': addr,
        'devicetype': devicetype,
        'floorid': floorid,
        'id': id,
        'relateparknum': relateparknum,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def deviceinfo_selectdeviceeventlog(deviceaddr: str, deviceid: int, devicetype: int, eventtimeend: str, eventtimestart: str, eventtype: int, pagenumber: int, pagesize: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/deviceInfo/selectDeviceEventLog'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def deviceinfo_selectpagelist(deviceaddrip: str, devicetype: int, id: int, nodedeviceaddr: str, onlinestatus: int, pagenumber: int, pagesize: int, protocoltype: int, workingstatus: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/deviceInfo/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def deviceinfo_update(addr: str, devicetype: int, floorid: int, id: str, relateparknum: int, remark: str):
    """
    修改 - 节点设备
    :param str addr: 设备ip转化后的数字，用于与设备建立连接
    :param int devicetype: 设备类型
    :param int floorid: 楼层id
    :param str id: id
    :param int relateparknum: 关联车位数
    :param str remark: 备注
    """
    url = 'http://192.168.21.249:8083' + '/deviceInfo/update'
    params = {
        'addr': addr,
        'devicetype': devicetype,
        'floorid': floorid,
        'id': id,
        'relateparknum': relateparknum,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementconnector_deletebatchbyids(ids: str):
    """
    批量删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/element-connector/deleteBatchByIds'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementconnector_exportdatasynchronization():
    """
    数据同步-导出
    
    """
    url = 'http://192.168.21.249:8083' + '/element-connector/exportDataSynchronization'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementconnector_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/element-connector/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementconnector_importdatasynchronization(lotid: int, multipartfile: str):
    """
    数据同步-导入
    :param int lotid: lotId
    :param str multipartfile: 导入文件
    """
    url = 'http://192.168.21.249:8083' + '/element-connector/importDataSynchronization'
    params = {
        'lotid': lotid,
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementconnector_insert(associatedconnectorids: str, floorid: int, lotid: int, name: str, species: int, xpoint: str, ypoint: str):
    """
    添加
    :param str associatedconnectorids: 关联设施ids，id之间以,隔开
    :param int floorid: 楼层id
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param int species: 种类 1：直梯 2：护梯 3：楼梯 4：出入口 5 车行车场入口 6 车行车场出口 7 车行场内入口 8 车行场内出口
    :param str xpoint: No description
    :param str ypoint: No description
    """
    url = 'http://192.168.21.249:8083' + '/element-connector/insert'
    params = {
        'associatedconnectorids': associatedconnectorids,
        'floorid': floorid,
        'lotid': lotid,
        'name': name,
        'species': species,
        'xpoint': xpoint,
        'ypoint': ypoint,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementconnector_selectbylotid(lotid: int):
    """
    查询指定车场所有通行设施
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/element-connector/selectByLotId'
    params = {
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementconnector_selectbylotidandfloorid(floorid: int, lotid: int):
    """
    查询指定楼层所有通行设施
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/element-connector/selectByLotIdAndFloorId'
    params = {
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementconnector_selectpagelist(associatedconnectorids: str, endtime: str, floorid: int, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, species: int, starttime: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-connector/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementconnector_update(associatedconnectorids: str, floorid: int, id: int, lotid: int, name: str, species: int, xpoint: str, ypoint: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-connector/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementcustomdetail_addbatchcustomelement(custompointcontent: list, elementcustomid: int, floorid: int, lotid: int):
    """
    批量添加自定义元素
    :param list custompointcontent: No description
    :param int elementcustomid: No description
    :param int floorid: No description
    :param int lotid: No description
    """
    url = 'http://192.168.21.249:8083' + '/element-custom-detail/addBatchCustomElement'
    params = {
        'custompointcontent': custompointcontent,
        'elementcustomid': elementcustomid,
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementcustomdetail_delete(ids: str):
    """
    批量删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/element-custom-detail/delete'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementcustomdetail_deletebyfloorid(elementcustomid: int, floorid: int):
    """
    自定义元素 - 删除某个楼层数据
    :param int elementcustomid: elementCustomId
    :param int floorid: floorId
    """
    url = 'http://192.168.21.249:8083' + '/element-custom-detail/deleteByFloorId'
    params = {
        'elementcustomid': elementcustomid,
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementcustomdetail_export(control: int, elementcustomid: int, floorenablestatus: int, floorid: int, floorname: str, floorstatus: int, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, parkaddr: int, parkcategory: int, parkno: str, status: int, type: int, uniqueidentificationfield: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-custom-detail/export'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementcustomdetail_exportdatasynchronization():
    """
    数据同步-导出
    
    """
    url = 'http://192.168.21.249:8083' + '/element-custom-detail/exportDataSynchronization'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementcustomdetail_importdatasynchronization(lotid: int, multipartfile: str):
    """
    数据同步-导入
    :param int lotid: lotId
    :param str multipartfile: 导入文件
    """
    url = 'http://192.168.21.249:8083' + '/element-custom-detail/importDataSynchronization'
    params = {
        'lotid': lotid,
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementcustomdetail_insert(elementcustomid: int, floorid: int, lotid: int, name: str):
    """
    添加
    :param int elementcustomid: 自定义元素id
    :param int floorid: 楼层Id
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    """
    url = 'http://192.168.21.249:8083' + '/element-custom-detail/insert'
    params = {
        'elementcustomid': elementcustomid,
        'floorid': floorid,
        'lotid': lotid,
        'name': name,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementcustomdetail_selectpagelist(control: int, elementcustomid: int, floorenablestatus: int, floorid: int, floorname: str, floorstatus: int, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, parkaddr: int, parkcategory: int, parkno: str, status: int, type: int, uniqueidentificationfield: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-custom-detail/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementcustomdetail_selectpagelistoffloor(control: int, elementcustomid: int, floorenablestatus: int, floorid: int, floorname: str, floorstatus: int, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, parkaddr: int, parkcategory: int, parkno: str, status: int, type: int, uniqueidentificationfield: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-custom-detail/selectPageListOfFloor'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementcustomdetail_update(id: int, name: str):
    """
    编辑
    :param int id: 自定义元素详情的id
    :param str name: 名称
    """
    url = 'http://192.168.21.249:8083' + '/element-custom-detail/update'
    params = {
        'id': id,
        'name': name,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementcustom_delete(id: int):
    """
    删除
    :param int id: id
    """
    url = 'http://192.168.21.249:8083' + '/element-custom/delete'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementcustom_edit(height: str, id: int, name: str, suspendheight: str):
    """
    编辑
    :param str height: 高度 默认0.1m
    :param int id: 主键id
    :param str name: 名称
    :param str suspendheight: 离地高度 默认0m
    """
    url = 'http://192.168.21.249:8083' + '/element-custom/edit'
    params = {
        'height': height,
        'id': id,
        'name': name,
        'suspendheight': suspendheight,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementcustom_insert(height: str, lotid: int, name: str, suspendheight: str):
    """
    添加
    :param str height: 高度 默认0.1m
    :param int lotid: 车场id lot_info id
    :param str name: 名称
    :param str suspendheight: 离地高度 默认0m
    """
    url = 'http://192.168.21.249:8083' + '/element-custom/insert'
    params = {
        'height': height,
        'lotid': lotid,
        'name': name,
        'suspendheight': suspendheight,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementcustom_listelementcustom(lotid: int):
    """
    查询自定义元素列表
    :param int lotid: 车场id
    """
    url = 'http://192.168.21.249:8083' + '/element-custom/listElementCustom'
    params = {
        'lotid': lotid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementcustom_listelementcustomdetail(lotid: int):
    """
    根据车场和楼层查询自定义元素的坐标和高度等信息
    :param int lotid: 车场id
    """
    url = 'http://192.168.21.249:8083' + '/element-custom/listElementCustomDetail'
    params = {
        'lotid': lotid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementmachineconfig_deletemachinerouteinfobyids(ids: str):
    """
    批量删除找车路线信息
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/element-machine-config/deleteMachineRouteInfoByIds'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementmachineconfig_editmachinerouteinfo(acrosselevatorid: int, acrosselevatorname: str, acrosstype: int, createtime: str, creator: str, endid: int, endname: str, id: int, imgsrc: str, startid: int, startname: str, updatetime: str, updater: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-machine-config/editMachineRouteInfo'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementmachineconfig_getallmachinerouteinfo():
    """
    查询所有找车路线信息
    
    """
    url = 'http://192.168.21.249:8083' + '/element-machine-config/getAllMachineRouteInfo'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementmachineconfig_getconfiginfo():
    """
    查询配置信息
    
    """
    url = 'http://192.168.21.249:8083' + '/element-machine-config/getConfigInfo'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementmachineconfig_savemachinerouteinfo(acrosselevatorid: int, acrosselevatorname: str, acrosstype: int, createtime: str, creator: str, endid: int, endname: str, id: int, imgsrc: str, startid: int, startname: str, updatetime: str, updater: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-machine-config/saveMachineRouteInfo'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementmachineconfig_updateconfiginfo(createtime: str, creator: str, emptyplaterecordcount: int, foreginlanguage: str, id: int, inquireways: list, isopenprint: int, isopenqrcode: int, languagesupport: int, machinemapswitch: int, parkmaxnum: int, platemaxnum: int, rotationangle: int, rotationswitch: int, routeqrswitch: int, routeqrtype: int, routeqrurl: str, scheduleface: int, updatetime: str, updater: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-machine-config/updateConfigInfo'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementmachine_deletebatchbyids(ids: str):
    """
    批量删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/element-machine/deleteBatchByIds'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementmachine_deletebyfloorid(floorid: int):
    """
    找车机-删除某个楼层的找车机
    :param int floorid: floorId
    """
    url = 'http://192.168.21.249:8083' + '/element-machine/deleteByFloorId'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementmachine_exportdatasynchronization():
    """
    数据同步-导出
    
    """
    url = 'http://192.168.21.249:8083' + '/element-machine/exportDataSynchronization'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementmachine_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/element-machine/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementmachine_importdatasynchronization(lotid: int, multipartfile: str):
    """
    数据同步-导入
    :param int lotid: lotId
    :param str multipartfile: 导入文件
    """
    url = 'http://192.168.21.249:8083' + '/element-machine/importDataSynchronization'
    params = {
        'lotid': lotid,
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementmachine_insert(directionnum: int, floorid: int, ip: str, lotid: int, name: str, species: int, xpoint: str, ypoint: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-machine/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementmachine_listmachineip():
    """
    有效的找车机ip集合
    
    """
    url = 'http://192.168.21.249:8083' + '/element-machine/listMachineIp'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementmachine_selectbylotidandfloorid(floorid: int, lotid: int):
    """
    查询指定楼层所有的找车机
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/element-machine/selectByLotIdAndFloorId'
    params = {
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementmachine_selectpagelist(endtime: str, floorenablestatus: int, floorid: int, id: int, ip: str, lotid: int, name: str, pagenumber: int, pagesize: int, species: int, starttime: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-machine/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementmachine_update(directionnum: int, floorid: int, id: int, ip: str, lotid: int, name: str, species: int, xpoint: str, ypoint: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-machine/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementpath_exporttotxt():
    """
    导出文本格式的数据
    
    """
    url = 'http://192.168.21.249:8083' + '/element-path/exportToTxt'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementpath_getbylotidandfloorid(floorid: int, lotid: int):
    """
    获取指定楼层的路网数据
    :param int floorid: 楼层id
    :param int lotid: 车场id
    """
    url = 'http://192.168.21.249:8083' + '/element-path/getByLotIdAndFloorId'
    params = {
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementpath_importbytxt(multipartfile: str):
    """
    通过文本导入数据
    :param str multipartfile: multipartFile
    """
    url = 'http://192.168.21.249:8083' + '/element-path/importByTxt'
    params = {
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementpath_update(floorid: int, lotid: int, pathlist: list):
    """
    更新路网数据
    :param int floorid: 楼层id
    :param int lotid: 车场id
    :param list pathlist: 路网集合
    """
    url = 'http://192.168.21.249:8083' + '/element-path/update'
    params = {
        'floorid': floorid,
        'lotid': lotid,
        'pathlist': pathlist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementscreen_deletebatchbyids(ids: str):
    """
    批量删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/deleteBatchByIds'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreen_deletebyfloorid(floorid: int):
    """
    屏 - 删除某个楼层数据
    :param int floorid: floorId
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/deleteByFloorId'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreen_downloadlcdlog(filename: str):
    """
    下载LCD日志文件
    :param str filename: 文件名
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/downloadLcdLog'
    params = {
        'filename': filename,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreen_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreen_getelementscreenwithlcdconfig(id: int):
    """
    根据主键获取详情(包含LCD屏配置信息)
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/getElementScreenWithLcdConfig'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreen_getelementscreenwithlcdconfigbyip(ip: str):
    """
    根据ip地址获取详情(包含LCD屏配置信息)
    :param str ip: ip
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/getElementScreenWithLcdConfigByIp'
    params = {
        'ip': ip,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreen_getscreenconfigofh5(ip: str, type: int):
    """
    H5单页面展示信息
    :param str ip: 屏ip
    :param int type: 屏类型
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/getScreenConfigOfH5'
    params = {
        'ip': ip,
        'type': type,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreen_insert(direction: int, elementscreenchildrequestvolist: list, floorid: int, lotid: int, name: str, screenaddr: int, screencategory: int, screentype: int, species: int, subscreennum: int, xpoint: str, ypoint: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementscreen_ledpagerefresh(screenid: int):
    """
    LED屏页面刷新
    :param int screenid: 主屏ID
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/ledPageRefresh'
    params = {
        'screenid': screenid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreen_move(direction: int, elementscreenchildrequestvolist: list, floorid: int, id: int, lotid: int, name: str, screenaddr: int, screentype: int, species: int, subscreennum: int, xpoint: str, ypoint: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/move'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementscreen_savelcdconfig(createtime: str, creator: str, deleted: bool, direction: int, floorid: int, id: int, lcdscreenconfiglist: list, lotid: int, name: str, onlinestatus: list, refreshflag: bool, remark: str, screenaddr: int, screentype: int, showtemplate: int, species: int, subscreennum: int, updatetime: str, updater: str, xpoint: str, ypoint: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/saveLcdConfig'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementscreen_selectbylotidandfloorid(floorid: int, lotid: int):
    """
    查询指定楼层所有屏
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/selectByLotIdAndFloorId'
    params = {
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreen_selectpagelist(endtime: str, floorenablestatus: int, floorid: int, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, screenaddr: int, species: int, starttime: str, subscreennum: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementscreen_selectscreenlistbypage(endtime: str, floorenablestatus: int, floorid: int, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, screenaddr: int, species: int, starttime: str, subscreennum: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/selectScreenListByPage'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementscreen_sendlcdscreencmd(cmd: str, data: str, ip: str, reqid: str, scene: str, screenaddr: int, showtemplate: int, ts: int, type: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/sendLcdScreenCmd'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementscreen_update(direction: int, elementscreenchildrequestvolist: list, floorid: int, id: int, lotid: int, name: str, screenaddr: int, screentype: int, species: int, subscreennum: int, xpoint: str, ypoint: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/element-screen/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def element3dmodel_deletebyid(id: int):
    """
    删除
    :param int id: id
    """
    url = 'http://192.168.21.249:8083' + '/element3dModel/deleteById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def element3dmodel_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/element3dModel/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def element3dmodel_insert(createtime: str, creator: str, elementname: str, elementtype: int, floorid: int, id: int, lotid: int, rotationangle: str, scale: str, suspendheight: str, updatetime: str, updater: str, xpoint: int, ypoint: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/element3dModel/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def element3dmodel_selectlist(floorid: int, lotid: int):
    """
    根据车场id和楼层id查询3D模型信息
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/element3dModel/selectList'
    params = {
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def element3dmodel_update(createtime: str, creator: str, elementname: str, elementtype: int, floorid: int, id: int, lotid: int, rotationangle: str, scale: str, suspendheight: str, updatetime: str, updater: str, xpoint: int, ypoint: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/element3dModel/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementbeacon_deletebatchbyids(ids: str):
    """
    批量删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/deleteBatchByIds'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementbeacon_deletebyfloorid(floorid: int):
    """
    批量删除某个楼层数据
    :param int floorid: floorId
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/deleteByFloorId'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementbeacon_exportbeaconexcel(floorid: int, id: int, lotid: int, major: str, minor: str, name: str, uuid: str):
    """
    导出数据
    :param int floorid: 楼层id
    :param int id: 主键id
    :param int lotid: 车场id lot_info id
    :param str major: 蓝牙信标的major
    :param str minor: 蓝牙信标的minor
    :param str name: 名称
    :param str uuid: 蓝牙信标的uuid
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/exportBeaconExcel'
    params = {
        'floorid': floorid,
        'id': id,
        'lotid': lotid,
        'major': major,
        'minor': minor,
        'name': name,
        'uuid': uuid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementbeacon_getbeaconbylotid(lotid: int):
    """
    根据车场id查询蓝牙设备列表
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/getBeaconByLotId'
    params = {
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementbeacon_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementbeacon_importcoordinatebyexcel(multipartfile: str, floorid: int, lotid: int):
    """
    通过excel导入坐标
    :param str multipartfile: No description
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/importCoordinateByExcel'
    params = {
        'multipartfile': multipartfile,
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementbeacon_importdatabyexcel(multipartfile: str, floorid: int, lotid: int):
    """
    通过excel导入数据
    :param str multipartfile: No description
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/importDataByExcel'
    params = {
        'multipartfile': multipartfile,
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementbeacon_importdatabylotid(lotid: int, multipartfile: str):
    """
    导入蓝牙数据（全覆盖）
    :param int lotid: lotId
    :param str multipartfile: multipartFile
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/importDataByLotId'
    params = {
        'lotid': lotid,
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementbeacon_importpointcoordinatesbyexcel(multipartfile: str, floorid: int, lotid: int):
    """
    通过excel导入点位坐标
    :param str multipartfile: No description
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/importPointCoordinatesByExcel'
    params = {
        'multipartfile': multipartfile,
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementbeacon_insert(floorid: int, id: int, lotid: int, major: str, minor: str, name: str, uuid: str, xpoint: str, ypoint: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementbeacon_insertbatch(multipartfile: str, floorid: int, lotid: int):
    """
    批量保存蓝牙数据,文件为txt格式
    :param str multipartfile: No description
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/insertBatch'
    params = {
        'multipartfile': multipartfile,
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementbeacon_selectbylotidandfloorid(floorid: int, lotid: int):
    """
    查询指定楼层所有的蓝牙信标
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/selectByLotIdAndFloorId'
    params = {
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementbeacon_selectpagelist(floorenablestatus: int, floorid: int, id: int, isinput: bool, lotid: int, major: str, minor: str, name: str, pagenumber: int, pagesize: int, uuid: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementbeacon_update(floorid: int, id: int, lotid: int, major: str, minor: str, name: str, uuid: str, xpoint: str, ypoint: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/elementBeacon/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementimpassablepath_batchsave(floorid: int, lotid: int, pathlist: list):
    """
    批量保存不可通行路网
    :param int floorid: 楼层id
    :param int lotid: 车场id
    :param list pathlist: 路网集合
    """
    url = 'http://192.168.21.249:8083' + '/elementImpassablePath/batchSave'
    params = {
        'floorid': floorid,
        'lotid': lotid,
        'pathlist': pathlist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementimpassablepath_deletebatchbyids(ids: str):
    """
    批量删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/elementImpassablePath/deleteBatchByIds'
    params = {
        'ids': ids,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementimpassablepath_deletebyid(id: int):
    """
    删除不可通行路网数据
    :param int id: id
    """
    url = 'http://192.168.21.249:8083' + '/elementImpassablePath/deleteById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementimpassablepath_exportimpassablepath():
    """
    数据同步-导出
    
    """
    url = 'http://192.168.21.249:8083' + '/elementImpassablePath/exportImpassablePath'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementimpassablepath_getbylotidandfloorid(floorid: int, lotid: int):
    """
    获取指定楼层的不可通行路网数据
    :param int floorid: 楼层id
    :param int lotid: 车场id
    """
    url = 'http://192.168.21.249:8083' + '/elementImpassablePath/getByLotIdAndFloorId'
    params = {
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementimpassablepath_importimpassablepath(multipartfile: str):
    """
    数据同步-导入
    :param str multipartfile: 导入文件
    """
    url = 'http://192.168.21.249:8083' + '/elementImpassablePath/importImpassablePath'
    params = {
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementimpassablepath_save(floorid: int, lotid: int, pathlist: list):
    """
    保存不可通行路网
    :param int floorid: 楼层id
    :param int lotid: 车场id
    :param list pathlist: 路网集合
    """
    url = 'http://192.168.21.249:8083' + '/elementImpassablePath/save'
    params = {
        'floorid': floorid,
        'lotid': lotid,
        'pathlist': pathlist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementimpassablepath_selectallbylotid(lotid: int):
    """
    获取车场所有不可通行路网数据
    :param int lotid: 车场id
    """
    url = 'http://192.168.21.249:8083' + '/elementImpassablePath/selectALLByLotId'
    params = {
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreenchild_getall():
    """
    获取所有子屏数据
    
    """
    url = 'http://192.168.21.249:8083' + '/elementScreenChild/getAll'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreenchild_getbyfloorid(floorid: int):
    """
    获取指定楼层的子屏
    :param int floorid: 楼层id
    """
    url = 'http://192.168.21.249:8083' + '/elementScreenChild/getByFloorId'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreenchild_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/elementScreenChild/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreenchild_getelementscreenchildcollection(floorid: int):
    """
    获取指定楼层整理后，子屏数据集合
    :param int floorid: 楼层id
    """
    url = 'http://192.168.21.249:8083' + '/elementScreenChild/getElementScreenChildCollection'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreenchild_listbyelementscreenid(elementscreenid: int):
    """
    根据主屏Id获取子屏信息(用于选择框)
    :param int elementscreenid: 主屏Id
    """
    url = 'http://192.168.21.249:8083' + '/elementScreenChild/listByElementScreenId'
    params = {
        'elementscreenid': elementscreenid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreenchild_update(arrowdirection: int, arrowposition: int, constantnum: int, criticalnum: int, description: str, id: int, parktype: int, relationareaidlist: str, revisenum: int, screenaddr: int, screencategory: int, screenspecies: int, screentype: int, showcolor: int, showtype: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/elementScreenChild/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def elementscreenchild_updatebatch(vo: str):
    """
    更新
    :param str vo: vo
    """
    url = 'http://192.168.21.249:8083' + '/elementScreenChild/updateBatch'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def elementscreenparkrelation_getparkidbyscreenid(screenid: int):
    """
    根据屏id获取对应的车位id
    :param int screenid: 屏id
    """
    url = 'http://192.168.21.249:8083' + '/elementScreenParkRelation/getParkIdByScreenId'
    params = {
        'screenid': screenid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreenparkrelation_selectrelatepark(elementscreenid: int):
    """
    查询可选车位和已选车位
    :param int elementscreenid: elementScreenId
    """
    url = 'http://192.168.21.249:8083' + '/elementScreenParkRelation/selectRelatePark'
    params = {
        'elementscreenid': elementscreenid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def elementscreenparkrelation_update(parkidlist: list, screenid: int):
    """
    更新
    :param list parkidlist: 车位id集合
    :param int screenid: 子屏id
    """
    url = 'http://192.168.21.249:8083' + '/elementScreenParkRelation/update'
    params = {
        'parkidlist': parkidlist,
        'screenid': screenid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def floorinfo_createflooruniqueidentification():
    """
    楼层唯一标识为空的生成唯一标识
    
    """
    url = 'http://192.168.21.249:8083' + '/floorInfo/createFloorUniqueIdentification'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def floorinfo_delete(floorid: int):
    """
    删除楼层
    :param int floorid: floorId
    """
    url = 'http://192.168.21.249:8083' + '/floorInfo/delete'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def floorinfo_flooruniquesynchronization(floorinfosynchronizationrequestvolist: str):
    """
    云端和场端楼层唯一标识同步
    :param str floorinfosynchronizationrequestvolist: floorInfoSynchronizationRequestVOList
    """
    url = 'http://192.168.21.249:8083' + '/floorInfo/floorUniqueSynchronization'
    params = {
        'floorinfosynchronizationrequestvolist': floorinfosynchronizationrequestvolist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def floorinfo_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/floorInfo/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def floorinfo_insert(floorname: str, lotid: int, remark: str, sort: int):
    """
    添加
    :param str floorname: 楼层名称
    :param int lotid: 车场id lot_info id
    :param str remark: 备注
    :param int sort: 楼层顺序（数字越大，楼层越高）
    """
    url = 'http://192.168.21.249:8083' + '/floorInfo/insert'
    params = {
        'floorname': floorname,
        'lotid': lotid,
        'remark': remark,
        'sort': sort,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def floorinfo_selectflooruniquebyother(lotcode: str):
    """
    查询云端楼层唯一标识
    :param str lotcode: 车场编码
    """
    url = 'http://192.168.21.249:8083' + '/floorInfo/selectFloorUniqueByOther'
    params = {
        'lotcode': lotcode,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def floorinfo_selectpagelist(endtime: str, floorname: str, flooruniqueidentification: str, id: int, lotid: int, pagenumber: int, pagesize: int, sort: int, starttime: str, status: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/floorInfo/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def floorinfo_update(floorname: str, id: int, lotid: int, remark: str, sort: int, status: int):
    """
    更新
    :param str floorname: 楼层名称
    :param int id: 楼层id
    :param int lotid: 场端楼层id
    :param str remark: 备注
    :param int sort: 楼层顺序（数字越大，楼层越高）
    :param int status: 状态 1启用 2停用
    """
    url = 'http://192.168.21.249:8083' + '/floorInfo/update'
    params = {
        'floorname': floorname,
        'id': id,
        'lotid': lotid,
        'remark': remark,
        'sort': sort,
        'status': status,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def floorinfo_updatescrollratio(id: int, scrollratio: int):
    """
    更新缩放比例
    :param int id: 楼层id
    :param int scrollratio: 缩放比例（%）
    """
    url = 'http://192.168.21.249:8083' + '/floorInfo/updateScrollRatio'
    params = {
        'id': id,
        'scrollratio': scrollratio,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def generalconfig_getall():
    """
    获取所有配置信息
    
    """
    url = 'http://192.168.21.249:8083' + '/generalConfig/getAll'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def generalconfig_getconfigbycode(configkey: str):
    """
    根据code获取配置
    :param str configkey: configKey
    """
    url = 'http://192.168.21.249:8083' + '/generalConfig/getConfigByCode'
    params = {
        'configkey': configkey,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def generalconfig_insert(configkey: str, configvalue: str, createtime: str, description: str, id: int, updatetime: str):
    """
    新增配置信息
    :param str configkey: 字段唯一标识，禁止重复
    :param str configvalue: 字段具体配置信息
    :param str createtime: 创建时间
    :param str description: 字段详细作用描述
    :param int id: 主键id
    :param str updatetime: 更新时间
    """
    url = 'http://192.168.21.249:8083' + '/generalConfig/insert'
    params = {
        'configkey': configkey,
        'configvalue': configvalue,
        'createtime': createtime,
        'description': description,
        'id': id,
        'updatetime': updatetime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def generalconfig_updatebyid(configkey: str, configvalue: str, createtime: str, description: str, id: int, updatetime: str):
    """
    根据ID修改对应配置
    :param str configkey: 字段唯一标识，禁止重复
    :param str configvalue: 字段具体配置信息
    :param str createtime: 创建时间
    :param str description: 字段详细作用描述
    :param int id: 主键id
    :param str updatetime: 更新时间
    """
    url = 'http://192.168.21.249:8083' + '/generalConfig/updateById'
    params = {
        'configkey': configkey,
        'configvalue': configvalue,
        'createtime': createtime,
        'description': description,
        'id': id,
        'updatetime': updatetime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def generalconfig_updateconfigbycode(configkey: str, configvalue: str):
    """
    根据code修改配置
    :param str configkey: 配置key
    :param str configvalue: 配置value
    """
    url = 'http://192.168.21.249:8083' + '/generalConfig/updateConfigByCode'
    params = {
        'configkey': configkey,
        'configvalue': configvalue,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def ground_delete(ids: str):
    """
    删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/ground/delete'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def ground_deletebyfloorid(floorid: int):
    """
    地面 - 删除某个楼层地面
    :param int floorid: floorId
    """
    url = 'http://192.168.21.249:8083' + '/ground/deleteByFloorId'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def ground_exportground():
    """
    数据同步-导出
    
    """
    url = 'http://192.168.21.249:8083' + '/ground/exportGround'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def ground_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/ground/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def ground_importground(multipartfile: str):
    """
    数据同步-导入
    :param str multipartfile: 导入文件
    """
    url = 'http://192.168.21.249:8083' + '/ground/importGround'
    params = {
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def ground_selectpagelist(control: int, elementcustomid: int, floorenablestatus: int, floorid: int, floorname: str, floorstatus: int, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, parkaddr: int, parkcategory: int, parkno: str, status: int, type: int, uniqueidentificationfield: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/ground/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def ground_update(chargingbrand: str, chargingtype: int, control: int, createtime: str, deleted: bool, devicetype: int, enable: int, floorid: int, id: int, lotid: int, name: str, parkaddr: int, parkcategory: int, parkno: str, parkinglockequipmentno: str, parkingpropertyright: str, status: int, stereoscopicparkcameraaddr: int, toward: int, type: int, updatetime: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/ground/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def ground_updategroundcoordinate(floorid: int, groundcontent: list, lotid: int):
    """
    更新地面坐标信息
    :param int floorid: 楼层id
    :param list groundcontent: 坐标列表
    :param int lotid: 车场id
    """
    url = 'http://192.168.21.249:8083' + '/ground/updateGroundCoordinate'
    params = {
        'floorid': floorid,
        'groundcontent': groundcontent,
        'lotid': lotid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def healthcheck():
    """
    healthCheck
    
    """
    url = 'http://192.168.21.249:8083' + '/healthCheck'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def imagestyles_insert(escalatorconnector: str, id: int, isshownameconnector: bool, isshownamemachine: bool, mapstylesid: int, norecordbeacon: str, passagewayconnector: str, recordbeacon: str, screenlcdurl: str, screenledurl: str, stairsconnector: str, verticalladderconnector: str, verticalmachine: str, wallmachine: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/image-styles/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def imagestyles_update(escalatorconnector: str, id: int, isshownameconnector: bool, isshownamemachine: bool, mapstylesid: int, norecordbeacon: str, passagewayconnector: str, recordbeacon: str, screenlcdurl: str, screenledurl: str, stairsconnector: str, verticalladderconnector: str, verticalmachine: str, wallmachine: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/image-styles/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def importolddata_machine(file: str):
    """
    导入找车机数据
    :param str file: No description
    """
    url = 'http://192.168.21.249:8083' + '/importOldData/machine'
    params = {
        'file': file,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def importolddata_screen(file: str):
    """
    导入主屏数据
    :param str file: No description
    """
    url = 'http://192.168.21.249:8083' + '/importOldData/screen'
    params = {
        'file': file,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def importolddata_screenchild(file: str):
    """
    导入子屏数据
    :param str file: No description
    """
    url = 'http://192.168.21.249:8083' + '/importOldData/screenChild'
    params = {
        'file': file,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def internationalization_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/internationalization/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def internationalization_insert(chinese: str, code: str, description: str, english: str, id: int, other1: str, other2: str, other3: str, other4: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/internationalization/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def internationalization_selectallfront():
    """
    获取属于前端的国际化数据
    
    """
    url = 'http://192.168.21.249:8083' + '/internationalization/selectAllFront'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def internationalization_selectpagelist(chinese: str, code: str, complete: bool, description: str, english: str, id: int, other1: str, other2: str, other3: str, other4: str, pagenumber: int, pagesize: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/internationalization/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def internationalization_update(chinese: str, code: str, description: str, english: str, id: int, other1: str, other2: str, other3: str, other4: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/internationalization/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()



def internationalizationrelation_controlstatus(id: int, status: bool):
    """
    启用/关闭语言
    :param int id: 主键
    :param bool status: 状态 0：未启用 1：启用
    """
    url = 'http://192.168.21.249:8083' + '/internationalizationRelation/controlStatus'
    params = {
        'id': id,
        'status': status,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def internationalizationrelation_exportinternational():
    """
    国际化数据excel文件导出
    
    """
    url = 'http://192.168.21.249:8083' + '/internationalizationRelation/exportInternational'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def internationalizationrelation_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/internationalizationRelation/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def internationalizationrelation_selectall():
    """
    查询所有记录
    
    """
    url = 'http://192.168.21.249:8083' + '/internationalizationRelation/selectAll'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def internationalizationrelation_selectenable():
    """
    查询启用状态的语言
    
    """
    url = 'http://192.168.21.249:8083' + '/internationalizationRelation/selectEnable'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def internationalizationrelation_update(field: str, id: int, name: str, shorthand: str, sort: int, status: bool):
    """
    更新
    :param str field: internationalization表的字段名
    :param int id: 主键id
    :param str name: 语言名称，用于显示在前端用于选择语言
    :param str shorthand: 语言简称，用于前端组件自带的国际化，如：zh_CN：简体中文  en_GB：英语
    :param int sort: 排序
    :param bool status: 状态  0：未启用   1：启用
    """
    url = 'http://192.168.21.249:8083' + '/internationalizationRelation/update'
    params = {
        'field': field,
        'id': id,
        'name': name,
        'shorthand': shorthand,
        'sort': sort,
        'status': status,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def lcdadvertisementconfig_batchdelete(ids: str):
    """
    批量删除
    :param str ids: 主键集合（逗号拼接）
    """
    url = 'http://192.168.21.249:8083' + '/lcd-advertisement-config/batchDelete'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def lcdadvertisementconfig_insert(filename: str, lcdadvertisementschemeid: int, playsort: int, remark: str):
    """
    添加
    :param str filename: 文件名
    :param int lcdadvertisementschemeid: LCD屏广告方案id
    :param int playsort: 播放顺序
    :param str remark: 备注
    """
    url = 'http://192.168.21.249:8083' + '/lcd-advertisement-config/insert'
    params = {
        'filename': filename,
        'lcdadvertisementschemeid': lcdadvertisementschemeid,
        'playsort': playsort,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def lcdadvertisementconfig_selectpagelist(lcdadvertisementschemeid: int, pagenumber: int, pagesize: int):
    """
    查看方案的广告配置
    :param int lcdadvertisementschemeid: 广告方案id
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    """
    url = 'http://192.168.21.249:8083' + '/lcd-advertisement-config/selectPageList'
    params = {
        'lcdadvertisementschemeid': lcdadvertisementschemeid,
        'pagenumber': pagenumber,
        'pagesize': pagesize,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def lcdadvertisementconfig_update(filename: str, id: int, lcdadvertisementschemeid: int, playsort: int, remark: str):
    """
    编辑
    :param str filename: 文件名
    :param int id: 主键id
    :param int lcdadvertisementschemeid: LCD屏广告方案id
    :param int playsort: 播放顺序
    :param str remark: 备注
    """
    url = 'http://192.168.21.249:8083' + '/lcd-advertisement-config/update'
    params = {
        'filename': filename,
        'id': id,
        'lcdadvertisementschemeid': lcdadvertisementschemeid,
        'playsort': playsort,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def lcdadvertisementscheme_batchdelete(ids: str):
    """
    批量删除
    :param str ids: 主键集合（逗号拼接）
    """
    url = 'http://192.168.21.249:8083' + '/lcd-advertisement-scheme/batchDelete'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def lcdadvertisementscheme_insert(carouselseconds: int, name: str, species: int):
    """
    添加
    :param int carouselseconds: 轮播时间 单位s(秒)
    :param str name: 方案名称
    :param int species: 类型 1：图片 2：视频
    """
    url = 'http://192.168.21.249:8083' + '/lcd-advertisement-scheme/insert'
    params = {
        'carouselseconds': carouselseconds,
        'name': name,
        'species': species,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def lcdadvertisementscheme_selectpagelist(endtime: str, id: int, name: str, pagenumber: int, pagesize: int, species: int, starttime: str):
    """
    分页查询
    :param str endtime: 结束时间
    :param int id: 主键id
    :param str name: 方案名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int species: 类型 1：图片 2：视频
    :param str starttime: 开始时间
    """
    url = 'http://192.168.21.249:8083' + '/lcd-advertisement-scheme/selectPageList'
    params = {
        'endtime': endtime,
        'id': id,
        'name': name,
        'pagenumber': pagenumber,
        'pagesize': pagesize,
        'species': species,
        'starttime': starttime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def lcdadvertisementscheme_update(carouselseconds: int, id: int, name: str, species: int):
    """
    编辑
    :param int carouselseconds: 轮播时间 单位s(秒)
    :param int id: 主键id
    :param str name: 方案名称
    :param int species: 类型 1：图片 2：视频
    """
    url = 'http://192.168.21.249:8083' + '/lcd-advertisement-scheme/update'
    params = {
        'carouselseconds': carouselseconds,
        'id': id,
        'name': name,
        'species': species,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def lcdscreenconfig_exchangeorder(elementscreenid: int):
    """
    对调屏顺序（目前只针对于双拼接屏）
    :param int elementscreenid: 主屏id
    """
    url = 'http://192.168.21.249:8083' + '/lcd-screen-config/exchangeOrder'
    params = {
        'elementscreenid': elementscreenid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def lcdscreenconfig_getall(elementscreenip: str):
    """
    查询车场所有屏信息
    :param str elementscreenip: 查询屏IP(不传IP值则默认查询所有数据)
    """
    url = 'http://192.168.21.249:8083' + '/lcd-screen-config/getAll'
    params = {
        'elementscreenip': elementscreenip,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def lcdscreenconfig_noticetest(elementscreenids: str, issuedtype: int):
    """
    全场屏指令下发测试接口
    :param str elementscreenids: 屏id集合,string类型以,分隔
    :param int issuedtype: 下发类型(1:测试指令，2;正常屏统计)
    """
    url = 'http://192.168.21.249:8083' + '/lcd-screen-config/noticeTest'
    params = {
        'elementscreenids': elementscreenids,
        'issuedtype': issuedtype,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def lightschemecontroller_cancel(id: int):
    """
    取消车位灯方案
    :param int id: id
    """
    url = 'http://192.168.21.249:8083' + '/lightSchemeController/cancel'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def lightschemecontroller_copy(id: int):
    """
    复制车位灯方案
    :param int id: No description
    """
    url = 'http://192.168.21.249:8083' + '/lightSchemeController/copy'
    params = {
        'id': id,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def lightschemecontroller_insert(elementparkids: list, freecolor: int, issuancetype: int, lightaddr: int, lightschemenname: str, lighttype: int, occupycolor: int, sendtime: str, systemtype: int, warningcolor: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/lightSchemeController/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def lightschemecontroller_selectpagelist(endcreatetime: str, endsendtime: str, id: int, lightaddr: int, lighttype: int, name: str, pagenumber: int, pagesize: int, parkno: str, startcreatetime: str, startsendtime: str, status: int, systemtype: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/lightSchemeController/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def lightschemecontroller_update(elementparkids: list, freecolor: int, issuancetype: int, lightaddr: int, lightschemenname: str, lighttype: int, occupycolor: int, sendtime: str, systemtype: int, warningcolor: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/lightSchemeController/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def lightschemegroup_deletebatch(idlist: str):
    """
    批量删除
    :param str idlist: idList
    """
    url = 'http://192.168.21.249:8083' + '/lightSchemeGroup/deleteBatch'
    params = {
        'idlist': idlist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def lightschemegroup_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/lightSchemeGroup/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def lightschemegroup_insert(cameraip: str, detectordevicetype: int, detectordsp: int, detectorip: str, detectornodedsp: int, devicetype: int, freecolor: int, groupname: str, id: int, lightaddr: int, lighttype: int, occupycolor: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/lightSchemeGroup/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def lightschemegroup_selectpagelist(endtime: str, groupname: str, lightaddr: int, pagenumber: int, pagesize: int, starttime: str):
    """
    分页查询
    :param str endtime: 创建时间-结束时间
    :param str groupname: 分组名称
    :param int lightaddr: 车位灯地址
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str starttime: 创建时间-开始时间
    """
    url = 'http://192.168.21.249:8083' + '/lightSchemeGroup/selectPageList'
    params = {
        'endtime': endtime,
        'groupname': groupname,
        'lightaddr': lightaddr,
        'pagenumber': pagenumber,
        'pagesize': pagesize,
        'starttime': starttime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def lightschemegroup_selectrelatepark(lightschemegroupid: int):
    """
    查询可选车位和已选车位
    :param int lightschemegroupid: lightSchemeGroupId
    """
    url = 'http://192.168.21.249:8083' + '/lightSchemeGroup/selectRelatePark'
    params = {
        'lightschemegroupid': lightschemegroupid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def lightschemegroup_update(cameraip: str, detectordevicetype: int, detectordsp: int, detectorip: str, detectornodedsp: int, devicetype: int, freecolor: int, groupname: str, id: int, lightaddr: int, lighttype: int, occupycolor: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/lightSchemeGroup/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def lightschemegroup_updateparkrelate(lightschemegroupid: int, parkidlist: list):
    """
    更新车位关联信息
    :param int lightschemegroupid: 分组车位灯方案id
    :param list parkidlist: 车位id集合
    """
    url = 'http://192.168.21.249:8083' + '/lightSchemeGroup/updateParkRelate'
    params = {
        'lightschemegroupid': lightschemegroupid,
        'parkidlist': parkidlist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def loginlog_selectpagelist(endtime: str, loginip: str, pagenumber: int, pagesize: int, starttime: str, useraccount: str, username: str, userphone: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/login-log/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def lotinfo_deletebatch(ids: str):
    """
    多车场 - 删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/lot-info/deleteBatch'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def lotinfo_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/lot-info/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def lotinfo_getmsg(lotcode: str):
    """
    获取车场信息
    :param str lotcode: lotCode
    """
    url = 'http://192.168.21.249:8083' + '/lot-info/getMsg'
    params = {
        'lotcode': lotcode,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def lotinfo_insert(addr: str, decodingstatus: int, deviceid: str, deviceipprefix: str, id: int, lisenceauthorizecode: str, lisencetrialperiod: str, lotcode: str, lotname: str, machinedebug: int, maptype: int, parkrepeatswitch: int, secret: str, serverip: str, systemtype: int, tel: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/lot-info/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def lotinfo_lotinfocheck(lotid: int):
    """
    车场配置检测
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/lot-info/lotInfoCheck'
    params = {
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def lotinfo_save(addr: str, deviceipprefix: str, id: int, lotcode: str, lotname: str, maptype: int, parkrepeatswitch: int, serverip: str, systemtype: int, tel: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/lot-info/save'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def lotinfo_selectlist(createenddatetime: str, createstartdatetime: str, lotcode: int, lotname: str, pagenumber: int, pagesize: int, status: int):
    """
    多车场 - 分页查询
    :param str createenddatetime: 创建时间结束时间
    :param str createstartdatetime: 创建时间开始时间
    :param int lotcode: 车场编码
    :param str lotname: 车场名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int status: 启用状态 0 未启用  1 启用
    """
    url = 'http://192.168.21.249:8083' + '/lot-info/selectList'
    params = {
        'createenddatetime': createenddatetime,
        'createstartdatetime': createstartdatetime,
        'lotcode': lotcode,
        'lotname': lotname,
        'pagenumber': pagenumber,
        'pagesize': pagesize,
        'status': status,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def lotinfo_update(addr: str, decodingstatus: int, deviceid: str, deviceipprefix: str, id: int, lisenceauthorizecode: str, lisencetrialperiod: str, lotcode: str, lotname: str, machinedebug: int, maptype: int, parkrepeatswitch: int, secret: str, serverip: str, systemtype: int, tel: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/lot-info/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def lotinfo_updateauthorizecode(authorizecode: str):
    """
    更新当前车场授权码(返回true为保存成功，返回false为保存失败)
    :param str authorizecode: Lisence授权码
    """
    url = 'http://192.168.21.249:8083' + '/lot-info/updateAuthorizeCode'
    params = {
        'authorizecode': authorizecode,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def machineadvertisementconfig_batchdelete(ids: str):
    """
    批量删除
    :param str ids: 主键集合（逗号拼接）
    """
    url = 'http://192.168.21.249:8083' + '/machine-advertisement-config/batchDelete'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def machineadvertisementconfig_savemachineadvertisementconfig(id: int, machineadschemeid: int, machineip: str, screenadschemeid: int, type: int):
    """
    保存
    :param int id: 主键id
    :param int machineadschemeid: 找车机广告方案id
    :param str machineip: 找车机ip
    :param int screenadschemeid: 广告屏广告方案id
    :param int type: 类型 0-全局 1-单独配置
    """
    url = 'http://192.168.21.249:8083' + '/machine-advertisement-config/saveMachineAdvertisementConfig'
    params = {
        'id': id,
        'machineadschemeid': machineadschemeid,
        'machineip': machineip,
        'screenadschemeid': screenadschemeid,
        'type': type,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def machineadvertisementconfig_selectpagelist(machineadschemeid: int, machineip: str, pagenumber: int, pagesize: int, screenadschemeid: int, type: int):
    """
    分页查询
    :param int machineadschemeid: 找车机广告方案id
    :param str machineip: 找车机ip
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int screenadschemeid: 广告屏广告方案id
    :param int type: 类型 0-全局 1-单独配置
    """
    url = 'http://192.168.21.249:8083' + '/machine-advertisement-config/selectPageList'
    params = {
        'machineadschemeid': machineadschemeid,
        'machineip': machineip,
        'pagenumber': pagenumber,
        'pagesize': pagesize,
        'screenadschemeid': screenadschemeid,
        'type': type,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def mapstyles_batchdelete(ids: str):
    """
    批量删除
    :param str ids: 主键集合（逗号拼接）
    """
    url = 'http://192.168.21.249:8083' + '/map-styles/batchDelete'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def mapstyles_batchdisable(disable: bool, ids: str):
    """
    批量禁用、启用
    :param bool disable: true 禁用 false 启用
    :param str ids: 主键集合（逗号拼接）
    """
    url = 'http://192.168.21.249:8083' + '/map-styles/batchDisable'
    params = {
        'disable': disable,
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def mapstyles_copy(id: int):
    """
    复制
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/map-styles/copy'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def mapstyles_exporttotxt():
    """
    导出文本格式的数据
    
    """
    url = 'http://192.168.21.249:8083' + '/map-styles/exportToTxt'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def mapstyles_generatemapstylefile(id: int, lotid: int):
    """
    生成地图样式json文件到指定目录
    :param int id: id
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/map-styles/generateMapStyleFile'
    params = {
        'id': id,
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def mapstyles_getmapstylesdetail(id: int, lotid: int):
    """
    根据mystyleId获取地图样式的详细信息，当id为null返回默认样式
    :param int id: 主键
    :param int lotid: 车场id
    """
    url = 'http://192.168.21.249:8083' + '/map-styles/getMapStylesDetail'
    params = {
        'id': id,
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def mapstyles_importbytxt(multipartfile: str):
    """
    通过文本导入数据
    :param str multipartfile: multipartFile
    """
    url = 'http://192.168.21.249:8083' + '/map-styles/importByTxt'
    params = {
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def mapstyles_insert(lotid: int, name: str, remark: str):
    """
    添加
    :param int lotid: 车场id
    :param str name: 样式名称
    :param str remark: 备注
    """
    url = 'http://192.168.21.249:8083' + '/map-styles/insert'
    params = {
        'lotid': lotid,
        'name': name,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def mapstyles_selectisshowcontrol():
    """
    找车机 - 控制是否显示名称
    
    """
    url = 'http://192.168.21.249:8083' + '/map-styles/selectIsShowControl'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def mapstyles_selectpagelist(deleted: bool, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, remark: str):
    """
    分页查询
    :param bool deleted: 是否禁用（0：禁用，1：启用）
    :param int id: 主键id
    :param int lotid: 车场编码
    :param str name: 样式名称
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str remark: 备注
    """
    url = 'http://192.168.21.249:8083' + '/map-styles/selectPageList'
    params = {
        'deleted': deleted,
        'id': id,
        'lotid': lotid,
        'name': name,
        'pagenumber': pagenumber,
        'pagesize': pagesize,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def mapstyles_update(id: int, name: str, remark: str):
    """
    编辑
    :param int id: 主键id
    :param str name: 样式名称
    :param str remark: 备注
    """
    url = 'http://192.168.21.249:8083' + '/map-styles/update'
    params = {
        'id': id,
        'name': name,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def mapinfo_backupmap(lotid: int):
    """
    场端地图备份
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/mapInfo/backupMap'
    params = {
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def mapinfo_exportmap(lotid: int):
    """
    场端地图数据导出（云端导入用）
    :param int lotid: 车场id
    """
    url = 'http://192.168.21.249:8083' + '/mapInfo/exportMap'
    params = {
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def mapinfo_exportmapdata():
    """
    场端地图导出
    
    """
    url = 'http://192.168.21.249:8083' + '/mapInfo/exportMapData'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def mapinfo_getallfloordata(floorid: int, lotid: int):
    """
    场端管理后台实时获取地图数据
    :param int floorid: floorId
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/mapInfo/getAllFloorData'
    params = {
        'floorid': floorid,
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def mapinfo_getmachineallfloordata(lotcode: str, realtimedata: bool):
    """
    找车机获取地图数据（优先内存获取,对外提供参数用lotCode）
    :param str lotcode: lotCode
    :param bool realtimedata: realTimeData
    """
    url = 'http://192.168.21.249:8083' + '/mapInfo/getMachineAllFloorData'
    params = {
        'lotcode': lotcode,
        'realtimedata': realtimedata,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def mapinfo_refreshmapdata(lotid: int):
    """
    刷新地图数据到内存（提供给找车机）
    :param int lotid: lotId
    """
    url = 'http://192.168.21.249:8083' + '/mapInfo/refreshMapData'
    params = {
        'lotid': lotid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def mapinfo_restoremap(lotid: int, multipartfile: str):
    """
    场端地图数据还原
    :param int lotid: lotId
    :param str multipartfile: multipartFile
    """
    url = 'http://192.168.21.249:8083' + '/mapInfo/restoreMap'
    params = {
        'lotid': lotid,
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def nodedevice_deletebatch(ids: str):
    """
    批量删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/nodeDevice/deleteBatch'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def nodedevice_deletebyfloorid(floorid: int):
    """
    节点设备 - 清空列表数据
    :param int floorid: floorId
    """
    url = 'http://192.168.21.249:8083' + '/nodeDevice/deleteByFloorId'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def nodedevice_importdatabyexcel(multipartfile: str):
    """
    通过excel导入数据
    :param str multipartfile: No description
    """
    url = 'http://192.168.21.249:8083' + '/nodeDevice/importDataByExcel'
    params = {
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def nodedevice_save(addr: str, devicetype: int, floorid: int, id: str, relateparknum: int, remark: str):
    """
    新增
    :param str addr: 设备ip转化后的数字，用于与设备建立连接
    :param int devicetype: 设备类型
    :param int floorid: 楼层id
    :param str id: id
    :param int relateparknum: 关联车位数
    :param str remark: 备注
    """
    url = 'http://192.168.21.249:8083' + '/nodeDevice/save'
    params = {
        'addr': addr,
        'devicetype': devicetype,
        'floorid': floorid,
        'id': id,
        'relateparknum': relateparknum,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def nodedevice_selectpagelist(addr: int, devicetype: int, endtime: str, floorid: int, id: int, lotid: int, pagenumber: int, pagesize: int, starttime: str, status: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/nodeDevice/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def nodedevice_update(addr: str, devicetype: int, floorid: int, id: str, relateparknum: int, remark: str):
    """
    修改
    :param str addr: 设备ip转化后的数字，用于与设备建立连接
    :param int devicetype: 设备类型
    :param int floorid: 楼层id
    :param str id: id
    :param int relateparknum: 关联车位数
    :param str remark: 备注
    """
    url = 'http://192.168.21.249:8083' + '/nodeDevice/update'
    params = {
        'addr': addr,
        'devicetype': devicetype,
        'floorid': floorid,
        'id': id,
        'relateparknum': relateparknum,
        'remark': remark,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def overnight_export(areaidlist: list, flooridlist: list, pagenumber: int, pagesize: int, parkno: str, recordendtime: str, recordstarttime: str):
    """
    过夜车数据导出
    :param list areaidlist: 区域ID集合
    :param list flooridlist: 楼层ID集合
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位编号
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    """
    url = 'http://192.168.21.249:8083' + '/overnight/export'
    params = {
        'areaidlist': areaidlist,
        'flooridlist': flooridlist,
        'pagenumber': pagenumber,
        'pagesize': pagesize,
        'parkno': parkno,
        'recordendtime': recordendtime,
        'recordstarttime': recordstarttime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def overnight_getdatabyarea(areaidlist: list, recordendtime: str, recordstarttime: str):
    """
    按照区域分组查询
    :param list areaidlist: 区域ID集合
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    """
    url = 'http://192.168.21.249:8083' + '/overnight/getDataByArea'
    params = {
        'areaidlist': areaidlist,
        'recordendtime': recordendtime,
        'recordstarttime': recordstarttime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def overnight_getdatabyfloor(recordendtime: str, recordstarttime: str):
    """
    按照楼层分组查询
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    """
    url = 'http://192.168.21.249:8083' + '/overnight/getDataByFloor'
    params = {
        'recordendtime': recordendtime,
        'recordstarttime': recordstarttime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def overnight_selectpagelist(areaidlist: list, flooridlist: list, pagenumber: int, pagesize: int, parkno: str, recordendtime: str, recordstarttime: str):
    """
    分页查询过夜车数据
    :param list areaidlist: 区域ID集合
    :param list flooridlist: 楼层ID集合
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位编号
    :param str recordendtime: 记录结束时间
    :param str recordstarttime: 记录开始时间
    """
    url = 'http://192.168.21.249:8083' + '/overnight/selectPageList'
    params = {
        'areaidlist': areaidlist,
        'flooridlist': flooridlist,
        'pagenumber': pagenumber,
        'pagesize': pagesize,
        'parkno': parkno,
        'recordendtime': recordendtime,
        'recordstarttime': recordstarttime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_addbatchpark(floorid: int, lotid: int, parkcontent: list):
    """
    批量新增车位
    :param int floorid: No description
    :param int lotid: No description
    :param list parkcontent: No description
    """
    url = 'http://192.168.21.249:8083' + '/park/addBatchPark'
    params = {
        'floorid': floorid,
        'lotid': lotid,
        'parkcontent': parkcontent,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_createparkuniqueidentification():
    """
    车位唯一标识为空的生成唯一标识
    
    """
    url = 'http://192.168.21.249:8083' + '/park/createParkUniqueIdentification'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_delete(ids: str):
    """
    删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/park/delete'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_deletebyfloorid(floorid: int):
    """
    删除楼层全部车位信息
    :param int floorid: floorId
    """
    url = 'http://192.168.21.249:8083' + '/park/deleteByFloorId'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_deletepresentcarandupdatestatus(presentcarrecordid: int):
    """
    清除当前车位的车辆信息
    :param int presentcarrecordid: 在场车辆的记录id
    """
    url = 'http://192.168.21.249:8083' + '/park/deletePresentCarAndUpdateStatus'
    params = {
        'presentcarrecordid': presentcarrecordid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_exportdatasynchronization():
    """
    数据同步-导出
    
    """
    url = 'http://192.168.21.249:8083' + '/park/exportDataSynchronization'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_exportparkinglot(control: int, elementcustomid: int, floorenablestatus: int, floorid: int, floorname: str, floorstatus: int, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, parkaddr: int, parkcategory: int, parkno: str, status: int, type: int, uniqueidentificationfield: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/park/exportParkingLot'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def park_getallparkinfo():
    """
    获取车位-楼层-区域信息
    
    """
    url = 'http://192.168.21.249:8083' + '/park/getAllParkInfo'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_getallparkinfowithoutstereoscopic():
    """
    获取所有车位数据(过滤已绑定立体车位)
    
    """
    url = 'http://192.168.21.249:8083' + '/park/getAllParkInfoWithOutStereoscopic'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/park/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_getelementparkandpresentcarinfo(id: int):
    """
    得到车位和当前车辆的信息
    :param int id: 车位主键id
    """
    url = 'http://192.168.21.249:8083' + '/park/getElementParkAndPresentCarInfo'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_getparkinfo(areaname: str, floorname: str, parkno: str):
    """
    根据车位编号查询车位信息
    :param str areaname: areaName
    :param str floorname: floorName
    :param str parkno: parkNo
    """
    url = 'http://192.168.21.249:8083' + '/park/getParkInfo'
    params = {
        'areaname': areaname,
        'floorname': floorname,
        'parkno': parkno,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_getparktotalusagerate():
    """
    大屏-车场总泊位使用率
    
    """
    url = 'http://192.168.21.249:8083' + '/park/getParkTotalUsageRate'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_getparkingcapture(parkaddr: int):
    """
    根据车位地址查询车位相机抓拍内容
    :param int parkaddr: parkAddr
    """
    url = 'http://192.168.21.249:8083' + '/park/getParkingCapture'
    params = {
        'parkaddr': parkaddr,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_importdatasynchronization(lotid: int, multipartfile: str):
    """
    数据同步-导入
    :param int lotid: lotId
    :param str multipartfile: 导入文件
    """
    url = 'http://192.168.21.249:8083' + '/park/importDataSynchronization'
    params = {
        'lotid': lotid,
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_importparkinglot(floorid: int, lotid: int, multipartfile: str):
    """
    车位数据excel文件导入
    :param int floorid: floorId
    :param int lotid: lotId
    :param str multipartfile: 导入文件
    """
    url = 'http://192.168.21.249:8083' + '/park/importParkingLot'
    params = {
        'floorid': floorid,
        'lotid': lotid,
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_initpostparkingspaceinfo():
    """
    initPostParkingSpaceInfo
    
    """
    url = 'http://192.168.21.249:8083' + '/park/initPostParkingSpaceInfo'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_listelementpark(chargingbrand: str, chargingtype: int, control: int, createtime: str, deleted: bool, devicetype: int, enable: int, floorid: int, id: int, lotid: int, name: str, parkaddr: int, parkcategory: int, parkno: str, parkinglockequipmentno: str, parkingpropertyright: str, status: int, stereoscopicparkcameraaddr: int, toward: int, type: int, updatetime: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/park/listElementPark'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def park_listelementparkusagerate(floorid: int, querytype: str):
    """
    大屏-车位占用率集合
    :param int floorid: 楼层id，类型为area时必传
    :param str querytype: 查询类型（floor-楼层，area-区域）
    """
    url = 'http://192.168.21.249:8083' + '/park/listElementParkUsageRate'
    params = {
        'floorid': floorid,
        'querytype': querytype,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_movepark(id: int, pointdtos: list):
    """
    2D地图编辑 - 移动车位
    :param int id: 车位id
    :param list pointdtos: 移动后新的车位坐标
    """
    url = 'http://192.168.21.249:8083' + '/park/movePark'
    params = {
        'id': id,
        'pointdtos': pointdtos,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_parkrelatearea(areaid: int, relateparkids: list, unrelateparkids: list):
    """
    车位关联 - 取消关联区域
    :param int areaid: No description
    :param list relateparkids: No description
    :param list unrelateparkids: No description
    """
    url = 'http://192.168.21.249:8083' + '/park/parkRelateArea'
    params = {
        'areaid': areaid,
        'relateparkids': relateparkids,
        'unrelateparkids': unrelateparkids,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_pushparkcamera(parkingip: str, parkingport: int):
    """
    车位相机照片抓拍指令下发
    :param str parkingip: parkingIp
    :param int parkingport: parkingPort
    """
    url = 'http://192.168.21.249:8083' + '/park/pushParkCamera'
    params = {
        'parkingip': parkingip,
        'parkingport': parkingport,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_selectfaultpark(floorid: int):
    """
    查询故障的车位id
    :param int floorid: 楼层id
    """
    url = 'http://192.168.21.249:8083' + '/park/selectFaultPark'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_selectofflinepark(floorid: int):
    """
    查询掉线的车位
    :param int floorid: 楼层id
    """
    url = 'http://192.168.21.249:8083' + '/park/selectOffLinePark'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_selectpagelist(control: int, elementcustomid: int, floorenablestatus: int, floorid: int, floorname: str, floorstatus: int, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, parkaddr: int, parkcategory: int, parkno: str, status: int, type: int, uniqueidentificationfield: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/park/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def park_selectpagetidylist(control: int, elementcustomid: int, floorenablestatus: int, floorid: int, floorname: str, floorstatus: int, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, parkaddr: int, parkcategory: int, parkno: str, status: int, type: int, uniqueidentificationfield: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/park/selectPageTidyList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def park_selectwarningpark(floorid: int):
    """
    查询正在告警的车位id
    :param int floorid: 楼层id
    """
    url = 'http://192.168.21.249:8083' + '/park/selectWarningPark'
    params = {
        'floorid': floorid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def park_synchronousparkaddr():
    """
    同步相机上报车位信息
    
    """
    url = 'http://192.168.21.249:8083' + '/park/synchronousParkAddr'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_test():
    """
    test
    
    """
    url = 'http://192.168.21.249:8083' + '/park/test'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_update(chargingbrand: str, chargingtype: int, control: int, createtime: str, deleted: bool, devicetype: int, enable: int, floorid: int, id: int, lotid: int, name: str, parkaddr: int, parkcategory: int, parkno: str, parkinglockequipmentno: str, parkingpropertyright: str, status: int, stereoscopicparkcameraaddr: int, toward: int, type: int, updatetime: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/park/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def park_updatebatch(params: str):
    """
    根据id批量更新车位编号/车位地址
    :param str params: params
    """
    url = 'http://192.168.21.249:8083' + '/park/updateBatch'
    params = {
        'params': params,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_updateelementparkcontrolandstatus(areaid: int, control: int, floorid: int, id: int, intime: str, lotid: int, parkaddr: int, plateno: str, presentcarrecordid: int, status: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/park/updateElementParkControlAndStatus'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def park_updatepark(areaid: int, id: int, parkcategory: int, parkno: str):
    """
    车场大屏-修改车位信息
    :param int areaid: No description
    :param int id: No description
    :param int parkcategory: No description
    :param str parkno: No description
    """
    url = 'http://192.168.21.249:8083' + '/park/updatePark'
    params = {
        'areaid': areaid,
        'id': id,
        'parkcategory': parkcategory,
        'parkno': parkno,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def park_updateparkingcapture(parkaddr: int):
    """
    清理车位相机抓拍内容
    :param int parkaddr: parkAddr
    """
    url = 'http://192.168.21.249:8083' + '/park/updateParkingCapture'
    params = {
        'parkaddr': parkaddr,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def parkconfig_syncparkconfig(file: str, coordinates: str):
    """
    旧版寻车厂配置转换新版寻车配置
    :param str file: No description
    :param str coordinates: 给出三组对应坐标，example：[[188,291,-125090.5,37856.5],[490,727,-46837.5,-76247],[895,577,59785.5,-38202]]  [188,291,-125090.5,37856.5]标识2D坐标为188,291 映射的3D为-125090.5,37856.5
    """
    url = 'http://192.168.21.249:8083' + '/parkConfig/syncParkConfig'
    params = {
        'file': file,
        'coordinates': coordinates,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def parkinglightscheme_batchdelete(ids: str):
    """
    批量删除
    :param str ids: 主键集合（逗号拼接）
    """
    url = 'http://192.168.21.249:8083' + '/parking-light-scheme/batchDelete'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def parkinglightscheme_insert(freecolor: int, lighttype: int, lotid: int, name: str, occupycolor: int, parkinglightarearelationlist: list, type: int, warningcolor: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/parking-light-scheme/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def parkinglightscheme_listrelatedarea(id: int):
    """
    关联区域集合
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/parking-light-scheme/listRelatedArea'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def parkinglightscheme_selectpagelist(endtime: str, id: int, lotid: int, name: str, pagenumber: int, pagesize: int, parkinglightarearelationlist: list, starttime: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/parking-light-scheme/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def parkinglightscheme_update(freecolor: int, id: int, lighttype: int, lotid: int, name: str, occupycolor: int, parkinglightarearelationlist: list, type: int, warningcolor: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/parking-light-scheme/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def permissions_disable(id: int):
    """
    关闭菜单
    :param int id: 主键id
    """
    url = 'http://192.168.21.249:8083' + '/permissions/disable'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def permissions_enable(id: int):
    """
    打开菜单
    :param int id: 主键id
    """
    url = 'http://192.168.21.249:8083' + '/permissions/enable'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def permissions_insert(icon: str, id: int, internationalizationcode: str, linkway: int, menutype: int, name: str, router: str, sort: int, status: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/permissions/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def permissions_insertchildmenu(id: int, internationalizationcode: str, linkway: int, menutype: int, name: str, parentid: int, router: str, sort: int, status: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/permissions/insertChildMenu'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def permissions_querypermission(name: str, router: str):
    """
    条件查询
    :param str name: No description
    :param str router: No description
    """
    url = 'http://192.168.21.249:8083' + '/permissions/queryPermission'
    params = {
        'name': name,
        'router': router,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def permissions_selectenablemenu():
    """
    查询所有开启的菜单
    
    """
    url = 'http://192.168.21.249:8083' + '/permissions/selectEnableMenu'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def permissions_selectlist():
    """
    查询
    
    """
    url = 'http://192.168.21.249:8083' + '/permissions/selectList'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def permissions_update(icon: str, id: int, internationalizationcode: str, linkway: int, menutype: int, name: str, router: str, sort: int, status: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/permissions/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def permissions_updatechildmenu(id: int, internationalizationcode: str, linkway: int, menutype: int, name: str, parentid: int, router: str, sort: int, status: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/permissions/updateChildMenu'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def presentcarplaterecord_listpresentcarplatebyid(id: int):
    """
    在场车辆车牌记录列表
    :param int id: 在场车停车记录id
    """
    url = 'http://192.168.21.249:8083' + '/present-car-plate-record/listPresentCarPlateById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def presentcarrecord_export(areaname: str, elementparkcontrol: int, floorid: int, inendtime: str, instarttime: str, intype: int, lotid: int, pagenumber: int, pagesize: int, parkaddr: str, parkno: str, parkstatus: int, plateno: str, specialdata: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/present-car-record/export'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def presentcarrecord_listpresentcar(areaname: str, elementparkcontrol: int, floorid: int, inendtime: str, instarttime: str, intype: int, lotid: int, pagenumber: int, pagesize: int, parkaddr: str, parkno: str, parkstatus: int, plateno: str, specialdata: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/present-car-record/listPresentCar'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def presentcarrecord_selectpagelist(areaname: str, elementparkcontrol: int, floorid: int, inendtime: str, instarttime: str, intype: int, lotid: int, pagenumber: int, pagesize: int, parkaddr: str, parkno: str, parkstatus: int, plateno: str, specialdata: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/present-car-record/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def presentcarrecordarea_selectpagelist(areaname: str, endtime: str, floorid: int, id: int, pagenumber: int, pagesize: int, plateno: str, starttime: str):
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
    """
    url = 'http://192.168.21.249:8083' + '/presentCarRecordArea/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def role_deletesoftinids(ids: str):
    """
    批量删除
    :param str ids: 主键
    """
    url = 'http://192.168.21.249:8083' + '/role/deleteSoftInIds'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def role_disable(id: int):
    """
    禁用
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/role/disable'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def role_enable(id: int):
    """
    启用
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/role/enable'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def role_getall():
    """
    查询所有记录
    
    """
    url = 'http://192.168.21.249:8083' + '/role/getAll'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def role_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/role/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def role_insert(description: str, id: int, name: str):
    """
    添加
    :param str description: 备注
    :param int id: 主键
    :param str name: 角色名称
    """
    url = 'http://192.168.21.249:8083' + '/role/insert'
    params = {
        'description': description,
        'id': id,
        'name': name,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def role_update(description: str, id: int, name: str):
    """
    更新
    :param str description: 备注
    :param int id: 主键
    :param str name: 角色名称
    """
    url = 'http://192.168.21.249:8083' + '/role/update'
    params = {
        'description': description,
        'id': id,
        'name': name,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def rolepermissionrelation_setpermissions(menuidlist: list, roleid: int):
    """
    设置权限
    :param list menuidlist: 菜单id集合
    :param int roleid: 角色id
    """
    url = 'http://192.168.21.249:8083' + '/rolePermissionRelation/setPermissions'
    params = {
        'menuidlist': menuidlist,
        'roleid': roleid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def schedule_getconfig():
    """
    参数配置 - 查询
    
    """
    url = 'http://192.168.21.249:8083' + '/schedule/getConfig'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def schedule_parkinitreport():
    """
    车位状态初始化上报
    
    """
    url = 'http://192.168.21.249:8083' + '/schedule/parkInitReport'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def schedule_saveconfig(areaparkimgduration: int, areapushswitch: int, cleanareapicture: int, cleanrecognitiontable: int, cleanstereoscopicparkduration: int, cleantemppicture: int, emptyparkpushlot: str, emptyparkpushswitch: int, emptyparkpushurl: str, freespacenumswitch: int, lightschemeduration: int, parkchangepushlot: str, parkchangepushswitch: int, parkchangepushurl: str, parkimgduration: int, platematchrule: int, postbaseinfo: list, postbusinout: int, postnodedevicestatus: int, postnodedeviceurl: str, queryrecognizerecord: int, tankwarnpushswitch: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/schedule/saveConfig'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def serverlog_downloadlog(filename: str, filepath: str):
    """
    下载日志
    :param str filename: fileName
    :param str filepath: filePath
    """
    url = 'http://192.168.21.249:8083' + '/server-log/downloadLog'
    params = {
        'filename': filename,
        'filepath': filepath,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def serverlog_refreshserverlog():
    """
    刷新服务日志
    
    """
    url = 'http://192.168.21.249:8083' + '/server-log/refreshServerLog'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def serverlog_selectpagelist(endtime: str, filename: str, logtime: str, pagenumber: int, pagesize: int, starttime: str):
    """
    分页查询
    :param str endtime: 结束时间
    :param str filename: 文件名
    :param str logtime: 日志时间
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str starttime: 开始时间
    """
    url = 'http://192.168.21.249:8083' + '/server-log/selectPageList'
    params = {
        'endtime': endtime,
        'filename': filename,
        'logtime': logtime,
        'pagenumber': pagenumber,
        'pagesize': pagesize,
        'starttime': starttime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def sync_convertcoordinate(multipartfile: str):
    """
    上传excel，返回转化后的坐标
    :param str multipartfile: multipartFile
    """
    url = 'http://192.168.21.249:8083' + '/sync/convertCoordinate'
    params = {
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def sync_downloadtemplate():
    """
    下载excel模板
    
    """
    url = 'http://192.168.21.249:8083' + '/sync/downloadTemplate'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def sync_test(list: str):
    """
    转换坐标 南昌用
    :param str list: list
    """
    url = 'http://192.168.21.249:8083' + '/sync/test'
    params = {
        'list': list,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def sync_test1():
    """
    转换坐标 鄱阳湖 顺时针90度
    
    """
    url = 'http://192.168.21.249:8083' + '/sync/test1'
    params = {
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def sync_uploadmessage(floorid: int, lotid: int, multipartfile: str):
    """
    上传excel，把excel里的数据更新到对应车位
    :param int floorid: floorId
    :param int lotid: lotId
    :param str multipartfile: multipartFile
    """
    url = 'http://192.168.21.249:8083' + '/sync/uploadMessage'
    params = {
        'floorid': floorid,
        'lotid': lotid,
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def taskmanage_resetall():
    """
    重新加载所有定时任务
    
    """
    url = 'http://192.168.21.249:8083' + '/taskManage/resetAll'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_checkunifiedinterstatus():
    """
    检查统一接口链接状态；1为连通
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/checkUnifiedInterStatus'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_clearareaenterparkrecord():
    """
    清除区域进出车记录
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/clearAreaEnterParkRecord'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_clearareapicture():
    """
    区域照片清理定时接口
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/clearAreaPicture'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_clearlightschemehistoryrecord():
    """
    清除车位灯方案记录
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/clearLightSchemeHistoryRecord'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_clearparkimg():
    """
    清除车位图片
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/clearParkImg'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_getcarinout():
    """
    进出车流量接口测试
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/getCarInOut'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_getfindcarmachinelist():
    """
    获取找车机设备状态信息
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/getFindCarMachineList'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_getovernight():
    """
    过夜车数据统计接口测试
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/getOvernight'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_getsign(appcode: str, appsecret: str, cmd: str, ts: str):
    """
    获取单车场接口签名
    :param str appcode: appCode
    :param str appsecret: appSecret
    :param str cmd: cmd
    :param str ts: ts
    """
    url = 'http://192.168.21.249:8083' + '/tool/getSign'
    params = {
        'appcode': appcode,
        'appsecret': appsecret,
        'cmd': cmd,
        'ts': ts,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_getts():
    """
    获取当前时间戳
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/getTS'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_pushallversioninfo():
    """
    寻车各个服务版本信息上传redis
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/pushAllVersionInfo'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_pushlotinfo():
    """
    上传车场基本信息
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/pushLotInfo'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_rebootdevice(ip: str):
    """
    找车机设备（找车机程序会下发指令给主板）重启指令下发
    :param str ip: ip
    """
    url = 'http://192.168.21.249:8083' + '/tool/rebootDevice'
    params = {
        'ip': ip,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_rebootmachine(ip: str):
    """
    找车机程序重启指令下发
    :param str ip: ip
    """
    url = 'http://192.168.21.249:8083' + '/tool/rebootMachine'
    params = {
        'ip': ip,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_refreshserverlog():
    """
    刷新运行日志
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/refreshServerLog'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_syncstereoscopicareahistory():
    """
    同步立体车位区域关联车位历史数据
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/syncStereoscopicAreaHistory'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_tableorganization():
    """
    表整理以及归档
    
    """
    url = 'http://192.168.21.249:8083' + '/tool/tableOrganization'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def tool_uploadmachineinfo(ip: str):
    """
    uploadMachineInfo
    :param str ip: ip
    """
    url = 'http://192.168.21.249:8083' + '/tool/uploadMachineInfo'
    params = {
        'ip': ip,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def upload_awsenableswitch(awsenableswitch: int):
    """
    是否上传车场问题图片到ai中心 0:开启  1:关闭
    :param int awsenableswitch: 是否上传车场问题图片到ai中心 0:开启  1:关闭
    """
    url = 'http://192.168.21.249:8083' + '/upload/awsEnableSwitch'
    params = {
        'awsenableswitch': awsenableswitch,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def upload_channelswaggerswitch(channelswaggerswitch: int):
    """
    channel_service服务swagger配置开关 0:开启  1:关闭
    :param int channelswaggerswitch: 是否上传车场问题图片到ai中心 0:开启  1:关闭
    """
    url = 'http://192.168.21.249:8083' + '/upload/channelSwaggerSwitch'
    params = {
        'channelswaggerswitch': channelswaggerswitch,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def upload_chunkupload(chunk: int, chunktotal: int, file: str, size: int, taskid: str):
    """
    广告-视频上传
    :param int chunk: 当前为第几分片（从第0片开始）
    :param int chunktotal: 分片总数
    :param str file: file文件
    :param int size: 每个分片的大小
    :param str taskid: 文件传输任务ID（同一次上传id相同，可取UUID）
    """
    url = 'http://192.168.21.249:8083' + '/upload/chunkUpload'
    params = {
        'chunk': chunk,
        'chunktotal': chunktotal,
        'file': file,
        'size': size,
        'taskid': taskid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def upload_downloadstylec():
    """
    下载识别文件
    
    """
    url = 'http://192.168.21.249:8083' + '/upload/downloadStyleC'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def upload_getconfig():
    """
    获取系统参数配置信息
    
    """
    url = 'http://192.168.21.249:8083' + '/upload/getConfig'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def upload_guidanceswaggerswitch(guidanceswaggerswitch: int):
    """
    parking_guidance服务swagger配置开关 0:开启  1:关闭
    :param int guidanceswaggerswitch: 是否上传车场问题图片到ai中心 0:开启  1:关闭
    """
    url = 'http://192.168.21.249:8083' + '/upload/guidanceSwaggerSwitch'
    params = {
        'guidanceswaggerswitch': guidanceswaggerswitch,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def upload_replacelib(multipartfile: str):
    """
    替换识别库
    :param str multipartfile: multipartFile
    """
    url = 'http://192.168.21.249:8083' + '/upload/replaceLib'
    params = {
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def upload_uploadad(file: str):
    """
    广告-图片上传
    :param str file: 文件
    """
    url = 'http://192.168.21.249:8083' + '/upload/uploadAd'
    params = {
        'file': file,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def upload_uploadfloorcapture(floorcapture: str, floorid: int):
    """
    上传楼层底图截图照片
    :param str floorcapture: 楼层截图照片
    :param int floorid: 楼层ID
    """
    url = 'http://192.168.21.249:8083' + '/upload/uploadFloorCapture'
    params = {
        'floorcapture': floorcapture,
        'floorid': floorid,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def upload_uploadicon(iconimage: str):
    """
    上传图标
    :param str iconimage: 文件
    """
    url = 'http://192.168.21.249:8083' + '/upload/uploadIcon'
    params = {
        'iconimage': iconimage,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def upload_uploadimagemap(imagemap: str):
    """
    上传找车机路线指引图片
    :param str imagemap: 指引图片
    """
    url = 'http://192.168.21.249:8083' + '/upload/uploadImageMap'
    params = {
        'imagemap': imagemap,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def upload_uploadimgaws():
    """
    AWS上传车牌识别异常图片 - 手动触发接口
    
    """
    url = 'http://192.168.21.249:8083' + '/upload/uploadImgAws'
    params = {
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def upload_uploadrouteqr(file: str):
    """
    上传找车路线二维码图片
    :param str file: 文件
    """
    url = 'http://192.168.21.249:8083' + '/upload/uploadRouteQr'
    params = {
        'file': file,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def upload_uploadstylec(lotid: int, multipartfile: str):
    """
    上传识别文件
    :param int lotid: lotId
    :param str multipartfile: multipartFile
    """
    url = 'http://192.168.21.249:8083' + '/upload/uploadStyleC'
    params = {
        'lotid': lotid,
        'multipartfile': multipartfile,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def user_changepassword(id: int, newpassword: str, oldpassword: str):
    """
    修改密码
    :param int id: 主键
    :param str newpassword: 新密码
    :param str oldpassword: 旧密码
    """
    url = 'http://192.168.21.249:8083' + '/user/changePassword'
    params = {
        'id': id,
        'newpassword': newpassword,
        'oldpassword': oldpassword,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def user_deletesoftinids(ids: str):
    """
    批量逻辑删除
    :param str ids: 主键
    """
    url = 'http://192.168.21.249:8083' + '/user/deleteSoftInIds'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def user_getbyid(id: int):
    """
    根据主键获取详情
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/user/getById'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def user_insert(account: str, id: int, name: str, password: str, phone: str, remark: str, roleid: int, status: bool):
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
    """
    url = 'http://192.168.21.249:8083' + '/user/insert'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def user_resetpassword(id: int, password: str):
    """
    重置密码
    :param int id: 主键
    :param str password: 密码
    """
    url = 'http://192.168.21.249:8083' + '/user/resetPassword'
    params = {
        'id': id,
        'password': password,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def user_selectpagelist(account: str, endtime: str, name: str, pagenumber: int, pagesize: int, phone: str, remark: str, roleid: int, starttime: str, status: bool):
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
    """
    url = 'http://192.168.21.249:8083' + '/user/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def user_update(account: str, id: int, name: str, password: str, phone: str, remark: str, roleid: int, status: bool):
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
    """
    url = 'http://192.168.21.249:8083' + '/user/update'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def open_getspacebyplate(parkcode: str, platenum: str):
    """
    按车牌号查询泊位信息接口
    :param str parkcode: 停车场 ID
    :param str platenum: 车牌号
    """
    url = 'http://192.168.21.249:8083' + '/v2/open/getSpaceByPlate'
    params = {
        'parkcode': parkcode,
        'platenum': platenum,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def open_getspaceinfo(parkcode: str, spacenum: str):
    """
    按泊位号查询泊位信息接口
    :param str parkcode: 停车场 ID
    :param str spacenum: 车位编号
    """
    url = 'http://192.168.21.249:8083' + '/v2/open/getSpaceInfo'
    params = {
        'parkcode': parkcode,
        'spacenum': spacenum,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def open_parkingspaceinfo(parkcode: str):
    """
    车位信息列表接口
    :param str parkcode: 停车场 ID
    """
    url = 'http://192.168.21.249:8083' + '/v2/open/parkingSpaceInfo'
    params = {
        'parkcode': parkcode,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def warnillegalpark_deleteinids(ids: str):
    """
    批量删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/warnIllegalPark/deleteInIds'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def warnillegalpark_insert(bindtype: int, parkareaidlist: list, plateno: str, warntimelist: list):
    """
    添加
    :param int bindtype: 绑定类型  1：绑定车位  2：绑定区域
    :param list parkareaidlist: 车位或区域id
    :param str plateno: 车牌号
    :param list warntimelist: 告警时间
    """
    url = 'http://192.168.21.249:8083' + '/warnIllegalPark/insert'
    params = {
        'bindtype': bindtype,
        'parkareaidlist': parkareaidlist,
        'plateno': plateno,
        'warntimelist': warntimelist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def warnillegalpark_selectpagelist(endtime: str, id: int, pagenumber: int, pagesize: int, parkareaname: str, plateno: str, starttime: str):
    """
    分页查询
    :param str endtime: 结束时间
    :param int id: 主键
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkareaname: 车位或区域的名称
    :param str plateno: 车牌号
    :param str starttime: 开始时间
    """
    url = 'http://192.168.21.249:8083' + '/warnIllegalPark/selectPageList'
    params = {
        'endtime': endtime,
        'id': id,
        'pagenumber': pagenumber,
        'pagesize': pagesize,
        'parkareaname': parkareaname,
        'plateno': plateno,
        'starttime': starttime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def warnillegalpark_update(bindtype: int, id: int, parkareaidlist: list, plateno: str, warntimelist: list):
    """
    更新
    :param int bindtype: 绑定类型  1：绑定车位  2：绑定区域
    :param int id: 主键
    :param list parkareaidlist: 车位或区域id
    :param str plateno: 车牌号
    :param list warntimelist: 告警时间
    """
    url = 'http://192.168.21.249:8083' + '/warnIllegalPark/update'
    params = {
        'bindtype': bindtype,
        'id': id,
        'parkareaidlist': parkareaidlist,
        'plateno': plateno,
        'warntimelist': warntimelist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def warnlog_selectpagelist(endtime: str, id: int, pagenumber: int, pagesize: int, parkno: str, parkplateno: str, starttime: str, warnstatus: int, warntype: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/warnLog/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def warnlog_stopwarn(id: int):
    """
    停止告警
    :param int id: 主键
    """
    url = 'http://192.168.21.249:8083' + '/warnLog/stopWarn'
    params = {
        'id': id,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def warnspaceoccupy_deletebyelementparkid(elementparkid: int):
    """
    删除指定车位id的记录
    :param int elementparkid: elementParkId
    """
    url = 'http://192.168.21.249:8083' + '/warnSpaceOccupy/deleteByElementParkId'
    params = {
        'elementparkid': elementparkid,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def warnspaceoccupy_deleteinids(ids: str):
    """
    批量删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/warnSpaceOccupy/deleteInIds'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def warnspaceoccupy_insert(parkid: int, plateno: str, warntimelist: list):
    """
    添加
    :param int parkid: 车位id
    :param str plateno: 车牌号
    :param list warntimelist: 告警时间
    """
    url = 'http://192.168.21.249:8083' + '/warnSpaceOccupy/insert'
    params = {
        'parkid': parkid,
        'plateno': plateno,
        'warntimelist': warntimelist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def warnspaceoccupy_selectpagelist(endtime: str, id: int, pagenumber: int, pagesize: int, parkno: str, plateno: str, starttime: str):
    """
    分页查询
    :param str endtime: 结束时间
    :param int id: 主键
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位号
    :param str plateno: 绑定车牌号，多个车牌号中间用英文分号隔开
    :param str starttime: 开始时间
    """
    url = 'http://192.168.21.249:8083' + '/warnSpaceOccupy/selectPageList'
    params = {
        'endtime': endtime,
        'id': id,
        'pagenumber': pagenumber,
        'pagesize': pagesize,
        'parkno': parkno,
        'plateno': plateno,
        'starttime': starttime,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def warnspaceoccupy_update(id: int, parkid: int, plateno: str, warntimelist: list):
    """
    更新
    :param int id: 主键
    :param int parkid: 车位id
    :param str plateno: 绑定车牌号，多个车牌号中间用英文分号隔开
    :param list warntimelist: 告警时间
    """
    url = 'http://192.168.21.249:8083' + '/warnSpaceOccupy/update'
    params = {
        'id': id,
        'parkid': parkid,
        'plateno': plateno,
        'warntimelist': warntimelist,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def warnspecialcar_deleteinids(ids: str):
    """
    批量删除
    :param str ids: ids
    """
    url = 'http://192.168.21.249:8083' + '/warnSpecialCar/deleteInIds'
    params = {
        'ids': ids,
    }
    response = requests.request('GET', url, json=params)
    return response.json()


def warnspecialcar_insert(lightwarnwitch: bool, plateno: str, remark: str, warntimelist: list, warntype: int):
    """
    添加
    :param bool lightwarnwitch: 车位灯告警开关   1：开  0：关
    :param str plateno: 车牌号
    :param str remark: 备注
    :param list warntimelist: 告警时间
    :param int warntype: 告警类型  1：入车告警  2：出车告警  3：入车和出车都告警
    """
    url = 'http://192.168.21.249:8083' + '/warnSpecialCar/insert'
    params = {
        'lightwarnwitch': lightwarnwitch,
        'plateno': plateno,
        'remark': remark,
        'warntimelist': warntimelist,
        'warntype': warntype,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


def warnspecialcar_selectpagelist(endtime: str, id: int, lightwarnwitch: bool, pagenumber: int, pagesize: int, plateno: str, remark: str, starttime: str, warntype: int):
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
    """
    url = 'http://192.168.21.249:8083' + '/warnSpecialCar/selectPageList'
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
    response = requests.request('POST', url, json=params)
    return response.json()


def warnspecialcar_update(id: int, lightwarnwitch: bool, plateno: str, remark: str, warntimelist: list, warntype: int):
    """
    更新
    :param int id: 主键
    :param bool lightwarnwitch: 车位灯告警开关   1：开  0：关
    :param str plateno: 车牌号
    :param str remark: 备注
    :param list warntimelist: 告警时间
    :param int warntype: 告警类型  1：入车告警  2：出车告警  3：入车和出车都告警
    """
    url = 'http://192.168.21.249:8083' + '/warnSpecialCar/update'
    params = {
        'id': id,
        'lightwarnwitch': lightwarnwitch,
        'plateno': plateno,
        'remark': remark,
        'warntimelist': warntimelist,
        'warntype': warntype,
    }
    response = requests.request('POST', url, json=params)
    return response.json()


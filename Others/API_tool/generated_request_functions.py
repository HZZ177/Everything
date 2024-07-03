import requests


def areaDeviceUpdateStatusUsingPOST(areaDeviceUpdateStatus):
    url = 'http://192.168.21.249:7072' + '/area/areaDeviceUpdateStatus'
    params = {
        'areaDeviceUpdateStatus': areaDeviceUpdateStatus,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def enterUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/area/enter'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def leaveUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/area/leave'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def updateStereoscopicDetectorParkAddrListUsingGET():
    url = 'http://192.168.21.249:7072' + '/area/updateStereoscopicDetectorParkAddrList'
    response = requests.request('GET', url, params=params)
    return response.json()

def areaInOutUsingPOST(areaInOutReqVo):
    url = 'http://192.168.21.249:7072' + '/areaCamera/areaInOut'
    params = {
        'areaInOutReqVo': areaInOutReqVo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def areaPostPictureUsingPOST(areaUpdatePlateReqVo):
    url = 'http://192.168.21.249:7072' + '/areaCamera/areaPostPicture'
    params = {
        'areaUpdatePlateReqVo': areaUpdatePlateReqVo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def listInOutCarInfoUsingPOST(inOutCarInfoReqDTO):
    url = 'http://192.168.21.249:7072' + '/carInOut/listInOutCarInfo'
    params = {
        'inOutCarInfoReqDTO': inOutCarInfoReqDTO,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def postCarOutInfoUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/charge/postCarOutInfo'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def getInfoUsingPOST(deviceEscalationReqVO):
    url = 'http://192.168.21.249:7072' + '/deviceEscalation/getInfo'
    params = {
        'deviceEscalationReqVO': deviceEscalationReqVO,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def saveInfoUsingPOST(deviceEscalationReqVO):
    url = 'http://192.168.21.249:7072' + '/deviceEscalation/saveInfo'
    params = {
        'deviceEscalationReqVO': deviceEscalationReqVO,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def offUsingGET():
    url = 'http://192.168.21.249:7072' + '/emergencyMode/off'
    response = requests.request('GET', url, params=params)
    return response.json()

def onUsingGET():
    url = 'http://192.168.21.249:7072' + '/emergencyMode/on'
    response = requests.request('GET', url, params=params)
    return response.json()

def healthCheckUsingGET():
    url = 'http://192.168.21.249:7072' + '/healthCheck'
    response = requests.request('GET', url, params=params)
    return response.json()

def pushConfigUsingPOST(iniChangeReqDTO):
    url = 'http://192.168.21.249:7072' + '/iniChange/pushConfig'
    params = {
        'iniChangeReqDTO': iniChangeReqDTO,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def noticeUsingPOST_1(vo):
    url = 'http://192.168.21.249:7072' + '/ledScreen/notice'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def noticeTestUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/ledScreen/noticeTest'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def updateScreenCmdUsingPOST(screenCmdReqVO):
    url = 'http://192.168.21.249:7072' + '/ledScreen/updateScreenCmd'
    params = {
        'screenCmdReqVO': screenCmdReqVO,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def initStatusBatchUsingPOST():
    url = 'http://192.168.21.249:7072' + '/nodeDevice/initStatusBatch'
    response = requests.request('POST', url, params=params)
    return response.json()

def select485AndIpCamListUsingPOST():
    url = 'http://192.168.21.249:7072' + '/nodeDevice/select485AndIpCamList'
    response = requests.request('POST', url, params=params)
    return response.json()

def selectAllListUsingPOST():
    url = 'http://192.168.21.249:7072' + '/nodeDevice/selectAllList'
    response = requests.request('POST', url, params=params)
    return response.json()

def selectInterNodeAndIpCamListUsingPOST():
    url = 'http://192.168.21.249:7072' + '/nodeDevice/selectInterAndIpCamList'
    response = requests.request('POST', url, params=params)
    return response.json()

def updateStatusBatchByAddrUsingPOST(param):
    url = 'http://192.168.21.249:7072' + '/nodeDevice/updateStatusBatchByAddr'
    params = {
        'param': param,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def clearCaptureUrlUsingGET(parkAddr):
    url = 'http://192.168.21.249:7072' + '/park/clearCaptureUrl'
    params = {
        'parkAddr': parkAddr,
    }
    response = requests.request('GET', url, params=params)
    return response.json()

def enterUsingPOST_1(vo):
    url = 'http://192.168.21.249:7072' + '/park/enter'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def faultForFindCarUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/park/faultForFindCar'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def faultForGuidanceUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/park/faultForGuidance'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def freeForFindCarUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/park/freeForFindCar'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def freeForGuidanceUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/park/freeForGuidance'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def getCaptureUrlUsingGET(parkAddr):
    url = 'http://192.168.21.249:7072' + '/park/getCaptureUrl'
    params = {
        'parkAddr': parkAddr,
    }
    response = requests.request('GET', url, params=params)
    return response.json()

def getEmptyCountUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/park/getEmptyCount'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def leaveUsingPOST_1(vo):
    url = 'http://192.168.21.249:7072' + '/park/leave'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def occupyForFindCarUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/park/occupyForFindCar'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def occupyForGuidanceUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/park/occupyForGuidance'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def pushParkCameraUsingGET(parkingIp, parkingPort):
    url = 'http://192.168.21.249:7072' + '/park/pushParkCamera'
    params = {
        'parkingIp': parkingIp,
        'parkingPort': parkingPort,
    }
    response = requests.request('GET', url, params=params)
    return response.json()

def selectParkListByConditionUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/park/selectParkListByCondition'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def snapAllByLotUsingGET():
    url = 'http://192.168.21.249:7072' + '/park/snapAllByLot'
    response = requests.request('GET', url, params=params)
    return response.json()

def testUsingPOST(addr):
    url = 'http://192.168.21.249:7072' + '/park/test'
    params = {
        'addr': addr,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def test2UsingPOST():
    url = 'http://192.168.21.249:7072' + '/park/test2'
    response = requests.request('POST', url, params=params)
    return response.json()

def updateAllFaultUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/park/updateAllFault'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def updateCaptureUrlUsingPOST(updateCaptureUrlVO):
    url = 'http://192.168.21.249:7072' + '/park/updateCaptureUrl'
    params = {
        'updateCaptureUrlVO': updateCaptureUrlVO,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def updatePlateNoUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/park/updatePlateNo'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def noticeUsingPOST(parkingLightNoticeReqVO):
    url = 'http://192.168.21.249:7072' + '/parking-light/notice'
    params = {
        'parkingLightNoticeReqVO': parkingLightNoticeReqVO,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def noticeForStopWarnUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/parking-light/noticeForStopWarn'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def postCarOutInfoUsingPOST_1(vo):
    url = 'http://192.168.21.249:7072' + '/parkmall/carEnd'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def getAllTcpAddrUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/screen/getAllTcpAddr'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def getLcdScreenDataUsingGET(ip, type):
    url = 'http://192.168.21.249:7072' + '/screen/getLcdScreenData'
    params = {
        'ip': ip,
        'type': type,
    }
    response = requests.request('GET', url, params=params)
    return response.json()

def initAllOffLineUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/screen/initAllOffLine'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def ledPageRefreshUsingPOST(dto):
    url = 'http://192.168.21.249:7072' + '/screen/ledPageRefresh'
    params = {
        'dto': dto,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def sendLcdScreenDataUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/screen/sendLcdScreenData'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def sendLcdScreenDefaultDataUsingGET(ip, type):
    url = 'http://192.168.21.249:7072' + '/screen/sendLcdScreenDefaultData'
    params = {
        'ip': ip,
        'type': type,
    }
    response = requests.request('GET', url, params=params)
    return response.json()

def updateStatusByAddrUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/screen/updateStatusByAddr'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def listLcdScreenUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/screenRelated/listLcdScreen'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def resetAllUsingGET():
    url = 'http://192.168.21.249:7072' + '/taskManage/resetAll'
    response = requests.request('GET', url, params=params)
    return response.json()

def controlHighTaskUsingGET(flag):
    url = 'http://192.168.21.249:7072' + '/tool/controlHighTask'
    params = {
        'flag': flag,
    }
    response = requests.request('GET', url, params=params)
    return response.json()

def dealWithGrpcCmdUsingPOST(customJsonCmdRespDTO):
    url = 'http://192.168.21.249:7072' + '/tool/dealWithGrpcCmd'
    params = {
        'customJsonCmdRespDTO': customJsonCmdRespDTO,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def sendCommandToAllScreenUsingGET():
    url = 'http://192.168.21.249:7072' + '/tool/sendCommandToAllScreen'
    response = requests.request('GET', url, params=params)
    return response.json()

def sendLightCommandToFindCarUsingPOST(baseReqDTO):
    url = 'http://192.168.21.249:7072' + '/tool/sendLightCommandToFindCar'
    params = {
        'baseReqDTO': baseReqDTO,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def sendLightCommandToGuidanceUsingPOST(baseReqDTO):
    url = 'http://192.168.21.249:7072' + '/tool/sendLightCommandToGuidance'
    params = {
        'baseReqDTO': baseReqDTO,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def snapUsingGET():
    url = 'http://192.168.21.249:7072' + '/tool/snap'
    response = requests.request('GET', url, params=params)
    return response.json()

def uniteApiProUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/tool/uniteApiPro'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def uniteApiTestUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/tool/uniteApiTest'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def uploadImgUsingGET(url):
    url = 'http://192.168.21.249:7072' + '/tool/uploadImg'
    params = {
        'url': url,
    }
    response = requests.request('GET', url, params=params)
    return response.json()

def getCarLocInfoUsingPOST(carLocInfoReqDTO):
    url = 'http://192.168.21.249:7072' + '/unified/getCarLocInfo'
    params = {
        'carLocInfoReqDTO': carLocInfoReqDTO,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def getParkListByPlateNoUsingPOST(getParkListByPlateNoReqDTO):
    url = 'http://192.168.21.249:7072' + '/unified/getParkListByPlateNo'
    params = {
        'getParkListByPlateNoReqDTO': getParkListByPlateNoReqDTO,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def generateCrossLineUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/warnLog/generateCrossLine'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()

def stopCrossLineUsingPOST(vo):
    url = 'http://192.168.21.249:7072' + '/warnLog/stopCrossLine'
    params = {
        'vo': vo,
    }
    response = requests.request('POST', url, params=params)
    return response.json()


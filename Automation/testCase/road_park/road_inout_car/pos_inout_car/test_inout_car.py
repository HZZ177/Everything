from time import strftime

import allure

from common.configLog import logger
from common.filepath import config
from common.generate_data import generate_data
from service.road_park.api.appService import AppService
from service.hardware_platform.LowVideoService import LowVideoService
from service.hardware_platform.cameraService import CameraServer
from service.hardware_platform.iotService import IOTService
from service.road_park.manage.formCenter.carDetailService import CarDetailService
from service.road_park.manage.formCenter.feeDetailService import FeeDetailService


@allure.epic('POS机入出车相关测试用例')
@allure.story('POS机入出车')
class TestInOutCar:
    """
    POS机入出车相关测试用例
    """

    @allure.title('POS机入车，免费停车时长内直接离场，查费')
    def test_incar_no_fee_out(self, setupAndTeardown):
        logger.info("=================================【【正在执行用例】】=================================")
        logger.info("POS机入车，免费停车时长内直接离场，查费")
        test_data = setupAndTeardown
        parking_info = test_data["parking_info"]
        inout_car_info = test_data["inout_car_info"]
        berth, carNo = parking_info['parkSpaceCode1'], generate_data.car_no()
        with allure.step(f'POS机入车：{carNo}'):
            records = AppService().public_in_car(carNo=carNo, parkspaceCode=berth, **inout_car_info, **parking_info)
            detail = AppService().get_present_detail(records['parkingRecordId'], **parking_info)
            assert detail['carNo'] == carNo, f'判断车位入车的车牌错误，理论值：{carNo}'
            assert detail['status'] == 1, '判断车位是否有车，理论值：有车'
        with allure.step('免费时间内，点击直接离场，查看出车消息'):
            AppService().public_out_car(carNo=carNo, parkspaceCode=berth, outTime=generate_data.adjust_time(seconds=60), **parking_info)
            fee_detail = CarDetailService().parking_session_page(carNo=carNo, **parking_info)['data']['records'][0]
            assert fee_detail['status'] == 3, '判断欠费状态错误，理论值：无需缴费'
            assert fee_detail['totalMoney'] == 0, '判断应收金额错误，理论值：0元'
            assert fee_detail['carNo'] == carNo, f'判断停车计费明细的车牌错误，理论值：{carNo}'

    @allure.title('POS机入车，产生费用后结算离场，再次入车，POS机二维码缴欠费，查看欠费状态和应收金额等')
    def test_incar_fee_out_settle_owe(self, setupAndTeardown):
        logger.info("=================================【【正在执行用例】】=================================")
        logger.info("POS机入车，产生费用后结算离场，再次入车，POS机二维码缴欠费，查看欠费状态和应收金额等")
        test_data = setupAndTeardown
        parking_info = test_data["parking_info"]
        toll_man_id = parking_info["tollmanId"]
        inout_car_info = test_data["inout_car_info"]
        no_Free_stopTime = test_data["no_Free_stopTime"]
        free_stopTime = test_data["free_stopTime"]
        now, berth = strftime('%Y-%m-%d %H:%M:%S'), parking_info['parkSpaceCode1']
        car_no, inTime = generate_data.car_no(), generate_data.adjust_time(now, -no_Free_stopTime * 2)
        with allure.step(f'POS机入车：{car_no}'):
            # 入车
            in_car = AppService().public_in_car(carNo=car_no, parkspaceCode=berth, inTime=inTime, **parking_info)
        with allure.step('产生停车费用后，点击结算离场'):
            out_time, parking_record_id = generate_data.adjust_time(now, -no_Free_stopTime), in_car.get(
                'parkingRecordId')
            AppService().public_fee_out_settle(car_no, parking_record_id, out_time, tollmanId=toll_man_id)
        with allure.step('查看停车计费明细表的应收金额和欠费状态'):
            details = CarDetailService().parking_session_page(car_no, **parking_info)['data']['records'][0]
            assert details['totalMoney'] > 0, f'判断本次应收金额大于零，理论值：大于零，实际：{details}'
            assert details['status'] == 0, '判断是否缴清状态错误，理论值：未缴清'
        with allure.step(f'POS机再次入车：{car_no}，结算离场时，POS机二维码支付欠费'):
            again_in_time = generate_data.adjust_time(out_time, 10)
            again_out_time = generate_data.adjust_time(again_in_time, free_stopTime)
            again_incar = AppService().public_in_car(carNo=car_no, parkspaceCode=berth, inTime=again_in_time, carType=in_car['carType'], **parking_info)
            again_parkingRecordId = again_incar['parkingRecordId']
            again_settle_out = AppService().public_fee_out_settle(car_no, again_parkingRecordId, again_out_time, tollmanId=toll_man_id)

            # lacks = again_settle_out['lacks'][0]
            # free_money, total_money = lacks['freeMoney'], lacks.get('totalMoney')
            # POS机二维码支付欠费：补缴欠款
            # details = [{
            #     'freeMoney': free_money,
            #     'orderType': 1,
            #     'originRecordId': parking_record_id,
            #     'payMoney': total_money,
            #     'totalMoney': total_money
            # }]
        AppService().public_pos_qrcode_pay(carNo=car_no, **parking_info)
        with allure.step('查看支付明细表的应收、实收、支付方式、支付来源、支付渠道'):
            pay_detail = FeeDetailService().pay_order_page(car_no, **parking_info)['data']['records'][0]
            assert pay_detail['totalMoney'] == pay_detail['payMoney'], '判断应收和实收是否相等，理论值应收等于实收'
            assert pay_detail['payType'] == 1, '判断支付方式是否正确，理论值：微信'
            assert pay_detail['paySource'] == 2, '判断支付来源是否正确，理论值：速停车'
            assert pay_detail['payChannel'] == 1, '判断支付渠道是否正确，理论值：POS机'
        with allure.step('查看停车计费明细表的应收金额和欠费状态'):
            details = CarDetailService().parking_session_page(car_no)['data']['records']
            assert details[0]['status'] == 3, '判断是否缴清状态错误，理论值：无需缴费'
            if details[1]['inTime'] == inTime:
                assert details[1]['totalMoney'] == pay_detail['totalMoney'], '判断应收错误'
            assert details[1]['status'] == 1, '判断是否缴清状态错误，理论值：已缴清'


    @allure.title('在场车有1笔历史欠费，POS机停车缴费，二维码缴本次和历史欠费')
    def test_incar_fee_owe_wechat_pay(self, setupAndTeardown):
        logger.info("=================================【【正在执行用例】】=================================")
        logger.info("在场车有1笔历史欠费，POS机停车缴费，二维码缴本次和历史欠费")
        test_data = setupAndTeardown
        parking_info = test_data["parking_info"]
        toll_man_id = parking_info["tollmanId"]
        no_Free_stopTime = test_data["no_Free_stopTime"]
        now = strftime('%Y-%m-%d %H:%M:%S')
        car_no, berth = generate_data.car_no(1), parking_info['parkSpaceCode2']
        yesterday_in_time = generate_data.adjust_time(now, minutes=-25 * 60)
        with allure.step(f'POS机入车：{car_no}，产生历史欠费'):
            # 入车
            in_car = AppService().public_in_car(carNo=car_no, parkspaceCode=berth, inTime=yesterday_in_time, **parking_info)
            # 结算离场
            outTime = generate_data.adjust_time(yesterday_in_time, no_Free_stopTime)
            AppService().public_fee_out_settle(car_no, in_car['parkingRecordId'], outTime, tollmanId=toll_man_id)
        with allure.step(f'POS机入车：{car_no}'):
            # 再次入车
            today_in_time = generate_data.adjust_time(now, -no_Free_stopTime)
            again_in_car = AppService().public_in_car(carNo=car_no, parkspaceCode=berth, inTime=today_in_time, carType=in_car['carType'], **parking_info)
        with allure.step('POS机停车缴费，二维码缴本次和历史的欠费'):
            # 支付：本次加历史欠款
            AppService().public_pos_qrcode_pay_escape_now(carNo=car_no, parkingRecordId=again_in_car['parkingRecordId'], **parking_info)
        with allure.step('查看支付明细表的应收、实收、支付方式、支付来源、支付渠道'):
            order_detail = FeeDetailService().pay_order_page(carNo=car_no)['data']['records'][0]
            assert order_detail['totalMoney'] > 0, '判断应收等于实收错误，理论值：应收等于实收'
            assert order_detail['payType'] == 1, '判断支付方式错误，理论值：微信'
            assert order_detail['payChannel'] == 1, '判断支付来源错误，理论值：POS机'
            assert order_detail['paySource'] == 2, '判断支付渠道错误，理论值：速停车'
        with allure.step('直接离场'):
            AppService().public_out_car(carNo=car_no, parkspaceCode=berth, **parking_info)
        with allure.step('查看停车计费明细表的应收金额和欠费状态'):
            query_time = [yesterday_in_time.split()[0], now.split()[0]]
            details = CarDetailService().parking_session_page(carNo=car_no, outTime=query_time)['data']['records']
            for i in details:
                assert i['totalMoney'] > 0, '判断应收金额错误，理论值：大于0'
                assert i['status'] == 1, '判断是否缴清状态错误，理论值：已缴清'

    @allure.title('入车预支付本次停车费用和历史欠费金额，结算离场后，查询车辆欠费状态')  # 维护可运行
    def test_incar_prepay_this_and_owe(self, setupAndTeardown):
        """
        1、POS机入车
        2、现金预支付金额1元，查看支付明细表的支付来源、支付渠道、支付方式
        3、结算离场时，本次停车费0.5元，核对POS机支付消息
        4、查看支付明细表的缴费明细
        5、查看车辆A的历史欠费记录是否缴清（停车计费明细表）
        """
        logger.info("=================================【【正在执行用例】】=================================")
        logger.info("在场车有1笔历史欠费，POS机停车缴费，二维码缴本次和历史欠费")
        test_data = setupAndTeardown
        parking_info = test_data["parking_info"]
        toll_man_id = parking_info["tollmanId"]
        inout_car_info = test_data["inout_car_info"]
        no_Free_stopTime = test_data["no_Free_stopTime"]
        now, berth = strftime('%Y-%m-%d %H:%M:%S'), parking_info['parkSpaceCode1']
        car_no = generate_data.car_no()
        yesterday_in_time = generate_data.adjust_time(now, minutes=-25 * 60)
        with allure.step(f'POS机入车：{car_no}产生欠费'):
            # 入车
            in_car = AppService().public_in_car(carNo=car_no, parkspaceCode=berth, inTime=yesterday_in_time, **inout_car_info, **parking_info)
            # 直接离场
            yesterday_out_time = generate_data.adjust_time(yesterday_in_time, no_Free_stopTime)
            AppService().public_out_car(carNo=car_no, parkspaceCode=berth, outTime=yesterday_out_time, **parking_info)
        with allure.step('POS机再次入车'):
            today_in_time = generate_data.adjust_time(now, -no_Free_stopTime)
            car_in = AppService().public_in_car(carNo=car_no, parkspaceCode=berth, inTime=today_in_time, carType=in_car['carType'], **parking_info)
            record_id = car_in['parkingRecordId']
        with allure.step('预支付'):
            # bill = app_service.get_bill(car_no, car_in['parkingRecordId'])['data'][0]
            # details = [{
            #     'freeMoney': 0,
            #     'orderType': 2,
            #     'payMoney': 100 - bill['totalMoney'],
            #     'totalMoney': 100 - bill['totalMoney'],
            #     'originRecordId': second_parkingRecordId
            # }, {
            #     'freeMoney': 0,
            #     'orderType': 1,
            #     'payMoney': bill['totalMoney'],
            #     'totalMoney': bill['totalMoney'],
            #     'originRecordId': bill['parkingRecordId']
            # }]
            # public_pos_qrcode_pay(details, car_no)
            AppService().public_pos_prepayment(car_no, parkingRecordId=record_id, **parking_info)
        with allure.step('结算离场'):
            # today_out_time = generate_data.adjust_time(today_in_time, free_stopTime)
            AppService().public_fee_out_settle(car_no, record_id, now, tollmanId=toll_man_id)
        # TODO 部分断言没有添加

    @allure.title('地磁入车-POS机出车')
    def test_nbiot_in_pos_out(self, setupAndTeardown, add_parkSpace_bindIot):
        logger.info("=================================【【正在执行用例】】=================================")
        logger.info("地磁入车-POS机出车")
        hardware_platform_info = config.get("hardware_platform")
        test_data = setupAndTeardown
        parking_info = test_data["parking_info"]
        now = strftime('%Y-%m-%d %H:%M:%S')
        iot_imei, nbiot_berth = hardware_platform_info.get("iot_imei"), add_parkSpace_bindIot
        outTime = generate_data.adjust_time(now, minutes=2)
        with allure.step('地磁入车'):
            IOTService().nbiot_inCar_success(now, iot_imei, nbiot_berth, parking_info=parking_info)
        with allure.step(f'POS机查看该车位：{nbiot_berth} 状态'):
            msg = AppService().message(parking_info['workstationId'])['data']['records'][0]
            assert msg['source'] == 1, '判断入车方式错误，理论值：地磁'
            assert msg['carNo'] == '未登记', '判断车牌错误，理论值：未登记'
        with allure.step('POS机直接离场'):
            AppService().public_out_car(carNo='未登记', parkspaceCode=nbiot_berth, outTime=outTime, **parking_info)
        with allure.step(f'2min后POS机出车，POS机查看该车位：{nbiot_berth} 状态'):
            page = AppService().get_presents(**parking_info)['data']['roadPresentCars'][0]['presentCars']
            assert page[1]['status'] is None, '判断车位是否有车，理论值：无车'

    @allure.title('高位相机入车-高位相机出车')
    def test_camera_inout(self, setupAndTeardown, add_parkSpace_bindCamera):
        logger.info("=================================【【正在执行用例】】=================================")
        logger.info("高位相机入车-高位相机出车")
        hardware_platform_info = config.get("hardware_platform")
        test_data = setupAndTeardown
        parking_info = test_data["parking_info"]
        camera_berth, device_no = add_parkSpace_bindCamera, hardware_platform_info['cameraId']
        now, car_no = strftime('%Y-%m-%d %H:%M:%S'), generate_data.car_no()
        inTime = generate_data.adjust_time(now, minutes=-2)
        with allure.step(f'高位相机入车：{car_no}，POS机查看该车位：{camera_berth}状态'):
            CameraServer().camera_inCar_success(car_no, device_no, inTime, camera_berth, parking_info=parking_info)
            page = AppService().get_presents(**parking_info)['data']['roadPresentCars'][0]['presentCars'][1]
            assert page['carNo'] == car_no, f'判断是车牌号是否正确，理论值：{car_no}'
            assert page['status'] == 1, '判断车位有车错误，理论值：车位有车'
        with allure.step('查看消息通知的入车方式'):
            msg = AppService().message(parking_info['workstationId'])['data']['records'][0]
            assert msg['source'] == 2, '判断消息的入车方式错误，理论值：高位相机'
            assert msg['messageType'] == 1, '判断消息类型错误，理论值：入车消息'
        with allure.step('2min后高位相机出车'):
            CameraServer().camera_outCar_success(car_no, device_no, now, camera_berth, parking_info=parking_info)
            page = AppService().get_presents(**parking_info)['data']['roadPresentCars'][0]['presentCars'][1]
            assert page['status'] is None, '判断车位有车错误，理论值：车位有车'
        with allure.step('查看消息通知的出车方式'):
            msg = AppService().message(parking_info['workstationId'])['data']['records'][0]
            assert msg['source'] == 2, '判断消息的入车方式错误，理论值：高位相机'
            assert msg['messageType'] == 3, '判断消息类型错误，理论值：入车消息'

    @allure.title('低位视频桩入车-低位视频桩出车')
    def test_low_video_inout(self, setupAndTeardown, add_parkSpace_bindLowVideo):
        logger.info("=================================【【正在执行用例】】=================================")
        logger.info("低位视频桩入车-低位视频桩出车")
        car_no, now = generate_data.car_no(), strftime('%Y-%m-%d %H:%M:%S')
        hardware_platform_info = config.get("hardware_platform")
        test_data = setupAndTeardown
        parking_info = test_data["parking_info"]
        low_video_berth, deviceId = add_parkSpace_bindLowVideo, hardware_platform_info['low_video_deviceId']
        inTime = generate_data.adjust_time(now, minutes=-2)
        with allure.step(f'视频桩入车：{car_no}，POS机查看该车位：{low_video_berth}状态'):
            LowVideoService().low_video_inCar_success(car_no, deviceId, inTime, low_video_berth, parking_info=parking_info)
            page = AppService().get_presents(**parking_info)['data']['roadPresentCars'][0]['presentCars'][1]
            assert page['status'] == 1, '判断车位是否有车错误，理论值：有在场车'
        with allure.step('查看消息通知的入车方式'):
            msg = AppService().message(parking_info['workstationId'])['data']['records'][0]
            assert msg['source'] == 4, '判断消息的入车方式错误，理论值：低位视频桩'
            assert msg['messageType'] == 1, '判断消息类型错误，理论值：入车'
        with allure.step(f'视频桩出车：{car_no}，POS机查看该车位：{low_video_berth}状态'):
            LowVideoService().low_video_outCar_success(car_no, deviceId, now, low_video_berth, parking_info=parking_info)
            page = AppService().get_presents(**parking_info)['data']['roadPresentCars'][0]['presentCars'][1]
            assert page['status'] is None, '判断车位是否有车错误，理论值：车位无车'
        with allure.step('查看消息通知的出车方式'):
            msg = AppService().message(parking_info['workstationId'])['data']['records'][0]
            assert msg['source'] == 4, '判断消息的出车方式错误，理论值：低位视频桩'
            assert msg['messageType'] == 3, '判断消息类型，理论值：出车'
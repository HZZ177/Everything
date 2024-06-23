import calendar
import math
import random
import uuid
from datetime import datetime, timedelta, date
from time import strftime, localtime, strptime, mktime


class GenerateData:

    @staticmethod
    def g_uuid():
        """
        生成uuid
        """
        return str(uuid.uuid4())

    def time_to_unixTime_ms(self, timestr=''):
        """
        时间转时间戳（毫秒级）
        """
        if timestr:
            datetime_obj = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
            return int(mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
        else:
            return self.time_to_unixTime() * 1000

    def time_to_unixTime(self, dt=''):
        """
        时间转时间戳（秒级）
        """
        timeArray = strptime(dt, '%Y-%m-%d %H:%M:%S') if dt else localtime()
        # 转换成时间戳
        return int(mktime(timeArray))

    def unix_time_ms_to_time(self, time_stamp: int) -> str:
        """
        毫秒时间戳转时间
        """
        time_local = localtime(time_stamp / 1000)
        return strftime("%Y-%m-%d %H:%M:%S", time_local)

    def car_no(self, default=0):
        """
        生成随机车牌（默认生成蓝牌车-小型车，绿牌车-新能源车）

        :param default: 设置车牌类型（蓝牌车、绿牌车）
        """
        city = ['京', '津', '沪', '渝', '蒙', '新', '藏', '宁', '桂', '港', '澳', '黑', '吉', '辽', '晋', '冀', '青', '鲁',
                '豫', '苏', '皖', '浙', '闽', '赣', '湘', '鄂', '粤', '琼', '甘', '陕', '黔', '滇', '川']
        first = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                 'W', 'X', 'Y', 'Z']
        after = first + ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        if not default:
            carNo = random.choice(city) + random.choice(first) + ''.join(random.choices(after, k=5))
        else:
            carNo = random.choice(city) + random.choice(first) + ''.join(random.choices(after, k=6))

        return carNo

    def random_carType(self) -> int:
        """
        生成随机车辆类型

         0 → 小型车 ; 1 → 中型车 ; 2 → 大型车 ; 3 → 新能源车 ; 4 → 特殊车辆
        """
        return random.randint(0, 4)

    @staticmethod
    def adjust_time(inTime='', seconds=0, minutes=0, month=0) -> str:
        """
        调整时间

        :param inTime: 传入的时间（格式如：'2022-06-29 15:10:58'）
        :param seconds: 秒为调整后的0点
        :param minutes: 分钟为调整后的0点
        :param month: 月份为调整后的0点
        """
        if inTime:
            just = datetime.strptime(inTime, '%Y-%m-%d %H:%M:%S')
        else:
            just = datetime.strptime(strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        if seconds != 0:
            return str(just + timedelta(seconds=seconds))
        if minutes != 0:
            return str(just + timedelta(minutes=minutes))
        if month != 0:
            # 这里的months 参数传入的是正数表示往后推，负数表示往前推
            month = just.month - 1 + month
            year = just.year + math.floor(month / 12)
            month = month % 12 + 1
            day = min(just.day, calendar.monthrange(year, month)[1])
            recent_date = date(year, month, day).strftime('%Y%m%d')
            return str(datetime.strptime(str(recent_date), '%Y%m%d'))

    @staticmethod
    def g_day_start():
        """
        生成当天时间零点，如：2022-12-12 00:00:00
        """
        day_start = strftime('%Y-%m-%d') + ' 00:00:00'
        return day_start

    @staticmethod
    def g_day_end():
        """
        生成当天时间最后时间，如：2022-12-12 23:59:59
        """
        day_end = strftime('%Y-%m-%d') + ' 23:59:59'
        return day_end

    @staticmethod
    def g_today() -> str:
        """
        生成当天日期，如：2022-12-12
        """
        return strftime('%Y-%m-%d')


generate_data = GenerateData()

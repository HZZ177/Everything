from enum import Enum
class CarStatusEnum(Enum):
    """探测器状态枚举值"""
    NORMAL_WITH_CAR = 0  # 有车正常
    FAULT_WITH_CAR = 1  # 有车故障
    NORMAL_NO_CAR = 2  # 无车正常
    FAULT_NO_CAR = 3  # 无车故障

car_status_enum = CarStatusEnum(1)

print(car_status_enum)
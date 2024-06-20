-- 构造表api_access_info
CREATE TABLE IF NOT EXISTS `api_access_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `app_code` varchar(64) DEFAULT '' COMMENT '租户编码',
  `secret` varchar(64) DEFAULT '' COMMENT '秘钥',
  `tenant_name` varchar(255) DEFAULT '' COMMENT '租户名称',
  `tenant_tel` int(11) DEFAULT NULL COMMENT '租户电话',
  `api_perm` varchar(1024) DEFAULT '' COMMENT '接口权限（逗号隔开）',
  `skip_auth` tinyint(1) DEFAULT '0' COMMENT '是否跳过鉴权 0-否，1-是',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除0未删除1已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_app_code` (`app_code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='api接入表';

-- 构造表api_push_info
CREATE TABLE IF NOT EXISTS `api_push_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `app_code` varchar(64) DEFAULT '' COMMENT '租户编码',
  `secret` varchar(64) DEFAULT '' COMMENT '秘钥',
  `tenant_name` varchar(255) DEFAULT '' COMMENT '租户名称',
  `func_module` varchar(64) DEFAULT '' COMMENT '功能模块',
  `push_url` varchar(255) DEFAULT '' COMMENT '推送路径',
  `impl_class` varchar(64) DEFAULT '' COMMENT '实现类',
  `attribute` varchar(255) DEFAULT '' COMMENT '额外备用',
  `push_switch` tinyint(1) DEFAULT '1' COMMENT '推送开关 0-关，1-开',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_func_module` (`func_module`) USING BTREE,
  KEY `index_app_code` (`app_code`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='推送信息';

-- 构造表api_supplementary_push
CREATE TABLE IF NOT EXISTS `api_supplementary_push` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `url` varchar(255) DEFAULT NULL COMMENT '补推完整路径地址',
  `header` varchar(255) DEFAULT NULL COMMENT '请求头相关信息',
  `params` varchar(255) DEFAULT NULL COMMENT '参数相关信息',
  `reason` varchar(255) DEFAULT NULL COMMENT '推送失败原因或异常信息',
  `status` tinyint(1) DEFAULT '0' COMMENT '补推状态 0：未推送 1：已推送',
  `req_id` varchar(32) DEFAULT NULL COMMENT '事件ID，用于查询对应绑定事件关系',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='补推信息表';

-- 构造表area_camera
CREATE TABLE IF NOT EXISTS `area_camera` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `camera_ip` varchar(255) DEFAULT NULL COMMENT '相机ip',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `camera_direction` int(11) DEFAULT NULL COMMENT '相机方向',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(255) DEFAULT NULL COMMENT '创建者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `updater` datetime DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='区域相机';

-- 构造表area_camera_relate
CREATE TABLE IF NOT EXISTS `area_camera_relate` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `area_camera_id` int(11) DEFAULT NULL COMMENT '区域相机id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `area_id` int(11) DEFAULT NULL COMMENT '区域id',
  `come_bind` tinyint(4) DEFAULT '1' COMMENT '来车绑定   1=入车   2=出车',
  `go_bind` tinyint(4) DEFAULT '2' COMMENT '去车绑定   1=入车   2=出车',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creater` varchar(50) DEFAULT NULL COMMENT '创建者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='区域相机关联区域表';

-- 构造表area_info
CREATE TABLE IF NOT EXISTS `area_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(255) DEFAULT NULL COMMENT '区域名称',
  `lot_id` int(11) NOT NULL COMMENT '车场id',
  `floor_id` int(11) NOT NULL COMMENT '楼层id',
  `type` int(11) DEFAULT '0' COMMENT '0:普通区域 1:立体车库区域',
  `x` varchar(255) DEFAULT NULL COMMENT '区域x坐标',
  `y` varchar(255) DEFAULT NULL COMMENT '区域y坐标',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0：未删除，1：已删除）',
  `creator` varchar(255) DEFAULT NULL COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(255) DEFAULT NULL COMMENT '更新人',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `park_space_camera_ip` varchar(64) DEFAULT NULL COMMENT '立体车位相机IP',
  `park_space_camera_unique_id` varchar(64) DEFAULT NULL COMMENT '立体车位相机唯一标识',
  `detector_park_addr_list` varchar(1024) DEFAULT NULL COMMENT '立体车位关联探测器车位唯一标识，以英文,分隔开',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='区域信息';

-- 构造表b_car_in_out_record
CREATE TABLE IF NOT EXISTS `b_car_in_out_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id lot_info id',
  `area_id` int(11) DEFAULT NULL COMMENT '区域id',
  `area_name` varchar(255) DEFAULT '' COMMENT '区域名称',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `floor_name` varchar(255) DEFAULT '' COMMENT '楼层名称',
  `element_park_id` int(11) DEFAULT NULL COMMENT '车位id',
  `park_addr` int(11) DEFAULT NULL COMMENT '车位地址',
  `park_status` int(11) DEFAULT NULL COMMENT '车位状态 0-空闲 1-占用 2-故障 3-停止服务',
  `park_control` int(11) DEFAULT NULL COMMENT '车位控制 0-自动控制 1-手动控制',
  `park_no` varchar(255) DEFAULT '' COMMENT '车位名称',
  `plate_no` varchar(64) DEFAULT '' COMMENT '车牌号',
  `plate_no_simple` varchar(64) DEFAULT NULL COMMENT '纯数字字母车牌',
  `car_image_url` varchar(255) DEFAULT NULL COMMENT '车辆照片地址',
  `plate_no_color` varchar(10) DEFAULT NULL COMMENT '车牌底色',
  `plate_no_record` varchar(1024) DEFAULT NULL COMMENT '历史车牌识别记录，多个车牌之间用英文逗号隔开',
  `in_time` datetime DEFAULT NULL COMMENT '入车时间',
  `out_time` datetime DEFAULT NULL COMMENT '出车时间',
  `in_type` tinyint(4) DEFAULT NULL COMMENT '操作类型 0-自动入车 1-手动入车',
  `out_type` tinyint(4) DEFAULT NULL COMMENT '操作类型 0-自动出车 1-手动出车',
  `unique_id` varchar(32) DEFAULT NULL COMMENT '每次进出车事件唯一UUID绑定',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_create_time` (`create_time`) USING BTREE,
  KEY `idx_out_time` (`out_time`) USING BTREE,
  KEY `index_element_park_id` (`element_park_id`) USING BTREE,
  KEY `index_park_no` (`park_no`) USING BTREE,
  KEY `index_plate_no` (`plate_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='历史进出车记录表';

-- 构造表b_car_in_out_record_area
CREATE TABLE IF NOT EXISTS `b_car_in_out_record_area` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `area_camera_id` int(11) DEFAULT NULL COMMENT '区域相机id',
  `area_camera_ip` varchar(255) DEFAULT NULL COMMENT '区域相机ip',
  `event_id` varchar(255) DEFAULT NULL COMMENT '事件id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `floor_name` varchar(100) DEFAULT NULL COMMENT '楼层名称',
  `area_id` int(11) DEFAULT NULL COMMENT '区域id',
  `area_name` varchar(100) DEFAULT NULL COMMENT '区域名称',
  `plate_no` varchar(100) DEFAULT NULL COMMENT '车牌号',
  `plate_no_simple` varchar(64) DEFAULT NULL COMMENT '纯数字字母车牌',
  `plate_no_color` varchar(10) DEFAULT NULL COMMENT '车牌底色',
  `car_image_url` varchar(255) DEFAULT NULL COMMENT '车辆抓拍照片路径',
  `type` tinyint(4) DEFAULT NULL COMMENT '事件类型  1：进车   2：出车',
  `in_out_time` datetime DEFAULT NULL COMMENT '入车时间或者出车时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(100) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(100) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_create_time` (`create_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车辆进出车记录（区域相机）';

-- 构造表b_present_car_plate_record
CREATE TABLE IF NOT EXISTS `b_present_car_plate_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `present_car_record_id` int(11) DEFAULT NULL COMMENT '在场车记录id',
  `plate_no` varchar(64) DEFAULT '' COMMENT '车牌号',
  `plate_no_simple` varchar(64) DEFAULT NULL COMMENT '纯数字字母车牌',
  `car_image_url` varchar(255) DEFAULT NULL COMMENT '车牌图片路径',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `plate_no_reliability` int(11) DEFAULT '0' COMMENT '图片识别车牌可信度',
  `recognition_number` int(11) DEFAULT '1' COMMENT '图片识别车牌次数',
  `charge_status` tinyint(1) DEFAULT '0' COMMENT '收费系统比对状态，0：未比对  1：已比对',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='在场车车牌记录表';

-- 构造表b_present_car_record
CREATE TABLE IF NOT EXISTS `b_present_car_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id lot_info id',
  `area_id` int(11) DEFAULT NULL COMMENT '区域id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `element_park_id` int(11) DEFAULT NULL COMMENT '车位id',
  `plate_no` varchar(64) DEFAULT '' COMMENT '车牌号，格式：川A8F43P',
  `plate_no_simple` varchar(64) DEFAULT NULL COMMENT '纯数字字母车牌',
  `plate_no_color` varchar(10) DEFAULT NULL COMMENT '车牌底色',
  `car_image_url` varchar(255) DEFAULT NULL COMMENT '车辆照片地址（相对路径）',
  `in_time` datetime DEFAULT NULL COMMENT '入车时间',
  `in_type` tinyint(4) DEFAULT NULL COMMENT '操作类型 0-自动入车 1-手动入车',
  `unique_id` varchar(32) DEFAULT NULL COMMENT '每次进出车事件唯一UUID绑定',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_element_park_id` (`element_park_id`) USING BTREE,
  KEY `index_plate_no` (`plate_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='在场车辆表';

-- 构造表b_present_car_record_area
CREATE TABLE IF NOT EXISTS `b_present_car_record_area` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `area_camera_id` int(11) DEFAULT NULL COMMENT '区域相机id',
  `area_camera_ip` varchar(255) DEFAULT NULL COMMENT '区域相机ip',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `event_id` varchar(36) DEFAULT NULL COMMENT '事件id',
  `area_id` int(11) DEFAULT NULL COMMENT '区域id',
  `plate_no` varchar(100) DEFAULT NULL COMMENT '车牌号',
  `plate_no_simple` varchar(64) DEFAULT NULL COMMENT '纯数字字母车牌',
  `plate_no_color` varchar(10) DEFAULT NULL COMMENT '车牌底色',
  `car_image_url` varchar(255) DEFAULT NULL COMMENT '车辆抓拍照片路径',
  `in_time` datetime DEFAULT NULL COMMENT '入车时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(100) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(100) DEFAULT NULL COMMENT '更新者',
  `data_source` tinyint(1) DEFAULT '0' COMMENT '数据来源 0：区域相机 1：立体车位',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='在场车辆表（区域相机使用）';

-- 构造表b_recognition_record
CREATE TABLE IF NOT EXISTS `b_recognition_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `park_addr` int(11) DEFAULT NULL COMMENT '车位地址',
  `plate_no` varchar(64) DEFAULT NULL COMMENT '车牌',
  `car_image_url` varchar(255) DEFAULT NULL COMMENT '车辆照片地址（相对路径）',
  `plate_no_reliability` int(11) DEFAULT NULL COMMENT '图片识别车牌可信度',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='识别记录表';

-- 构造表berth_rate_info
CREATE TABLE IF NOT EXISTS `berth_rate_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `time` datetime NOT NULL COMMENT '时间',
  `all_park_number` int(11) DEFAULT NULL COMMENT '当前车场全部车位数',
  `all_berth_data` varchar(10) DEFAULT NULL COMMENT '当前全车场泊位占用数据',
  `berth_type` tinyint(1) NOT NULL COMMENT '泊位类型，0：根据楼层区分，1：根据车位类型区分',
  `berth_info` varchar(256) DEFAULT NULL COMMENT '泊位占用信息,如B1:100,B2:100这样的数据',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COMMENT='泊位使用率信息表';

-- 构造表color_transparency_styles
CREATE TABLE IF NOT EXISTS `color_transparency_styles` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `map_styles_id` int(11) NOT NULL COMMENT '地图样式id',
  `occupy_flash` int(11) DEFAULT NULL COMMENT '占用时车位闪烁 0 不闪烁 1 闪烁',
  `free_flash` int(11) DEFAULT NULL COMMENT '空闲时车位闪烁开关  0 不闪烁 1 闪烁',
  `select_color` varchar(32) DEFAULT NULL COMMENT '选中时颜色',
  `fill_color` varchar(32) DEFAULT NULL COMMENT '填充颜色',
  `border_color` varchar(32) DEFAULT NULL COMMENT '边框颜色',
  `transparency` int(11) DEFAULT NULL COMMENT '透明度',
  `type` tinyint(4) DEFAULT NULL COMMENT '-1:柱子,-2:地面,-3:背景,1:普通车位,2:新能源车位,3:时租车,4:幼稚园班车,5:自定义元素,6:区域,7:立体车位',
  `area_id` int(11) DEFAULT NULL COMMENT '区域id',
  `element_custom_id` int(11) DEFAULT NULL COMMENT '当type=5时，存放自定义元素id',
  `is_show_name` tinyint(1) DEFAULT '0' COMMENT '是否显示元素名称；0：不显示，1：显示',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除（0：未删除，1：已删除）',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `occupy_fill_color` varchar(32) DEFAULT NULL COMMENT '车位占用时填充颜色',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_map_styles_id` (`map_styles_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='颜色透明度配置表';

-- 构造表coordinate
CREATE TABLE IF NOT EXISTS `coordinate` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增，主键',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id',
  `element_id` int(11) DEFAULT NULL COMMENT '元素id',
  `type` tinyint(4) DEFAULT NULL COMMENT '元素类型详情见枚举1 地面  2 柱子  3 车位  4蓝牙信标  5路网 6找车机 7通行设施  8自定义元素  9不可通行路网  10子屏 11屏',
  `attribute` varchar(50) DEFAULT '' COMMENT '冗余字段 （当字段type=5,则begin表示起点，end表示终点）',
  `x_point` varchar(50) DEFAULT NULL COMMENT 'x坐标',
  `y_point` varchar(50) DEFAULT NULL COMMENT 'y坐标',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除0未删除1已删除',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_element_id` (`element_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='元素坐标表';

-- 构造表device_escalation
CREATE TABLE IF NOT EXISTS `device_escalation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `device_ip` varchar(255) DEFAULT NULL COMMENT '上报设备IP',
  `device_port` int(11) DEFAULT NULL COMMENT '上报设备端口',
  `floor_name` varchar(255) DEFAULT NULL COMMENT '楼层名称',
  `area_name` varchar(255) DEFAULT NULL COMMENT '区域名称',
  `park_no` varchar(255) DEFAULT NULL COMMENT '车位编号',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `exception` tinyint(1) DEFAULT '0' COMMENT '异常问题(0：正常， 1：车位编号重复， 2：无车位编号)',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备信息上报表';

-- 构造表element_beacon
CREATE TABLE IF NOT EXISTS `element_beacon` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id lot_info id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `name` varchar(255) DEFAULT NULL COMMENT '名称',
  `uuid` varchar(50) DEFAULT NULL COMMENT '蓝牙信标的uuid',
  `minor` varchar(30) DEFAULT NULL COMMENT '蓝牙信标的minor',
  `major` varchar(30) DEFAULT NULL COMMENT '蓝牙信标的major',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除0未删除1已删除',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='蓝牙信标';

-- 构造表element_column
CREATE TABLE IF NOT EXISTS `element_column` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `name` varchar(255) DEFAULT NULL COMMENT '名称',
  `height` double DEFAULT NULL COMMENT '高度 柱子高度2米',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除0未删除1已删除',
  `creator` varchar(255) DEFAULT NULL COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(255) DEFAULT NULL COMMENT '更新人',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='柱子元素表';

-- 构造表element_connector
CREATE TABLE IF NOT EXISTS `element_connector` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id lot_info id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `name` varchar(255) DEFAULT NULL COMMENT '名称',
  `species` tinyint(4) DEFAULT NULL COMMENT '种类 1：直梯 2：护梯 3：楼梯 4：出入口',
  `associated_connector_ids` varchar(255) DEFAULT NULL COMMENT '关联设施ids',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除0未删除1已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_map_floor_id` (`floor_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='通行设施';

-- 构造表element_custom
CREATE TABLE IF NOT EXISTS `element_custom` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id',
  `name` varchar(255) DEFAULT '' COMMENT '名称',
  `height` double DEFAULT '0.1' COMMENT '高度 默认0.1m',
  `suspend_height` double DEFAULT '0' COMMENT '离地高度 默认0m',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除 0未删除 1已删除',
  `creator` varchar(255) DEFAULT '' COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(255) DEFAULT '' COMMENT '更新人',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_lot_id` (`lot_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='自定义元素表';

-- 构造表element_custom_detail
CREATE TABLE IF NOT EXISTS `element_custom_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `element_custom_id` int(11) DEFAULT NULL COMMENT '自定义元素id',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `name` varchar(255) DEFAULT '' COMMENT '名称',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除 0未删除 1已删除',
  `creator` varchar(255) DEFAULT '' COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(255) DEFAULT '' COMMENT '更新人',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_element_custom_id` (`element_custom_id`) USING BTREE,
  KEY `idx_floor_id` (`floor_id`) USING BTREE,
  KEY `idx_lot_id` (`lot_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='自定义元素详情表';

-- 构造表element_ground
CREATE TABLE IF NOT EXISTS `element_ground` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `name` varchar(255) DEFAULT NULL COMMENT '名称',
  `height` double DEFAULT NULL COMMENT '高度 地面默认0.1米',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除0未删除1已删除',
  `creator` varchar(255) DEFAULT NULL COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(255) DEFAULT NULL COMMENT '更新人',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_map_floor_id` (`floor_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地面元素表';

-- 构造表element_impassable_path
CREATE TABLE IF NOT EXISTS `element_impassable_path` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id lot_info id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除，0未删除，1已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_floor_id` (`floor_id`) USING BTREE,
  KEY `idx_lot_id` (`lot_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='不可通行路线';

-- 构造表element_machine
CREATE TABLE IF NOT EXISTS `element_machine` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id lot_info id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `name` varchar(255) DEFAULT NULL COMMENT '名称',
  `species` tinyint(4) DEFAULT NULL COMMENT '种类 1：立式找车机 2：壁式找车机',
  `ip` varchar(32) DEFAULT NULL COMMENT '找车机ip',
  `direction_num` int(11) DEFAULT '0' COMMENT '朝向(度数)',
  `unique_identification_field` varchar(50) DEFAULT NULL COMMENT '唯一标识',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除0未删除1已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_ip` (`ip`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='找车机';

-- 构造表element_model
CREATE TABLE IF NOT EXISTS `element_model` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lot_id` int(11) NOT NULL COMMENT '车场id',
  `floor_id` int(11) NOT NULL COMMENT '楼层id',
  `element_type` int(11) DEFAULT NULL COMMENT '模型类型',
  `element_name` varchar(255) DEFAULT NULL COMMENT '模型名称',
  `rotation_angle` double DEFAULT '0' COMMENT '模型的朝向设置（0~360），实时预览，默认为0',
  `x_point` int(11) DEFAULT NULL COMMENT 'X坐标',
  `y_point` int(11) DEFAULT NULL COMMENT 'y坐标',
  `scale` double DEFAULT '1' COMMENT '缩放比例，模型的大小控制（0.5-2），实时预览，默认为1',
  `suspend_height` double DEFAULT '0' COMMENT '离地高度，模型底面离地面上表面的距离（0-10.0），默认为0',
  `creator` varchar(255) DEFAULT '' COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(255) DEFAULT '' COMMENT '更新人',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_floor_id` (`floor_id`) USING BTREE,
  KEY `idx_lot_id` (`lot_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='模型';

-- 构造表element_park
CREATE TABLE IF NOT EXISTS `element_park` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id lot_info id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `name` varchar(255) DEFAULT NULL COMMENT '名称',
  `height` double DEFAULT NULL COMMENT '高度 地面默认0.1米 车位默认高度0.1米 柱子默认2米',
  `park_category` tinyint(4) DEFAULT NULL COMMENT '车位种类1 为普通车位 2 为新能源车位 3 为立体车位 4共享车位',
  `stereoscopic_park_camera_addr` int(11) DEFAULT NULL COMMENT '立体车位对应的相机地址',
  `park_no` varchar(50) DEFAULT NULL COMMENT '车位号编号',
  `park_addr` int(11) DEFAULT NULL COMMENT '车位地址',
  `x_center` varchar(100) DEFAULT NULL COMMENT '车位中心点坐标X',
  `y_center` varchar(100) DEFAULT NULL COMMENT '车位中心点坐标y',
  `control` tinyint(4) DEFAULT '0' COMMENT '车位控制 0-自动控制 1-手动控制',
  `status` tinyint(1) DEFAULT '0' COMMENT '车位状态 0-空闲 1-占用 2-故障 3-停止服务',
  `area_id` int(11) DEFAULT NULL COMMENT 'area_info区域id',
  `toward` int(11) DEFAULT '0' COMMENT '方向朝向（0-360角度整数存值）',
  `warning` tinyint(1) DEFAULT '0' COMMENT '告警状态  1：告警中  0：未告警',
  `last_leave_time` timestamp NULL DEFAULT NULL COMMENT '车位最近一次出车时间',
  `cpp_report_count` int(11) DEFAULT '0' COMMENT 'C++程序给这个车位连续上报异常状态的次数',
  `unique_identification_field` varchar(32) DEFAULT NULL COMMENT '车位唯一标识字段',
  `change_push_flag` tinyint(1) DEFAULT '0' COMMENT '车位状态变化推送标识（单车场接口使用）  0-无变化，无需推送  1-有变化，需推送',
  `change_push_time` datetime DEFAULT NULL COMMENT '车位状态变化时间（单车场接口使用）',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除0未删除1已删除',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `parking_capture` varchar(255) DEFAULT NULL COMMENT '车位相机抓拍照片路径',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_park_addr` (`park_addr`) USING BTREE,
  KEY `index_area_id` (`area_id`) USING BTREE,
  KEY `index_park_no` (`park_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车位';

-- 构造表element_path
CREATE TABLE IF NOT EXISTS `element_path` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id lot_info id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `entry` tinyint(4) DEFAULT '0' COMMENT '方向，预留字段，0 双向通行，1 正向通行，2反向通行',
  `distance` varchar(255) DEFAULT NULL COMMENT '路线长度',
  `road_type` tinyint(1) DEFAULT '3' COMMENT '1  人行  2   车行  3  人/车行',
  `tag` int(11) DEFAULT '0' COMMENT '权限标签',
  `weight` int(11) DEFAULT NULL COMMENT '权重',
  `roadnet_floor` int(11) DEFAULT '0' COMMENT '1，就是表示通行设施连接其他楼层通行设施路网',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除，0未删除，1已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_floor_id` (`floor_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='路网';

-- 构造表element_screen
CREATE TABLE IF NOT EXISTS `element_screen` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id lot_info id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `name` varchar(255) DEFAULT NULL COMMENT '名称',
  `species` tinyint(4) DEFAULT NULL COMMENT '种类 1：LED屏 2：LCD屏',
  `screen_addr` int(11) DEFAULT NULL COMMENT '屏地址',
  `sub_screen_num` tinyint(4) DEFAULT NULL COMMENT '子屏数 1：单向屏 2：双向屏 3：三向屏',
  `screen_type` tinyint(4) DEFAULT NULL COMMENT '屏类型 1-单拼接屏 2-双拼接屏 3-三拼接屏',
  `show_template` tinyint(4) DEFAULT NULL COMMENT '展示模板',
  `remark` varchar(255) DEFAULT '' COMMENT '备注',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除 0未删除 1已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `direction` int(11) DEFAULT '1' COMMENT '屏方向（屏顺序配置字段，用来控制屏从左到右地址是递增(1)还是递减(-1)）',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_screen_addr` (`screen_addr`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='屏';

-- 构造表element_screen_child
CREATE TABLE IF NOT EXISTS `element_screen_child` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `parent_id` int(11) DEFAULT NULL COMMENT '主屏id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id  冗余字段  屏配置好后不能更改楼层，所以冗余这个字段',
  `screen_addr` int(11) DEFAULT NULL COMMENT '屏地址',
  `description` varchar(255) DEFAULT NULL COMMENT '描述',
  `screen_species` tinyint(4) DEFAULT NULL COMMENT '屏种类 1：LED屏 2：LCD屏',
  `screen_category` tinyint(4) DEFAULT '1' COMMENT '屏类别   1：LED网络屏、  2：485总屏、3：485子屏',
  `screen_type` tinyint(4) DEFAULT '1' COMMENT '屏类型   1：普通屏、2：总屏',
  `show_type` tinyint(4) DEFAULT '1' COMMENT '展示内容   1：关联车位空车位数、2：关联车位占用车位数、3：车场总空车位数、4：车位总占用车位数、5：固定显示数值',
  `area_id` int(11) DEFAULT NULL COMMENT '区域id',
  `revise_num` int(11) DEFAULT '0' COMMENT '校正数值 （结果数值加上这个值）',
  `critical_num` int(11) DEFAULT '0' COMMENT '临界值（小于临界值直接输出0）',
  `constant_num` int(11) DEFAULT '0' COMMENT '固定显示数值',
  `arrow_position` tinyint(4) DEFAULT '0' COMMENT '箭头位置   0：右   1：左',
  `arrow_direction` tinyint(4) DEFAULT '0' COMMENT '箭头方向   0：右   1：左   2：上   3：下   17：左上   18：左下   19：右上   20：右下',
  `show_color` tinyint(4) DEFAULT '0' COMMENT '显示颜色   0：红   1：橙   2：绿   3：根据数值',
  `park_type` tinyint(4) DEFAULT '0' COMMENT '车位类型   0：正常、1：残障',
  `show_num` int(11) DEFAULT NULL COMMENT '显示数字（对应的屏应该展示的数字，定时任务以及进出车和车屏关系变动会更新这个字段）',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '删除状态   0：未删除   1：已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(50) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(50) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_parent_id` (`parent_id`) USING BTREE,
  KEY `index_screen_addr` (`screen_addr`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='子屏表';

-- 构造表element_screen_park_relation
CREATE TABLE IF NOT EXISTS `element_screen_park_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `screen_id` int(11) DEFAULT NULL COMMENT '子屏id  element_screen_child表的id',
  `park_id` int(11) DEFAULT NULL COMMENT '车位id  element_park表的id',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(255) DEFAULT NULL COMMENT '创建者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_screen_id` (`screen_id`) USING BTREE,
  KEY `idx_park_id` (`park_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='屏和车位的关系表';

-- 构造表f_config
CREATE TABLE IF NOT EXISTS `f_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `config_code` varchar(64) DEFAULT '' COMMENT '配置编码',
  `config_value` varchar(64) DEFAULT '' COMMENT '配置值',
  `config_desc` varchar(255) DEFAULT '' COMMENT '配置描述',
  `attribute` varchar(64) DEFAULT '' COMMENT '额外字段',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0：未删除，1：已删除）',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `aws_enable_switch` tinyint(1) DEFAULT '1' COMMENT '是否上传车场问题图片到ai中心 0:开启  1:关闭',
  `guidance_swagger_switch` tinyint(1) DEFAULT '1' COMMENT 'parking_guidance服务swagger配置开关 0:开启  1:关闭',
  `channel_swagger_switch` tinyint(1) DEFAULT '1' COMMENT 'channel_service服务swagger配置开关 0:开启  1:关闭',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_config_code` (`config_code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';

-- 构造表face_info
CREATE TABLE IF NOT EXISTS `face_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plate_no` varchar(50) DEFAULT '' COMMENT '车牌号码',
  `face_info` longtext COMMENT '人脸信息数据',
  `is_temp` int(11) DEFAULT '0' COMMENT '是否临时数据',
  `face_id` varchar(50) DEFAULT '' COMMENT '人脸信息唯一值',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0：未删除，1：已删除）',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='人脸信息表';

-- 构造表floor_info
CREATE TABLE IF NOT EXISTS `floor_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `lot_id` int(11) NOT NULL COMMENT '车场id lot_info id',
  `floor_name` varchar(255) NOT NULL COMMENT '楼层名称',
  `status` int(11) DEFAULT NULL COMMENT '状态 1启用 2停用',
  `sort` int(11) NOT NULL COMMENT '楼层顺序（数字越大，楼层越高）',
  `scroll_ratio` int(11) DEFAULT '10' COMMENT '缩放比例（%）',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除（0：未删除，1：已删除）',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `floor_unique_identification` varchar(32) DEFAULT NULL COMMENT '楼层唯一标识字段',
  `floor_capture` varchar(255) DEFAULT NULL COMMENT '楼层底图截图保存URL',
  `capture_source` tinyint(1) DEFAULT '0' COMMENT '楼层底图来源方式，0:3D手动截图 1:2D地图照片迁移',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='楼层信息';

-- 构造表general_config
CREATE TABLE IF NOT EXISTS `general_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `config_key` varchar(255) DEFAULT NULL COMMENT '字段唯一标识，禁止重复',
  `description` varchar(255) DEFAULT NULL COMMENT '字段详细作用描述',
  `config_value` varchar(255) DEFAULT NULL COMMENT '字段具体配置信息',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COMMENT='通用参数配置信息表';

-- 构造表image_styles
CREATE TABLE IF NOT EXISTS `image_styles` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `map_styles_id` int(11) NOT NULL COMMENT '地图样式id',
  `record_beacon` varchar(255) DEFAULT NULL COMMENT '已录入蓝牙图标url',
  `no_record_beacon` varchar(255) DEFAULT NULL COMMENT '未录入蓝牙图标url',
  `vertical_machine` varchar(255) DEFAULT NULL COMMENT '立式找车机图标url',
  `wall_machine` varchar(255) DEFAULT NULL COMMENT '壁挂式找车机图标url',
  `vertical_ladder_connector` varchar(255) DEFAULT NULL COMMENT '直梯图标url',
  `escalator_connector` varchar(255) DEFAULT NULL COMMENT '扶梯图标url',
  `stairs_connector` varchar(255) DEFAULT NULL COMMENT '楼梯图标url',
  `passageway_connector` varchar(255) DEFAULT NULL COMMENT '出入口图标url',
  `screen_lcd_url` varchar(255) DEFAULT '' COMMENT 'LCD屏图标URL',
  `screen_led_url` varchar(255) DEFAULT '' COMMENT 'LED屏图标URL',
  `is_show_name_machine` tinyint(1) DEFAULT '0' COMMENT '找车机是否显示元素名称  0：不显示  1：显示',
  `is_show_name_connector` tinyint(1) DEFAULT '0' COMMENT '通行设施是否显示元素名称  0：不显示  1：显示',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除（0：未删除，1：已删除）',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_map_styles_id` (`map_styles_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='图标配置表';

-- 构造表info_across_floor
CREATE TABLE IF NOT EXISTS `info_across_floor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_id` int(11) DEFAULT NULL COMMENT '起点楼层ID',
  `end_id` int(11) DEFAULT NULL COMMENT '终点楼层ID',
  `end_name` varchar(255) DEFAULT NULL COMMENT '终点楼层名称',
  `start_name` varchar(255) DEFAULT NULL COMMENT '起点楼层名称',
  `across_elevator_id` int(11) DEFAULT NULL COMMENT '通行设施ID',
  `across_elevator_name` varchar(255) DEFAULT NULL COMMENT '通行设施名称',
  `img_src` varchar(255) DEFAULT NULL COMMENT '提示图片',
  `across_type` int(11) DEFAULT '0' COMMENT '跨层类型(0:楼层到楼层 1:查询机到楼层)',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0：未删除，1：已删除）',
  `creator` varchar(255) DEFAULT NULL COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(255) DEFAULT NULL COMMENT '更新人',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='跨层寻车用指引设置表';

-- 构造表info_machine_config
CREATE TABLE IF NOT EXISTS `info_machine_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inquire_ways` varchar(200) DEFAULT NULL COMMENT '查询方式',
  `empty_plate_record_count` int(11) DEFAULT '25' COMMENT '空车牌查询显示记录上限',
  `plate_max_num` int(11) DEFAULT '6' COMMENT '车牌号输入上限',
  `park_max_num` int(11) DEFAULT '6' COMMENT '车位号输入上限',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0：未删除，1：已删除）',
  `creator` varchar(255) DEFAULT NULL COMMENT '创建人',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(255) DEFAULT NULL COMMENT '更新人',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `websocket_version_code` varchar(32) DEFAULT NULL COMMENT '用于判断当前人脸信息和找车机上是否一致，这个随机值下发给找车机进行判断',
  `is_open_print` tinyint(1) DEFAULT '1' COMMENT '是否启用停车打印功能 0:不启用 1:启用',
  `machine_map_switch` tinyint(1) DEFAULT '1' COMMENT '找车机是否开启3D地图(1为开启  0 为关闭)',
  `schedule_face` tinyint(1) DEFAULT '1' COMMENT '定时给找车机推送车辆出场，删除人脸数据(0为开启  1为关闭)',
  `is_open_qrcode` tinyint(1) DEFAULT '0' COMMENT '是否显示找车二维码(0：否，1：是)',
  `rotation_switch` int(11) DEFAULT '1' COMMENT '初始化时找车机地图是否根据找车机朝向旋转(0为开启  1为关闭)，默认关闭',
  `rotation_angle` int(11) DEFAULT '0' COMMENT '初始化时找车机旋转角度，0-360',
  `language_support` tinyint(4) DEFAULT '0' COMMENT '语言支持  0=中文+英文  1=中文  2=英文',
  `foregin_language` varchar(50) DEFAULT NULL COMMENT '设置的第三种语言支持 ms=马来西亚 esp=西班牙 未设置则返回空',
  `route_qr_switch` tinyint(4) DEFAULT '0' COMMENT '找车路线二维码开关  0=关  1=开',
  `route_qr_type` tinyint(4) DEFAULT '0' COMMENT '找车路线二维码类型  0=自定义二维码',
  `route_qr_url` varchar(255) DEFAULT NULL COMMENT '找车路线二维码图片路径',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='找车机常用参数表';

-- 构造表ini_config
CREATE TABLE IF NOT EXISTS `ini_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `dsp_recog` tinyint(1) DEFAULT '0' COMMENT '控制软识别与硬识别 0 软识别, 1 硬识别',
  `witch` tinyint(1) DEFAULT '0' COMMENT '控制故障状态的设备的开关 0 关闭， 1 开启',
  `comname` varchar(255) DEFAULT NULL COMMENT '连接服务器的端口号 windows下是COM5, linux下是 /dev/ttyS0',
  `ret` tinyint(1) DEFAULT '0' COMMENT '控制TCP还是485通讯 0 tcp, 1 485',
  `province` varchar(255) DEFAULT NULL COMMENT '车牌的默认省份(省份简称汉字) 默认为空',
  `pic_switch` tinyint(1) DEFAULT '0' COMMENT '是否开启空车牌图片收集功能  1 开启,  0 关闭',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='C++参数配置表';

-- 构造表internationalization
CREATE TABLE IF NOT EXISTS `internationalization` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(100) NOT NULL COMMENT '代码，前缀是front.的为前端，前缀是server.的为后端',
  `description` varchar(100) DEFAULT NULL COMMENT '描述',
  `chinese` varchar(500) DEFAULT NULL COMMENT '简体中文',
  `english` varchar(500) DEFAULT NULL COMMENT '英文',
  `other1` varchar(500) DEFAULT NULL COMMENT '其他语言1，预留字段',
  `other2` varchar(500) DEFAULT NULL COMMENT '其他语言2，预留字段',
  `other3` varchar(500) DEFAULT NULL COMMENT '其他语言3，预留字段',
  `other4` varchar(500) DEFAULT NULL COMMENT '其他语言4，预留字段',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '删除状态  0：未删除   1：已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `udx_code` (`code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=29895 DEFAULT CHARSET=utf8mb4 COMMENT='国际化';

-- 构造表internationalization_relation
CREATE TABLE IF NOT EXISTS `internationalization_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(100) DEFAULT '待配置' COMMENT '语言名称，用于显示在前端用于选择语言',
  `field` varchar(100) DEFAULT NULL COMMENT 'internationalization表的字段名',
  `shorthand` varchar(100) DEFAULT NULL COMMENT '语言简称，用于前端组件自带的国际化，如：zh_CN：简体中文  en_GB：英语',
  `sort` int(11) DEFAULT '0' COMMENT '排序',
  `status` tinyint(1) DEFAULT '0' COMMENT '状态  0：未启用   1：启用',
  `update_package_status` tinyint(1) DEFAULT '0' COMMENT '上传语言包状态  0：未上传   1：已上传',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COMMENT='国际化字段与语言关系表';

-- 构造表lcd_advertisement_config
CREATE TABLE IF NOT EXISTS `lcd_advertisement_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `lcd_advertisement_scheme_id` int(11) DEFAULT NULL COMMENT 'LCD屏广告方案id',
  `remark` varchar(255) DEFAULT '' COMMENT '备注',
  `play_sort` int(11) DEFAULT NULL COMMENT '播放顺序',
  `file_name` varchar(255) DEFAULT '' COMMENT '文件名',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除0未删除1已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_lcd_advertisement_scheme_id` (`lcd_advertisement_scheme_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='LCD屏广告配置表';

-- 构造表lcd_advertisement_scheme
CREATE TABLE IF NOT EXISTS `lcd_advertisement_scheme` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(255) DEFAULT '' COMMENT '方案名称',
  `species` tinyint(4) DEFAULT NULL COMMENT '类型 1：图片 2：视频',
  `carousel_seconds` int(11) DEFAULT '0' COMMENT '轮播时间 单位s(秒)',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除0未删除1已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='LCD屏广告方案表';

-- 构造表lcd_screen_config
CREATE TABLE IF NOT EXISTS `lcd_screen_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `element_screen_id` int(11) DEFAULT NULL COMMENT '主屏id',
  `show_type` tinyint(4) DEFAULT NULL COMMENT '显示内容 1：引导内容 2：广告',
  `attribute_id` int(11) DEFAULT NULL COMMENT '若显示内容是 1，则为子屏id， 若显示内容为2 则为广告id',
  `show_sort` int(11) DEFAULT NULL COMMENT '显示顺序',
  `belong_id` tinyint(4) DEFAULT NULL COMMENT '所属id id相同表示属于同一个物理屏',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除0未删除1已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_element_screen_id` (`element_screen_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='LCD屏配置';

-- 构造表light_scheme_plan
CREATE TABLE IF NOT EXISTS `light_scheme_plan` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(50) DEFAULT NULL COMMENT '方案名称',
  `system_type` tinyint(4) DEFAULT '1' COMMENT '设备类型  0-DSP车位相机   1-NODE节点控制器',
  `light_type` tinyint(4) DEFAULT '1' COMMENT '灯类型   1-有线多彩灯  2-有线双色灯',
  `occupy_color` tinyint(4) DEFAULT NULL COMMENT '占用颜色',
  `free_color` tinyint(4) DEFAULT NULL COMMENT '空闲颜色',
  `warning_color` tinyint(4) DEFAULT NULL COMMENT '告警颜色',
  `send_time` datetime DEFAULT NULL COMMENT '下发时间',
  `status` tinyint(4) DEFAULT '1' COMMENT '下发状态  1-未生效  2-下发成功  3-下发失败  4-取消',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车位灯方案下发计划';

-- 构造表light_scheme_plan_park_relation
CREATE TABLE IF NOT EXISTS `light_scheme_plan_park_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `plan_id` int(11) DEFAULT NULL COMMENT '车位灯方案下发计划id',
  `element_park_id` int(11) DEFAULT NULL COMMENT '车位id',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车位灯方案下发计划与车位关系表';

-- 构造表lot_info
CREATE TABLE IF NOT EXISTS `lot_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `lot_code` varchar(100) DEFAULT NULL COMMENT '车场编码',
  `lot_name` varchar(255) NOT NULL COMMENT '车场名称',
  `device_id` varchar(100) DEFAULT NULL COMMENT '场端设备id，用于统一接口通信',
  `addr` varchar(1000) DEFAULT NULL COMMENT '车场地址',
  `tel` varchar(50) DEFAULT NULL COMMENT '联系电话',
  `secret` varchar(50) DEFAULT NULL COMMENT '密钥（接口加密使用）',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `system_type` tinyint(1) DEFAULT '3' COMMENT 'C++端部署形式  1:引导系统  2:找车系统  3:引导系统和找车系统同时部署',
  `server_ip` varchar(32) DEFAULT '127.0.0.1' COMMENT '服务器IP',
  `device_ip_prefix` varchar(32) DEFAULT '192.168.' COMMENT '设备IP网段前缀',
  `park_repeat_switch` tinyint(1) DEFAULT '0' COMMENT '车位编号限制 0:不允许重复的车位编号  1:允许重复车位编号',
  `map_type` tinyint(1) DEFAULT '1' COMMENT '地图类型 0:2D地图 1:3D地图',
  `status` int(11) DEFAULT '1' COMMENT '车场状态(0 禁用  1 启用） ',
  `machine_debug` int(11) DEFAULT '0' COMMENT '找车机是否为调试模式(0 关闭 1 开启)',
  `lisence_authorize_code` varchar(1024) DEFAULT NULL COMMENT 'Lisence授权码',
  `lisence_trial_period` datetime DEFAULT NULL COMMENT 'Lisence首次默认30天试用期(寻车服务首次启动时，开始生效)，开始试用时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='车场信息';

-- 构造表machine_advertisement_config
CREATE TABLE IF NOT EXISTS `machine_advertisement_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `machine_ad_scheme_id` int(11) DEFAULT NULL COMMENT '找车机广告方案id',
  `screen_ad_scheme_id` int(11) DEFAULT NULL COMMENT '广告屏广告方案id',
  `machine_ip` varchar(64) DEFAULT '' COMMENT '找车机ip',
  `type` tinyint(4) DEFAULT '0' COMMENT '类型 0-全局 1-单独配置',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_machine_ad_scheme_id` (`machine_ad_scheme_id`) USING BTREE,
  KEY `idx_machine_ip` (`machine_ip`) USING BTREE,
  KEY `idx_screen_ad_scheme_id` (`screen_ad_scheme_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='找车机广告配置';

-- 构造表map_styles
CREATE TABLE IF NOT EXISTS `map_styles` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id',
  `name` varchar(32) NOT NULL COMMENT '样式名称',
  `remark` varchar(32) DEFAULT NULL COMMENT '备注',
  `is_using` tinyint(1) DEFAULT '0' COMMENT '当前配置使用状态 0：未使用，1：正在使用',
  `deleted` tinyint(1) DEFAULT '0' COMMENT 'true：启用，false：禁用（原作为是否删除表示，但此处做逻辑删除，遂复用这字段，真正删除使用的物理删除）',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地图样式配置表';

-- 构造表node_device
CREATE TABLE IF NOT EXISTS `node_device` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `addr` int(11) DEFAULT NULL COMMENT 'IPCAM总地址|DSP总地址',
  `device_type` int(11) DEFAULT NULL COMMENT '节点设备类型：1：相机  2：485节点 3：网络4字节 4：网络8字节 5：网络10 字节',
  `relate_park_num` int(11) DEFAULT NULL COMMENT '关联车位数',
  `status` int(11) DEFAULT '0' COMMENT '状态（0 离线  1在线）',
  `congestion_status` int(11) DEFAULT NULL COMMENT '区域相机拥堵状态（0 不拥堵   1 拥堵）',
  `online_start_time` datetime DEFAULT NULL COMMENT '最近一次在线开始时间',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `type` int(11) DEFAULT NULL COMMENT '用于区分节点设备和区域设备， 1：节点设备、  2： 区域设备 ',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(255) DEFAULT NULL COMMENT '创建人',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(255) DEFAULT NULL COMMENT '最近一次更新人',
  `deleted` int(11) DEFAULT '0' COMMENT '是否删除  0：未删除、  1：已删除',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='节点设备';

-- 构造表node_device_relate
CREATE TABLE IF NOT EXISTS `node_device_relate` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `area_device_id` int(11) DEFAULT NULL COMMENT '区域设备id  node_device表的id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `area_id` int(11) DEFAULT NULL COMMENT '区域id',
  `entrance_exit` tinyint(4) DEFAULT NULL COMMENT '相机放置类型  1：入口   2：出口   3：出入口',
  `entrance_exit_name` varchar(255) DEFAULT NULL COMMENT '枚举类型：  入口   出口  出入口',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='区域设备与区域的关系表';

-- 构造表parking_light_area_relation
CREATE TABLE IF NOT EXISTS `parking_light_area_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `parking_light_scheme_id` int(11) DEFAULT NULL COMMENT '车位灯方案id',
  `area_id` int(11) DEFAULT NULL COMMENT '区域id',
  `area_name` varchar(64) DEFAULT NULL COMMENT '区域名称',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_area_id` (`area_id`) USING BTREE,
  KEY `index_parking_light_scheme_id` (`parking_light_scheme_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车位灯方案和区域的关系表';

-- 构造表parking_light_scheme
CREATE TABLE IF NOT EXISTS `parking_light_scheme` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(255) DEFAULT '' COMMENT '名称',
  `lot_id` int(11) DEFAULT NULL COMMENT '车场id',
  `occupy_color` tinyint(4) DEFAULT '0' COMMENT '占用颜色',
  `free_color` tinyint(4) DEFAULT '0' COMMENT '空闲颜色',
  `warning_color` tinyint(4) DEFAULT '0' COMMENT '告警颜色',
  `type` tinyint(4) DEFAULT NULL COMMENT '设备类型  0-DSP车位相机   1-NODE节点控制器',
  `light_type` tinyint(4) DEFAULT '1' COMMENT '灯类型   1-有线多彩灯  2-有线双色灯',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除0未删除1已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `custom_occupy_color` varchar(32) DEFAULT NULL COMMENT '自定义占用颜色',
  `custom_warning_color` varchar(32) DEFAULT NULL COMMENT '自定义告警颜色',
  `custom_free_color` varchar(32) DEFAULT NULL COMMENT '自定义空闲颜色',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车位灯方案';

-- 构造表permissions
CREATE TABLE IF NOT EXISTS `permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(255) DEFAULT NULL COMMENT '名称',
  `router` varchar(255) DEFAULT NULL COMMENT '路由',
  `type` tinyint(4) DEFAULT NULL COMMENT '权限类型 1:菜单 2:权限抽象功能 3:按钮 4:普通接口 5:基础权限接口（所有角色都可以访问） ',
  `icon` varchar(255) DEFAULT NULL COMMENT '图标',
  `permission_code` varchar(255) DEFAULT NULL COMMENT '权限标识 ',
  `internationalization_code` varchar(255) DEFAULT NULL COMMENT '国际化code',
  `parent_id` int(11) DEFAULT NULL COMMENT '父权限id',
  `status` tinyint(4) DEFAULT NULL COMMENT '开关（1开0关）',
  `sort` int(11) DEFAULT '0' COMMENT '排序字段',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除 0未删除 1已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(255) DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updator` varchar(255) DEFAULT NULL COMMENT '更新人',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=591 DEFAULT CHARSET=utf8mb4 COMMENT='权限';

-- 构造表role
CREATE TABLE IF NOT EXISTS `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(255) DEFAULT NULL COMMENT '角色名称',
  `description` varchar(255) DEFAULT NULL COMMENT '备注',
  `enable` tinyint(1) DEFAULT '0' COMMENT '启用状态  1：启用  0：禁用',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '删除状态  1：已删除  0：未删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(50) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(50) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='角色';

-- 构造表role_permission_relation
CREATE TABLE IF NOT EXISTS `role_permission_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` int(11) DEFAULT NULL COMMENT '角色id',
  `permission_id` int(11) DEFAULT NULL COMMENT '权限id',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(50) DEFAULT NULL COMMENT '创建者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=971 DEFAULT CHARSET=utf8mb4 COMMENT='角色权限关系表';

-- 构造表schedule_config
CREATE TABLE IF NOT EXISTS `schedule_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `create_time` datetime DEFAULT NULL COMMENT '更新时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `park_img_duration` int(11) DEFAULT NULL COMMENT '车位照片定时清理',
  `area_park_img_duration` int(11) DEFAULT NULL COMMENT '区域在场车辆定时清理',
  `in_car_push_switch` tinyint(1) DEFAULT '0' COMMENT '车位入车延迟上报，0开启，1关闭',
  `out_car_push_switch` tinyint(1) DEFAULT '0' COMMENT '车位出车延迟上报，0开启，1关闭',
  `update_plate_push_switch` tinyint(1) DEFAULT '1' COMMENT '更新车牌上报，0开启，1关闭',
  `empty_park_push_switch` tinyint(1) DEFAULT NULL COMMENT '空车位上报，0开启，1关闭',
  `empty_park_push_lot` varchar(255) DEFAULT NULL COMMENT '空车位上报车场id',
  `empty_park_push_url` varchar(2000) DEFAULT NULL COMMENT '空车位上报url  多个url直接用英语逗号隔开',
  `park_change_push_switch` tinyint(1) DEFAULT NULL COMMENT '车位状态变更上报',
  `park_change_push_lot` varchar(255) DEFAULT NULL COMMENT '车位状态变更上报车场id',
  `park_change_push_url` varchar(2000) DEFAULT NULL COMMENT '车位状态变更上报url  多个url直接用英语逗号隔开',
  `creator` varchar(255) DEFAULT NULL COMMENT '更新者',
  `url_prefix_config` varchar(255) DEFAULT NULL COMMENT '单车场查询返回图片URL拼接前缀地址',
  `free_space_num_switch` tinyint(1) DEFAULT '1' COMMENT '实时剩余车位数本地文件对接开关，0开启，1关闭',
  `image_upload_switch` tinyint(1) DEFAULT '0' COMMENT '图片上传OSS开关(0:开启,1:关闭)',
  `unified_image_prefix` varchar(255) DEFAULT NULL COMMENT '统一接口查询返回图片URL前缀',
  `post_bus_in_out` tinyint(1) DEFAULT '1' COMMENT '上报出入车 0:开启  1:关闭',
  `post_node_device_status` tinyint(1) DEFAULT '1' COMMENT '节点设备状态变更上报 0:开启  1:关闭',
  `clean_stereoscopic_park_switch` tinyint(1) DEFAULT '1' COMMENT '定时清理立体车位的车牌识别记录 0:开启  1:关闭',
  `free_space_switch` tinyint(1) DEFAULT '1' COMMENT '剩余车位数上报收费系统开关 0:开启  1:关闭',
  `post_node_device_url` varchar(2000) DEFAULT NULL COMMENT '节点设备状态变更上报url  多个url直接用英语逗号隔开',
  `clean_stereoscopic_park_duration` int(11) DEFAULT NULL COMMENT '清理立体车位的车牌识别记录(天)',
  `car_loc_info_switch` tinyint(1) DEFAULT '1' COMMENT '车辆停放位置查询接口开关 0:开启  1:关闭',
  `area_push_switch` tinyint(1) DEFAULT '1' COMMENT '区域进出车上报开关 0:开启  1:关闭',
  `tank_warn_push_switch` tinyint(1) DEFAULT '1' COMMENT '油车告警上报开关 0:开启  1:关闭',
  `light_scheme_duration` int(11) DEFAULT '60' COMMENT '车位灯方案删除 ',
  `grpc_switch` tinyint(1) DEFAULT '1' COMMENT 'gRPC连接云端C++用于统一接口开关 0:开启  1:关闭',
  `screen_cmd_interval` int(11) DEFAULT '30' COMMENT '屏指令下发间隔时间（低频），默认30分钟',
  `screen_cmd_interval_fast` int(11) NOT NULL DEFAULT '8' COMMENT '屏指令下发间隔时间（高频），默认8秒钟',
  `statistic_screen_type` tinyint(4) NOT NULL DEFAULT '1' COMMENT '统计屏数据方式  0=定时统计 1=进出车触发 ',
  `query_recognize_record` tinyint(1) DEFAULT '0' COMMENT '是否查询识别记录 0:开启  1:关闭（开启查询识别记录，关闭查询实时在场车）',
  `plate_match_rule` int(11) DEFAULT '1' COMMENT '车牌匹配规则（0 【完全匹配】只返回除汉字部分完全一致的车牌）;1 【全匹配】 查2222可能返回12222或22221',
  `clean_temp_picture` int(11) DEFAULT '1' COMMENT '清理n天以前的临时识别文件',
  `clean_recognition_table` int(11) DEFAULT '30' COMMENT '车牌识别日志表定时清理（单位：天）',
  `clean_area_picture` int(11) DEFAULT '1' COMMENT '区域照片文件定时清理（单位：天）',
  `warn_switch` int(11) NOT NULL DEFAULT '1' COMMENT '告警开关 1=开 0=关',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='参数配置表';

-- 构造表t_access_config
CREATE TABLE IF NOT EXISTS `t_access_config` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '唯一id',
  `dsp_port` int(11) DEFAULT NULL COMMENT 'dsp 连接端口',
  `node_port` int(11) DEFAULT NULL COMMENT 'node tcp节点连接端口',
  `ip_Pre` varchar(255) DEFAULT NULL COMMENT 'tcp地址拼接前缀',
  `broadcast_times` int(11) DEFAULT NULL COMMENT '广播次数',
  `broadcast_interval` int(11) DEFAULT NULL COMMENT '播放间隔',
  `channel_http` varchar(255) DEFAULT NULL COMMENT 'channel服务url地址',
  `serial_port` varchar(64) DEFAULT NULL COMMENT '串口地址',
  `baud_rate` int(11) DEFAULT NULL COMMENT '波特率',
  `A` int(11) DEFAULT NULL COMMENT '识别模式A',
  `B` int(11) DEFAULT NULL COMMENT '识别模式B',
  `C` int(11) DEFAULT NULL COMMENT '识别模式C',
  `pr_num` int(11) DEFAULT NULL COMMENT '车牌类型长度',
  `army_car` int(11) DEFAULT NULL COMMENT '军车车牌',
  `police_car` int(11) DEFAULT NULL COMMENT '警车车牌',
  `wujing_car` int(11) DEFAULT NULL COMMENT '武警车牌',
  `farm_car` int(11) DEFAULT NULL COMMENT '农用车牌',
  `embassy_car` int(11) DEFAULT NULL COMMENT '大使馆车牌',
  `personality_car` int(11) DEFAULT NULL COMMENT '个性化车牌',
  `civil_car` int(11) DEFAULT NULL COMMENT '民航车牌',
  `new_energy_car` int(11) DEFAULT NULL COMMENT '新能源车牌',
  `type_pr_num` int(11) DEFAULT NULL COMMENT '车牌长度',
  `set_lr_num` int(11) DEFAULT NULL COMMENT '车牌数组长度',
  `set_lpr_cs` int(11) DEFAULT NULL COMMENT '识别种类（0:裁剪，1：A版，2：B版，3：A+B版，4：C版 5：A+C版，6：B+C，7：A+B+C）',
  `province` varchar(12) DEFAULT NULL COMMENT '默认省份',
  `set_priority` int(11) DEFAULT '0' COMMENT '设置三地车牌输出优先级:1:MO 2:HK 3:CN 4:CN>HK>MO 5:MO>CN>HK 6:MO>HK>CN 7:HK>CN>MO 8:HK>MO>CN other:CN>MO>HK',
  `original_picture_path` varchar(255) DEFAULT NULL COMMENT '原图保存路径',
  `front_save_path` varchar(255) DEFAULT NULL COMMENT '前端保存路径',
  `temp_rcv_path` varchar(255) DEFAULT NULL COMMENT '临时文件路径',
  `recognition_path` varchar(255) DEFAULT NULL COMMENT '识别文件路径',
  `recognition_lib_path` varchar(255) DEFAULT NULL COMMENT '识别库地址',
  `switch_serial_port` tinyint(1) DEFAULT '1' COMMENT '485节点串口扫描开关（0：关闭  1：开启）',
  `region_picture_path` varchar(255) DEFAULT NULL COMMENT '区域相机照片保存路径',
  `snap_picture_path` varchar(255) DEFAULT NULL COMMENT '相机抓拍照片保存路径',
  `quality_inspection_picture_path` varchar(255) DEFAULT NULL COMMENT '质检中心抓拍照片保存路径',
  `recognition_switch` tinyint(1) DEFAULT '1' COMMENT '识别库开关，0:关闭 1:开启',
  `free_occupy_switch` tinyint(1) DEFAULT '0' COMMENT '找车系统-有车 和找车系统-无车数据接口上报开关 (0：关闭，1：开启)',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='C++重构配置信息表';

-- 构造表t_car_in_out_statistics
CREATE TABLE IF NOT EXISTS `t_car_in_out_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `floor_id` int(11) NOT NULL COMMENT '楼层id',
  `floor_name` varchar(64) DEFAULT NULL COMMENT '楼层名称',
  `general_num` int(11) DEFAULT '0' COMMENT '普通车数量',
  `energy_num` int(11) DEFAULT '0' COMMENT '新能源车数量',
  `record_start_time` datetime DEFAULT NULL COMMENT '记录开始时间',
  `record_end_time` datetime DEFAULT NULL COMMENT '记录结束时间',
  `type` tinyint(4) DEFAULT '1' COMMENT '统计类型:入车-1 出车-0',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_record_time` (`record_end_time`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='出入车流量统计';

-- 构造表t_login_log
CREATE TABLE IF NOT EXISTS `t_login_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_name` varchar(64) DEFAULT '' COMMENT '用户名',
  `user_account` varchar(64) DEFAULT '' COMMENT '用户账号',
  `user_phone` varchar(64) DEFAULT '' COMMENT '用户电话',
  `login_ip` varchar(64) DEFAULT '' COMMENT '登陆ip',
  `login_time` datetime DEFAULT NULL COMMENT '登陆时间',
  `type` tinyint(4) DEFAULT '0' COMMENT '类型 0-登陆',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_user_account` (`user_account`) USING BTREE,
  KEY `idx_user_name` (`user_name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COMMENT='登陆日志表';

-- 构造表t_server_log
CREATE TABLE IF NOT EXISTS `t_server_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `file_name` varchar(64) DEFAULT '' COMMENT '文件名',
  `file_path` varchar(255) DEFAULT '' COMMENT '文件路径',
  `type` tinyint(4) DEFAULT '0' COMMENT '类型 0-管理后台',
  `log_time` datetime DEFAULT NULL COMMENT '日志时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_file_name` (`file_name`) USING BTREE,
  KEY `idx_log_time` (`log_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8mb4 COMMENT='服务日志表';

-- 构造表user
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(50) DEFAULT NULL COMMENT '用户名',
  `account` varchar(50) DEFAULT NULL COMMENT '账号',
  `password` varchar(500) DEFAULT NULL COMMENT '密码',
  `phone` varchar(11) DEFAULT NULL COMMENT '手机号',
  `remark` varchar(200) DEFAULT NULL COMMENT '备注',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态 1 启用  0 禁用',
  `user_type` tinyint(4) DEFAULT '2' COMMENT '用户类型  1 超级管理员  2 普通用户',
  `role_id` int(11) DEFAULT NULL COMMENT '角色id （一个用户只对应一个角色）',
  `wrong_password_count` int(11) DEFAULT '0' COMMENT '密码错误次数',
  `locked` tinyint(1) DEFAULT '0' COMMENT '账号是否被锁定  1：是  0：否',
  `lock_start_time` datetime DEFAULT NULL COMMENT '锁定开始时间',
  `unlock_time` datetime DEFAULT NULL COMMENT '解锁时间',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除 0 未删除 1已删除',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `password_record` varchar(255) DEFAULT NULL COMMENT '密码修改信息记录(默认保存最近5条更新数据)',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COMMENT='用户';

-- 构造表warn_illegal_park
CREATE TABLE IF NOT EXISTS `warn_illegal_park` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `plate_no` varchar(50) DEFAULT NULL COMMENT '车牌号',
  `bind_type` tinyint(4) DEFAULT NULL COMMENT '绑定类型  1：绑定车位  2：绑定区域',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除  0：未删除  1：已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(255) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(50) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车辆违停告警配置';

-- 构造表warn_illegal_park_relate
CREATE TABLE IF NOT EXISTS `warn_illegal_park_relate` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `warn_illegal_park_id` int(11) DEFAULT NULL COMMENT 'warn_illegal_park表的id',
  `park_area_id` int(11) DEFAULT NULL COMMENT '车位id或者区域id，具体要看绑定类型',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(50) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(50) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车辆违停告警配置关系表';

-- 构造表warn_log
CREATE TABLE IF NOT EXISTS `warn_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `park_id` int(11) DEFAULT NULL COMMENT '车位id',
  `park_no` varchar(50) DEFAULT NULL COMMENT '车位编号',
  `park_plate_no` varchar(50) DEFAULT NULL COMMENT '违停车牌',
  `bind_plate_no` varchar(50) DEFAULT NULL COMMENT '绑定车牌',
  `warn_type` tinyint(4) DEFAULT NULL COMMENT '告警类型  1：车位占用告警   2：车辆违停告警  3：特殊车辆入车  4：特殊车辆出车  5：车辆压线',
  `warn_source` tinyint(1) NOT NULL DEFAULT '0' COMMENT '告警来源 0-寻车系统 1-第三方',
  `bind_park_area` varchar(1024) DEFAULT NULL COMMENT '绑定的车位编号或者区域的名称  多个之间用英语分号隔开',
  `park_time` datetime DEFAULT NULL COMMENT '停入时间',
  `warn_time` datetime DEFAULT NULL COMMENT '告警时间',
  `warn_status` tinyint(4) DEFAULT NULL COMMENT '告警状态  1：告警中  2：手动停止  3：自动停止',
  `car_image_url` varchar(255) DEFAULT NULL COMMENT '车辆抓拍照片地址',
  `present_car_record_id` int(11) DEFAULT NULL COMMENT '在场车id b_present_car_record表的id 用来标识唯一入车事件',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(50) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(50) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_park_id` (`park_id`) USING BTREE,
  KEY `idx_present_car_record_id` (`present_car_record_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='告警记录';

-- 构造表warn_space_occupy
CREATE TABLE IF NOT EXISTS `warn_space_occupy` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `park_id` int(11) DEFAULT NULL COMMENT '车位id',
  `plate_no` varchar(1024) DEFAULT NULL COMMENT '绑定车牌号，多个车牌号中间用英文分号隔开',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除  0：未删除  1：已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(50) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(50) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='车位占用告警配置';

-- 构造表warn_special_car
CREATE TABLE IF NOT EXISTS `warn_special_car` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `plate_no` varchar(50) DEFAULT NULL COMMENT '车牌号',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `warn_type` tinyint(4) DEFAULT NULL COMMENT '告警类型  1：入车告警  2：出车告警  3：入车和出车都告警',
  `light_warn_witch` tinyint(1) DEFAULT '0' COMMENT '车位灯告警开关   1：开  0：关',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除  0：未删除  1：已删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(50) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(50) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='特殊车辆配置';

-- 构造表warn_time
CREATE TABLE IF NOT EXISTS `warn_time` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `warn_config_id` int(11) DEFAULT NULL COMMENT '关联的配置表的id （warn_occupy，warn_park，warn_spacial）表的id',
  `warn_config_type` tinyint(4) DEFAULT NULL COMMENT '关联类型  1：warn_occupy车位占用告警   2：warn_park车辆违停告警  3：warn_spacial特殊车告警',
  `day_of_week` int(11) DEFAULT NULL COMMENT '一周的第几天（星期几）',
  `start_time` varchar(50) DEFAULT NULL COMMENT '开始时间  HH:mm:ss',
  `end_time` varchar(50) DEFAULT NULL COMMENT '结束时间  HH:mm:ss',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(50) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(50) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='固定车绑定告警时间';


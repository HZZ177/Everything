SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- ============定义存储过程============

DROP PROCEDURE IF EXISTS add_element_unless_exists;
DELIMITER $$
-- 新增字段或索引，新增之前会判定是否存在
-- element_type：参数类型 column=字段 index=索引
-- tab_name：表名
-- element_name：字段名或索引名
-- sql_statement：执行的sql
CREATE PROCEDURE add_element_unless_exists(IN element_type VARCHAR(64), IN tab_name VARCHAR(64), IN element_name VARCHAR(64), IN sql_statement VARCHAR(500))
BEGIN
    -- 设置字符集为 utf8mb4
    SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
    SET CHARACTER SET utf8mb4;
    
    -- 新增字段
    IF element_type = 'column' THEN
        IF NOT EXISTS (
            -- 判定字段是否存在
            SELECT * FROM information_schema.columns
            WHERE table_schema = DATABASE() and table_name = tab_name AND column_name = element_name
        ) THEN
            SET @s = sql_statement;
            PREPARE stmt FROM @s;
            EXECUTE stmt;
        END IF;
    END IF;

    -- 新增索引
    IF element_type = 'index' THEN
        IF NOT EXISTS (
            -- 判定索引是否存在
            SELECT 1 FROM INFORMATION_SCHEMA.STATISTICS
            WHERE table_schema = DATABASE() and table_name= tab_name AND index_name= element_name
        ) THEN
            SET @s = sql_statement;
            PREPARE stmt FROM @s;
            EXECUTE stmt;
        END IF;
    END IF;

END; $$
DELIMITER ;


-- ===============全量创建标准库表===============
-- 构造表 api_access_info
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='api接入表';

-- 构造表 api_push_info
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=16384 ROW_FORMAT=DYNAMIC COMMENT='推送信息';

-- 构造表 api_supplementary_push
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='补推信息表';

-- 构造表 area_camera
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='区域相机';

-- 构造表 area_camera_relate
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='区域相机关联区域表';

-- 构造表 area_info
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='区域信息';

-- 构造表 b_car_in_out_record
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='历史进出车记录表';

-- 构造表 b_car_in_out_record_area
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='车辆进出车记录（区域相机）';

-- 构造表 b_present_car_plate_record
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='在场车车牌记录表';

-- 构造表 b_present_car_record
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='在场车辆表';

-- 构造表 b_present_car_record_area
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
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='在场车辆表（区域相机使用）';

-- 构造表 b_recognition_record
CREATE TABLE IF NOT EXISTS `b_recognition_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `park_addr` int(11) DEFAULT NULL COMMENT '车位地址',
  `plate_no` varchar(64) DEFAULT NULL COMMENT '车牌',
  `car_image_url` varchar(255) DEFAULT NULL COMMENT '车辆照片地址（相对路径）',
  `plate_no_reliability` int(11) DEFAULT NULL COMMENT '图片识别车牌可信度',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='识别记录表';

-- 构造表 berth_rate_info
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=174 ROW_FORMAT=DYNAMIC COMMENT='泊位使用率信息表';

-- 构造表 color_transparency_styles
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='颜色透明度配置表';

-- 构造表 coordinate
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='元素坐标表';

-- 构造表 device_escalation
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='设备信息上报表';

-- 构造表 element_beacon
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='蓝牙信标';

-- 构造表 element_column
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='柱子元素表';

-- 构造表 element_connector
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='通行设施';

-- 构造表 element_custom
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='自定义元素表';

-- 构造表 element_custom_detail
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='自定义元素详情表';

-- 构造表 element_ground
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='地面元素表';

-- 构造表 element_impassable_path
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='不可通行路线';

-- 构造表 element_machine
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='找车机';

-- 构造表 element_model
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='模型';

-- 构造表 element_park
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='车位';

-- 构造表 element_path
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='路网';

-- 构造表 element_screen
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='屏';

-- 构造表 element_screen_child
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='子屏表';

-- 构造表 element_screen_park_relation
CREATE TABLE IF NOT EXISTS `element_screen_park_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `screen_id` int(11) DEFAULT NULL COMMENT '子屏id  element_screen_child表的id',
  `park_id` int(11) DEFAULT NULL COMMENT '车位id  element_park表的id',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(255) DEFAULT NULL COMMENT '创建者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_screen_id` (`screen_id`) USING BTREE,
  KEY `idx_park_id` (`park_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='屏和车位的关系表';

-- 构造表 f_config
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=16384 ROW_FORMAT=DYNAMIC COMMENT='系统配置表';

-- 构造表 face_info
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='人脸信息表';

-- 构造表 floor_info
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='楼层信息';

-- 构造表 general_config
CREATE TABLE IF NOT EXISTS `general_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `config_key` varchar(255) DEFAULT NULL COMMENT '字段唯一标识，禁止重复',
  `description` varchar(255) DEFAULT NULL COMMENT '字段详细作用描述',
  `config_value` varchar(255) DEFAULT NULL COMMENT '字段具体配置信息',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=2730 ROW_FORMAT=COMPACT COMMENT='通用参数配置信息表';

-- 构造表 image_styles
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='图标配置表';

-- 构造表 info_across_floor
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='跨层寻车用指引设置表';

-- 构造表 info_machine_config
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=16384 ROW_FORMAT=DYNAMIC COMMENT='找车机常用参数表';

-- 构造表 ini_config
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=16384 ROW_FORMAT=DYNAMIC COMMENT='C++参数配置表';

-- 构造表 internationalization
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
) ENGINE=InnoDB AUTO_INCREMENT=29896 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT COMMENT='国际化';

-- 构造表 internationalization_relation
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=4096 ROW_FORMAT=DYNAMIC COMMENT='国际化字段与语言关系表';

-- 构造表 lcd_advertisement_config
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='LCD屏广告配置表';

-- 构造表 lcd_advertisement_scheme
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='LCD屏广告方案表';

-- 构造表 lcd_screen_config
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='LCD屏配置';

-- 构造表 light_scheme_plan
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='车位灯方案下发计划';

-- 构造表 light_scheme_plan_park_relation
CREATE TABLE IF NOT EXISTS `light_scheme_plan_park_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `plan_id` int(11) DEFAULT NULL COMMENT '车位灯方案下发计划id',
  `element_park_id` int(11) DEFAULT NULL COMMENT '车位id',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='车位灯方案下发计划与车位关系表';

-- 构造表 lot_info
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=16384 ROW_FORMAT=DYNAMIC COMMENT='车场信息';

-- 构造表 machine_advertisement_config
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='找车机广告配置';

-- 构造表 map_styles
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='地图样式配置表';

-- 构造表 node_device
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='节点设备';

-- 构造表 node_device_relate
CREATE TABLE IF NOT EXISTS `node_device_relate` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `area_device_id` int(11) DEFAULT NULL COMMENT '区域设备id  node_device表的id',
  `floor_id` int(11) DEFAULT NULL COMMENT '楼层id',
  `area_id` int(11) DEFAULT NULL COMMENT '区域id',
  `entrance_exit` tinyint(4) DEFAULT NULL COMMENT '相机放置类型  1：入口   2：出口   3：出入口',
  `entrance_exit_name` varchar(255) DEFAULT NULL COMMENT '枚举类型：  入口   出口  出入口',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='区域设备与区域的关系表';

-- 构造表 parking_light_area_relation
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='车位灯方案和区域的关系表';

-- 构造表 parking_light_scheme
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='车位灯方案';

-- 构造表 permissions
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
) ENGINE=InnoDB AUTO_INCREMENT=598 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='权限';

-- 构造表 role
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=5461 ROW_FORMAT=DYNAMIC COMMENT='角色';

-- 构造表 role_permission_relation
CREATE TABLE IF NOT EXISTS `role_permission_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` int(11) DEFAULT NULL COMMENT '角色id',
  `permission_id` int(11) DEFAULT NULL COMMENT '权限id',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(50) DEFAULT NULL COMMENT '创建者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=971 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=234 ROW_FORMAT=DYNAMIC COMMENT='角色权限关系表';

-- 构造表 schedule_config
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=16384 ROW_FORMAT=DYNAMIC COMMENT='参数配置表';

-- 构造表 t_access_config
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=16384 ROW_FORMAT=COMPACT COMMENT='C++重构配置信息表';

-- 构造表 t_car_in_out_statistics
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='出入车流量统计';

-- 构造表 t_login_log
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='登陆日志表';

-- 构造表 t_server_log
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
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=119 ROW_FORMAT=DYNAMIC COMMENT='服务日志表';

-- 构造表 user
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=4096 ROW_FORMAT=DYNAMIC COMMENT='用户';

-- 构造表 warn_illegal_park
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='车辆违停告警配置';

-- 构造表 warn_illegal_park_relate
CREATE TABLE IF NOT EXISTS `warn_illegal_park_relate` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `warn_illegal_park_id` int(11) DEFAULT NULL COMMENT 'warn_illegal_park表的id',
  `park_area_id` int(11) DEFAULT NULL COMMENT '车位id或者区域id，具体要看绑定类型',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(50) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(50) DEFAULT NULL COMMENT '更新者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='车辆违停告警配置关系表';

-- 构造表 warn_log
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='告警记录';

-- 构造表 warn_space_occupy
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='车位占用告警配置';

-- 构造表 warn_special_car
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='特殊车辆配置';

-- 构造表 warn_time
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='固定车绑定告警时间';

-- ===============全量更新所有表字段===============
-- 更新表 api_access_info 所有字段和索引
ALTER TABLE api_access_info CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE api_access_info COMMENT = 'api接入表';
CALL add_element_unless_exists('column', 'api_access_info', 'id', 'ALTER TABLE api_access_info ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'api_access_info', 'app_code', 'ALTER TABLE api_access_info ADD COLUMN `app_code` varchar(64) DEFAULT "" COMMENT "租户编码" AFTER id;');
CALL add_element_unless_exists('column', 'api_access_info', 'secret', 'ALTER TABLE api_access_info ADD COLUMN `secret` varchar(64) DEFAULT "" COMMENT "秘钥" AFTER app_code;');
CALL add_element_unless_exists('column', 'api_access_info', 'tenant_name', 'ALTER TABLE api_access_info ADD COLUMN `tenant_name` varchar(255) DEFAULT "" COMMENT "租户名称" AFTER secret;');
CALL add_element_unless_exists('column', 'api_access_info', 'tenant_tel', 'ALTER TABLE api_access_info ADD COLUMN `tenant_tel` int(11) DEFAULT NULL COMMENT "租户电话" AFTER tenant_name;');
CALL add_element_unless_exists('column', 'api_access_info', 'api_perm', 'ALTER TABLE api_access_info ADD COLUMN `api_perm` varchar(1024) DEFAULT "" COMMENT "接口权限（逗号隔开）" AFTER tenant_tel;');
CALL add_element_unless_exists('column', 'api_access_info', 'skip_auth', 'ALTER TABLE api_access_info ADD COLUMN `skip_auth` tinyint(1) DEFAULT "0" COMMENT "是否跳过鉴权 0-否，1-是" AFTER api_perm;');
CALL add_element_unless_exists('column', 'api_access_info', 'deleted', 'ALTER TABLE api_access_info ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除0未删除1已删除" AFTER skip_auth;');
CALL add_element_unless_exists('column', 'api_access_info', 'create_time', 'ALTER TABLE api_access_info ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'api_access_info', 'creator', 'ALTER TABLE api_access_info ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'api_access_info', 'update_time', 'ALTER TABLE api_access_info ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'api_access_info', 'updater', 'ALTER TABLE api_access_info ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'api_access_info', 'index_app_code', 'ALTER TABLE api_access_info ADD INDEX index_app_code (app_code) USING BTREE');

-- 更新表 api_push_info 所有字段和索引
ALTER TABLE api_push_info CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE api_push_info COMMENT = '推送信息';
CALL add_element_unless_exists('column', 'api_push_info', 'id', 'ALTER TABLE api_push_info ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'api_push_info', 'app_code', 'ALTER TABLE api_push_info ADD COLUMN `app_code` varchar(64) DEFAULT "" COMMENT "租户编码" AFTER id;');
CALL add_element_unless_exists('column', 'api_push_info', 'secret', 'ALTER TABLE api_push_info ADD COLUMN `secret` varchar(64) DEFAULT "" COMMENT "秘钥" AFTER app_code;');
CALL add_element_unless_exists('column', 'api_push_info', 'tenant_name', 'ALTER TABLE api_push_info ADD COLUMN `tenant_name` varchar(255) DEFAULT "" COMMENT "租户名称" AFTER secret;');
CALL add_element_unless_exists('column', 'api_push_info', 'func_module', 'ALTER TABLE api_push_info ADD COLUMN `func_module` varchar(64) DEFAULT "" COMMENT "功能模块" AFTER tenant_name;');
CALL add_element_unless_exists('column', 'api_push_info', 'push_url', 'ALTER TABLE api_push_info ADD COLUMN `push_url` varchar(255) DEFAULT "" COMMENT "推送路径" AFTER func_module;');
CALL add_element_unless_exists('column', 'api_push_info', 'impl_class', 'ALTER TABLE api_push_info ADD COLUMN `impl_class` varchar(64) DEFAULT "" COMMENT "实现类" AFTER push_url;');
CALL add_element_unless_exists('column', 'api_push_info', 'attribute', 'ALTER TABLE api_push_info ADD COLUMN `attribute` varchar(255) DEFAULT "" COMMENT "额外备用" AFTER impl_class;');
CALL add_element_unless_exists('column', 'api_push_info', 'push_switch', 'ALTER TABLE api_push_info ADD COLUMN `push_switch` tinyint(1) DEFAULT "1" COMMENT "推送开关 0-关，1-开" AFTER attribute;');
CALL add_element_unless_exists('column', 'api_push_info', 'create_time', 'ALTER TABLE api_push_info ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER push_switch;');
CALL add_element_unless_exists('column', 'api_push_info', 'creator', 'ALTER TABLE api_push_info ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'api_push_info', 'update_time', 'ALTER TABLE api_push_info ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'api_push_info', 'updater', 'ALTER TABLE api_push_info ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'api_push_info', 'idx_func_module', 'ALTER TABLE api_push_info ADD INDEX idx_func_module (func_module) USING BTREE');
CALL add_element_unless_exists('index', 'api_push_info', 'index_app_code', 'ALTER TABLE api_push_info ADD INDEX index_app_code (app_code) USING BTREE');

-- 更新表 api_supplementary_push 所有字段和索引
ALTER TABLE api_supplementary_push CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE api_supplementary_push COMMENT = '补推信息表';
CALL add_element_unless_exists('column', 'api_supplementary_push', 'id', 'ALTER TABLE api_supplementary_push ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'api_supplementary_push', 'url', 'ALTER TABLE api_supplementary_push ADD COLUMN `url` varchar(255) DEFAULT NULL COMMENT "补推完整路径地址" AFTER id;');
CALL add_element_unless_exists('column', 'api_supplementary_push', 'header', 'ALTER TABLE api_supplementary_push ADD COLUMN `header` varchar(255) DEFAULT NULL COMMENT "请求头相关信息" AFTER url;');
CALL add_element_unless_exists('column', 'api_supplementary_push', 'params', 'ALTER TABLE api_supplementary_push ADD COLUMN `params` varchar(255) DEFAULT NULL COMMENT "参数相关信息" AFTER header;');
CALL add_element_unless_exists('column', 'api_supplementary_push', 'reason', 'ALTER TABLE api_supplementary_push ADD COLUMN `reason` varchar(255) DEFAULT NULL COMMENT "推送失败原因或异常信息" AFTER params;');
CALL add_element_unless_exists('column', 'api_supplementary_push', 'status', 'ALTER TABLE api_supplementary_push ADD COLUMN `status` tinyint(1) DEFAULT "0" COMMENT "补推状态 0：未推送 1：已推送" AFTER reason;');
CALL add_element_unless_exists('column', 'api_supplementary_push', 'req_id', 'ALTER TABLE api_supplementary_push ADD COLUMN `req_id` varchar(32) DEFAULT NULL COMMENT "事件ID，用于查询对应绑定事件关系" AFTER status;');
CALL add_element_unless_exists('column', 'api_supplementary_push', 'create_time', 'ALTER TABLE api_supplementary_push ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER req_id;');

-- 更新表 area_camera 所有字段和索引
ALTER TABLE area_camera CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE area_camera COMMENT = '区域相机';
CALL add_element_unless_exists('column', 'area_camera', 'id', 'ALTER TABLE area_camera ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'area_camera', 'camera_ip', 'ALTER TABLE area_camera ADD COLUMN `camera_ip` varchar(255) DEFAULT NULL COMMENT "相机ip" AFTER id;');
CALL add_element_unless_exists('column', 'area_camera', 'remark', 'ALTER TABLE area_camera ADD COLUMN `remark` varchar(255) DEFAULT NULL COMMENT "备注" AFTER camera_ip;');
CALL add_element_unless_exists('column', 'area_camera', 'camera_direction', 'ALTER TABLE area_camera ADD COLUMN `camera_direction` int(11) DEFAULT NULL COMMENT "相机方向" AFTER remark;');
CALL add_element_unless_exists('column', 'area_camera', 'create_time', 'ALTER TABLE area_camera ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER camera_direction;');
CALL add_element_unless_exists('column', 'area_camera', 'creater', 'ALTER TABLE area_camera ADD COLUMN `creater` varchar(255) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'area_camera', 'update_time', 'ALTER TABLE area_camera ADD COLUMN `update_time` datetime DEFAULT NULL COMMENT "更新时间" AFTER creater;');
CALL add_element_unless_exists('column', 'area_camera', 'updater', 'ALTER TABLE area_camera ADD COLUMN `updater` datetime DEFAULT NULL COMMENT "更新者" AFTER update_time;');

-- 更新表 area_camera_relate 所有字段和索引
ALTER TABLE area_camera_relate CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE area_camera_relate COMMENT = '区域相机关联区域表';
CALL add_element_unless_exists('column', 'area_camera_relate', 'id', 'ALTER TABLE area_camera_relate ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'area_camera_relate', 'area_camera_id', 'ALTER TABLE area_camera_relate ADD COLUMN `area_camera_id` int(11) DEFAULT NULL COMMENT "区域相机id" AFTER id;');
CALL add_element_unless_exists('column', 'area_camera_relate', 'floor_id', 'ALTER TABLE area_camera_relate ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER area_camera_id;');
CALL add_element_unless_exists('column', 'area_camera_relate', 'area_id', 'ALTER TABLE area_camera_relate ADD COLUMN `area_id` int(11) DEFAULT NULL COMMENT "区域id" AFTER floor_id;');
CALL add_element_unless_exists('column', 'area_camera_relate', 'come_bind', 'ALTER TABLE area_camera_relate ADD COLUMN `come_bind` tinyint(4) DEFAULT "1" COMMENT "来车绑定   1=入车   2=出车" AFTER area_id;');
CALL add_element_unless_exists('column', 'area_camera_relate', 'go_bind', 'ALTER TABLE area_camera_relate ADD COLUMN `go_bind` tinyint(4) DEFAULT "2" COMMENT "去车绑定   1=入车   2=出车" AFTER come_bind;');
CALL add_element_unless_exists('column', 'area_camera_relate', 'create_time', 'ALTER TABLE area_camera_relate ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER go_bind;');
CALL add_element_unless_exists('column', 'area_camera_relate', 'creater', 'ALTER TABLE area_camera_relate ADD COLUMN `creater` varchar(50) DEFAULT NULL COMMENT "创建者" AFTER create_time;');

-- 更新表 area_info 所有字段和索引
ALTER TABLE area_info CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE area_info COMMENT = '区域信息';
CALL add_element_unless_exists('column', 'area_info', 'id', 'ALTER TABLE area_info ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'area_info', 'name', 'ALTER TABLE area_info ADD COLUMN `name` varchar(255) DEFAULT NULL COMMENT "区域名称" AFTER id;');
CALL add_element_unless_exists('column', 'area_info', 'lot_id', 'ALTER TABLE area_info ADD COLUMN `lot_id` int(11) NOT NULL COMMENT "车场id" AFTER name;');
CALL add_element_unless_exists('column', 'area_info', 'floor_id', 'ALTER TABLE area_info ADD COLUMN `floor_id` int(11) NOT NULL COMMENT "楼层id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'area_info', 'type', 'ALTER TABLE area_info ADD COLUMN `type` int(11) DEFAULT "0" COMMENT "0:普通区域 1:立体车库区域" AFTER floor_id;');
CALL add_element_unless_exists('column', 'area_info', 'x', 'ALTER TABLE area_info ADD COLUMN `x` varchar(255) DEFAULT NULL COMMENT "区域x坐标" AFTER type;');
CALL add_element_unless_exists('column', 'area_info', 'y', 'ALTER TABLE area_info ADD COLUMN `y` varchar(255) DEFAULT NULL COMMENT "区域y坐标" AFTER x;');
CALL add_element_unless_exists('column', 'area_info', 'deleted', 'ALTER TABLE area_info ADD COLUMN `deleted` tinyint(1) NOT NULL DEFAULT "0" COMMENT "是否删除（0：未删除，1：已删除）" AFTER y;');
CALL add_element_unless_exists('column', 'area_info', 'creator', 'ALTER TABLE area_info ADD COLUMN `creator` varchar(255) DEFAULT NULL COMMENT "创建人" AFTER deleted;');
CALL add_element_unless_exists('column', 'area_info', 'create_time', 'ALTER TABLE area_info ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'area_info', 'updater', 'ALTER TABLE area_info ADD COLUMN `updater` varchar(255) DEFAULT NULL COMMENT "更新人" AFTER create_time;');
CALL add_element_unless_exists('column', 'area_info', 'update_time', 'ALTER TABLE area_info ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');
CALL add_element_unless_exists('column', 'area_info', 'park_space_camera_ip', 'ALTER TABLE area_info ADD COLUMN `park_space_camera_ip` varchar(64) DEFAULT NULL COMMENT "立体车位相机IP" AFTER update_time;');
CALL add_element_unless_exists('column', 'area_info', 'park_space_camera_unique_id', 'ALTER TABLE area_info ADD COLUMN `park_space_camera_unique_id` varchar(64) DEFAULT NULL COMMENT "立体车位相机唯一标识" AFTER park_space_camera_ip;');
CALL add_element_unless_exists('column', 'area_info', 'detector_park_addr_list', 'ALTER TABLE area_info ADD COLUMN `detector_park_addr_list` varchar(1024) DEFAULT NULL COMMENT "立体车位关联探测器车位唯一标识，以英文,分隔开" AFTER park_space_camera_unique_id;');

-- 更新表 b_car_in_out_record 所有字段和索引
ALTER TABLE b_car_in_out_record CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE b_car_in_out_record COMMENT = '历史进出车记录表';
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'id', 'ALTER TABLE b_car_in_out_record ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'lot_id', 'ALTER TABLE b_car_in_out_record ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id lot_info id" AFTER id;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'area_id', 'ALTER TABLE b_car_in_out_record ADD COLUMN `area_id` int(11) DEFAULT NULL COMMENT "区域id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'area_name', 'ALTER TABLE b_car_in_out_record ADD COLUMN `area_name` varchar(255) DEFAULT "" COMMENT "区域名称" AFTER area_id;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'floor_id', 'ALTER TABLE b_car_in_out_record ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER area_name;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'floor_name', 'ALTER TABLE b_car_in_out_record ADD COLUMN `floor_name` varchar(255) DEFAULT "" COMMENT "楼层名称" AFTER floor_id;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'element_park_id', 'ALTER TABLE b_car_in_out_record ADD COLUMN `element_park_id` int(11) DEFAULT NULL COMMENT "车位id" AFTER floor_name;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'park_addr', 'ALTER TABLE b_car_in_out_record ADD COLUMN `park_addr` int(11) DEFAULT NULL COMMENT "车位地址" AFTER element_park_id;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'park_status', 'ALTER TABLE b_car_in_out_record ADD COLUMN `park_status` int(11) DEFAULT NULL COMMENT "车位状态 0-空闲 1-占用 2-故障 3-停止服务" AFTER park_addr;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'park_control', 'ALTER TABLE b_car_in_out_record ADD COLUMN `park_control` int(11) DEFAULT NULL COMMENT "车位控制 0-自动控制 1-手动控制" AFTER park_status;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'park_no', 'ALTER TABLE b_car_in_out_record ADD COLUMN `park_no` varchar(255) DEFAULT "" COMMENT "车位名称" AFTER park_control;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'plate_no', 'ALTER TABLE b_car_in_out_record ADD COLUMN `plate_no` varchar(64) DEFAULT "" COMMENT "车牌号" AFTER park_no;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'plate_no_simple', 'ALTER TABLE b_car_in_out_record ADD COLUMN `plate_no_simple` varchar(64) DEFAULT NULL COMMENT "纯数字字母车牌" AFTER plate_no;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'car_image_url', 'ALTER TABLE b_car_in_out_record ADD COLUMN `car_image_url` varchar(255) DEFAULT NULL COMMENT "车辆照片地址" AFTER plate_no_simple;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'plate_no_color', 'ALTER TABLE b_car_in_out_record ADD COLUMN `plate_no_color` varchar(10) DEFAULT NULL COMMENT "车牌底色" AFTER car_image_url;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'plate_no_record', 'ALTER TABLE b_car_in_out_record ADD COLUMN `plate_no_record` varchar(1024) DEFAULT NULL COMMENT "历史车牌识别记录，多个车牌之间用英文逗号隔开" AFTER plate_no_color;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'in_time', 'ALTER TABLE b_car_in_out_record ADD COLUMN `in_time` datetime DEFAULT NULL COMMENT "入车时间" AFTER plate_no_record;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'out_time', 'ALTER TABLE b_car_in_out_record ADD COLUMN `out_time` datetime DEFAULT NULL COMMENT "出车时间" AFTER in_time;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'in_type', 'ALTER TABLE b_car_in_out_record ADD COLUMN `in_type` tinyint(4) DEFAULT NULL COMMENT "操作类型 0-自动入车 1-手动入车" AFTER out_time;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'out_type', 'ALTER TABLE b_car_in_out_record ADD COLUMN `out_type` tinyint(4) DEFAULT NULL COMMENT "操作类型 0-自动出车 1-手动出车" AFTER in_type;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'unique_id', 'ALTER TABLE b_car_in_out_record ADD COLUMN `unique_id` varchar(32) DEFAULT NULL COMMENT "每次进出车事件唯一UUID绑定" AFTER out_type;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'create_time', 'ALTER TABLE b_car_in_out_record ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER unique_id;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'creator', 'ALTER TABLE b_car_in_out_record ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'update_time', 'ALTER TABLE b_car_in_out_record ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'b_car_in_out_record', 'updater', 'ALTER TABLE b_car_in_out_record ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'b_car_in_out_record', 'idx_create_time', 'ALTER TABLE b_car_in_out_record ADD INDEX idx_create_time (create_time) USING BTREE');
CALL add_element_unless_exists('index', 'b_car_in_out_record', 'idx_out_time', 'ALTER TABLE b_car_in_out_record ADD INDEX idx_out_time (out_time) USING BTREE');
CALL add_element_unless_exists('index', 'b_car_in_out_record', 'index_element_park_id', 'ALTER TABLE b_car_in_out_record ADD INDEX index_element_park_id (element_park_id) USING BTREE');
CALL add_element_unless_exists('index', 'b_car_in_out_record', 'index_park_no', 'ALTER TABLE b_car_in_out_record ADD INDEX index_park_no (park_no) USING BTREE');
CALL add_element_unless_exists('index', 'b_car_in_out_record', 'index_plate_no', 'ALTER TABLE b_car_in_out_record ADD INDEX index_plate_no (plate_no) USING BTREE');

-- 更新表 b_car_in_out_record_area 所有字段和索引
ALTER TABLE b_car_in_out_record_area CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE b_car_in_out_record_area COMMENT = '车辆进出车记录（区域相机）';
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'id', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'area_camera_id', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `area_camera_id` int(11) DEFAULT NULL COMMENT "区域相机id" AFTER id;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'area_camera_ip', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `area_camera_ip` varchar(255) DEFAULT NULL COMMENT "区域相机ip" AFTER area_camera_id;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'event_id', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `event_id` varchar(255) DEFAULT NULL COMMENT "事件id" AFTER area_camera_ip;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'floor_id', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER event_id;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'floor_name', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `floor_name` varchar(100) DEFAULT NULL COMMENT "楼层名称" AFTER floor_id;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'area_id', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `area_id` int(11) DEFAULT NULL COMMENT "区域id" AFTER floor_name;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'area_name', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `area_name` varchar(100) DEFAULT NULL COMMENT "区域名称" AFTER area_id;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'plate_no', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `plate_no` varchar(100) DEFAULT NULL COMMENT "车牌号" AFTER area_name;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'plate_no_simple', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `plate_no_simple` varchar(64) DEFAULT NULL COMMENT "纯数字字母车牌" AFTER plate_no;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'plate_no_color', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `plate_no_color` varchar(10) DEFAULT NULL COMMENT "车牌底色" AFTER plate_no_simple;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'car_image_url', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `car_image_url` varchar(255) DEFAULT NULL COMMENT "车辆抓拍照片路径" AFTER plate_no_color;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'type', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `type` tinyint(4) DEFAULT NULL COMMENT "事件类型  1：进车   2：出车" AFTER car_image_url;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'in_out_time', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `in_out_time` datetime DEFAULT NULL COMMENT "入车时间或者出车时间" AFTER type;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'create_time', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER in_out_time;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'creator', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `creator` varchar(100) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'update_time', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'b_car_in_out_record_area', 'updater', 'ALTER TABLE b_car_in_out_record_area ADD COLUMN `updater` varchar(100) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'b_car_in_out_record_area', 'idx_create_time', 'ALTER TABLE b_car_in_out_record_area ADD INDEX idx_create_time (create_time) USING BTREE');

-- 更新表 b_present_car_plate_record 所有字段和索引
ALTER TABLE b_present_car_plate_record CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE b_present_car_plate_record COMMENT = '在场车车牌记录表';
CALL add_element_unless_exists('column', 'b_present_car_plate_record', 'id', 'ALTER TABLE b_present_car_plate_record ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'b_present_car_plate_record', 'present_car_record_id', 'ALTER TABLE b_present_car_plate_record ADD COLUMN `present_car_record_id` int(11) DEFAULT NULL COMMENT "在场车记录id" AFTER id;');
CALL add_element_unless_exists('column', 'b_present_car_plate_record', 'plate_no', 'ALTER TABLE b_present_car_plate_record ADD COLUMN `plate_no` varchar(64) DEFAULT "" COMMENT "车牌号" AFTER present_car_record_id;');
CALL add_element_unless_exists('column', 'b_present_car_plate_record', 'plate_no_simple', 'ALTER TABLE b_present_car_plate_record ADD COLUMN `plate_no_simple` varchar(64) DEFAULT NULL COMMENT "纯数字字母车牌" AFTER plate_no;');
CALL add_element_unless_exists('column', 'b_present_car_plate_record', 'car_image_url', 'ALTER TABLE b_present_car_plate_record ADD COLUMN `car_image_url` varchar(255) DEFAULT NULL COMMENT "车牌图片路径" AFTER plate_no_simple;');
CALL add_element_unless_exists('column', 'b_present_car_plate_record', 'create_time', 'ALTER TABLE b_present_car_plate_record ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER car_image_url;');
CALL add_element_unless_exists('column', 'b_present_car_plate_record', 'creator', 'ALTER TABLE b_present_car_plate_record ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'b_present_car_plate_record', 'update_time', 'ALTER TABLE b_present_car_plate_record ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'b_present_car_plate_record', 'updater', 'ALTER TABLE b_present_car_plate_record ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('column', 'b_present_car_plate_record', 'plate_no_reliability', 'ALTER TABLE b_present_car_plate_record ADD COLUMN `plate_no_reliability` int(11) DEFAULT "0" COMMENT "图片识别车牌可信度" AFTER updater;');
CALL add_element_unless_exists('column', 'b_present_car_plate_record', 'recognition_number', 'ALTER TABLE b_present_car_plate_record ADD COLUMN `recognition_number` int(11) DEFAULT "1" COMMENT "图片识别车牌次数" AFTER plate_no_reliability;');
CALL add_element_unless_exists('column', 'b_present_car_plate_record', 'charge_status', 'ALTER TABLE b_present_car_plate_record ADD COLUMN `charge_status` tinyint(1) DEFAULT "0" COMMENT "收费系统比对状态，0：未比对  1：已比对" AFTER recognition_number;');

-- 更新表 b_present_car_record 所有字段和索引
ALTER TABLE b_present_car_record CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE b_present_car_record COMMENT = '在场车辆表';
CALL add_element_unless_exists('column', 'b_present_car_record', 'id', 'ALTER TABLE b_present_car_record ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'b_present_car_record', 'lot_id', 'ALTER TABLE b_present_car_record ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id lot_info id" AFTER id;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'area_id', 'ALTER TABLE b_present_car_record ADD COLUMN `area_id` int(11) DEFAULT NULL COMMENT "区域id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'floor_id', 'ALTER TABLE b_present_car_record ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER area_id;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'element_park_id', 'ALTER TABLE b_present_car_record ADD COLUMN `element_park_id` int(11) DEFAULT NULL COMMENT "车位id" AFTER floor_id;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'plate_no', 'ALTER TABLE b_present_car_record ADD COLUMN `plate_no` varchar(64) DEFAULT "" COMMENT "车牌号，格式：川A8F43P" AFTER element_park_id;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'plate_no_simple', 'ALTER TABLE b_present_car_record ADD COLUMN `plate_no_simple` varchar(64) DEFAULT NULL COMMENT "纯数字字母车牌" AFTER plate_no;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'plate_no_color', 'ALTER TABLE b_present_car_record ADD COLUMN `plate_no_color` varchar(10) DEFAULT NULL COMMENT "车牌底色" AFTER plate_no_simple;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'car_image_url', 'ALTER TABLE b_present_car_record ADD COLUMN `car_image_url` varchar(255) DEFAULT NULL COMMENT "车辆照片地址（相对路径）" AFTER plate_no_color;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'in_time', 'ALTER TABLE b_present_car_record ADD COLUMN `in_time` datetime DEFAULT NULL COMMENT "入车时间" AFTER car_image_url;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'in_type', 'ALTER TABLE b_present_car_record ADD COLUMN `in_type` tinyint(4) DEFAULT NULL COMMENT "操作类型 0-自动入车 1-手动入车" AFTER in_time;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'unique_id', 'ALTER TABLE b_present_car_record ADD COLUMN `unique_id` varchar(32) DEFAULT NULL COMMENT "每次进出车事件唯一UUID绑定" AFTER in_type;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'create_time', 'ALTER TABLE b_present_car_record ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER unique_id;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'creator', 'ALTER TABLE b_present_car_record ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'update_time', 'ALTER TABLE b_present_car_record ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'b_present_car_record', 'updater', 'ALTER TABLE b_present_car_record ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'b_present_car_record', 'index_element_park_id', 'ALTER TABLE b_present_car_record ADD INDEX index_element_park_id (element_park_id) USING BTREE');
CALL add_element_unless_exists('index', 'b_present_car_record', 'index_plate_no', 'ALTER TABLE b_present_car_record ADD INDEX index_plate_no (plate_no) USING BTREE');

-- 更新表 b_present_car_record_area 所有字段和索引
ALTER TABLE b_present_car_record_area CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE b_present_car_record_area COMMENT = '在场车辆表（区域相机使用）';
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'id', 'ALTER TABLE b_present_car_record_area ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'area_camera_id', 'ALTER TABLE b_present_car_record_area ADD COLUMN `area_camera_id` int(11) DEFAULT NULL COMMENT "区域相机id" AFTER id;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'area_camera_ip', 'ALTER TABLE b_present_car_record_area ADD COLUMN `area_camera_ip` varchar(255) DEFAULT NULL COMMENT "区域相机ip" AFTER area_camera_id;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'floor_id', 'ALTER TABLE b_present_car_record_area ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER area_camera_ip;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'event_id', 'ALTER TABLE b_present_car_record_area ADD COLUMN `event_id` varchar(36) DEFAULT NULL COMMENT "事件id" AFTER floor_id;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'area_id', 'ALTER TABLE b_present_car_record_area ADD COLUMN `area_id` int(11) DEFAULT NULL COMMENT "区域id" AFTER event_id;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'plate_no', 'ALTER TABLE b_present_car_record_area ADD COLUMN `plate_no` varchar(100) DEFAULT NULL COMMENT "车牌号" AFTER area_id;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'plate_no_simple', 'ALTER TABLE b_present_car_record_area ADD COLUMN `plate_no_simple` varchar(64) DEFAULT NULL COMMENT "纯数字字母车牌" AFTER plate_no;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'plate_no_color', 'ALTER TABLE b_present_car_record_area ADD COLUMN `plate_no_color` varchar(10) DEFAULT NULL COMMENT "车牌底色" AFTER plate_no_simple;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'car_image_url', 'ALTER TABLE b_present_car_record_area ADD COLUMN `car_image_url` varchar(255) DEFAULT NULL COMMENT "车辆抓拍照片路径" AFTER plate_no_color;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'in_time', 'ALTER TABLE b_present_car_record_area ADD COLUMN `in_time` datetime DEFAULT NULL COMMENT "入车时间" AFTER car_image_url;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'create_time', 'ALTER TABLE b_present_car_record_area ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER in_time;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'creator', 'ALTER TABLE b_present_car_record_area ADD COLUMN `creator` varchar(100) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'update_time', 'ALTER TABLE b_present_car_record_area ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'updater', 'ALTER TABLE b_present_car_record_area ADD COLUMN `updater` varchar(100) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('column', 'b_present_car_record_area', 'data_source', 'ALTER TABLE b_present_car_record_area ADD COLUMN `data_source` tinyint(1) DEFAULT "0" COMMENT "数据来源 0：区域相机 1：立体车位" AFTER updater;');

-- 更新表 b_recognition_record 所有字段和索引
ALTER TABLE b_recognition_record CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE b_recognition_record COMMENT = '识别记录表';
CALL add_element_unless_exists('column', 'b_recognition_record', 'id', 'ALTER TABLE b_recognition_record ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'b_recognition_record', 'park_addr', 'ALTER TABLE b_recognition_record ADD COLUMN `park_addr` int(11) DEFAULT NULL COMMENT "车位地址" AFTER id;');
CALL add_element_unless_exists('column', 'b_recognition_record', 'plate_no', 'ALTER TABLE b_recognition_record ADD COLUMN `plate_no` varchar(64) DEFAULT NULL COMMENT "车牌" AFTER park_addr;');
CALL add_element_unless_exists('column', 'b_recognition_record', 'car_image_url', 'ALTER TABLE b_recognition_record ADD COLUMN `car_image_url` varchar(255) DEFAULT NULL COMMENT "车辆照片地址（相对路径）" AFTER plate_no;');
CALL add_element_unless_exists('column', 'b_recognition_record', 'plate_no_reliability', 'ALTER TABLE b_recognition_record ADD COLUMN `plate_no_reliability` int(11) DEFAULT NULL COMMENT "图片识别车牌可信度" AFTER car_image_url;');
CALL add_element_unless_exists('column', 'b_recognition_record', 'create_time', 'ALTER TABLE b_recognition_record ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER plate_no_reliability;');

-- 更新表 berth_rate_info 所有字段和索引
ALTER TABLE berth_rate_info CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE berth_rate_info COMMENT = '泊位使用率信息表';
CALL add_element_unless_exists('column', 'berth_rate_info', 'id', 'ALTER TABLE berth_rate_info ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'berth_rate_info', 'time', 'ALTER TABLE berth_rate_info ADD COLUMN `time` datetime NOT NULL COMMENT "时间" AFTER id;');
CALL add_element_unless_exists('column', 'berth_rate_info', 'all_park_number', 'ALTER TABLE berth_rate_info ADD COLUMN `all_park_number` int(11) DEFAULT NULL COMMENT "当前车场全部车位数" AFTER time;');
CALL add_element_unless_exists('column', 'berth_rate_info', 'all_berth_data', 'ALTER TABLE berth_rate_info ADD COLUMN `all_berth_data` varchar(10) DEFAULT NULL COMMENT "当前全车场泊位占用数据" AFTER all_park_number;');
CALL add_element_unless_exists('column', 'berth_rate_info', 'berth_type', 'ALTER TABLE berth_rate_info ADD COLUMN `berth_type` tinyint(1) NOT NULL COMMENT "泊位类型，0：根据楼层区分，1：根据车位类型区分" AFTER all_berth_data;');
CALL add_element_unless_exists('column', 'berth_rate_info', 'berth_info', 'ALTER TABLE berth_rate_info ADD COLUMN `berth_info` varchar(256) DEFAULT NULL COMMENT "泊位占用信息,如B1:100,B2:100这样的数据" AFTER berth_type;');
CALL add_element_unless_exists('column', 'berth_rate_info', 'create_time', 'ALTER TABLE berth_rate_info ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER berth_info;');
CALL add_element_unless_exists('column', 'berth_rate_info', 'update_time', 'ALTER TABLE berth_rate_info ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER create_time;');

-- 更新表 color_transparency_styles 所有字段和索引
ALTER TABLE color_transparency_styles CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE color_transparency_styles COMMENT = '颜色透明度配置表';
CALL add_element_unless_exists('column', 'color_transparency_styles', 'id', 'ALTER TABLE color_transparency_styles ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'map_styles_id', 'ALTER TABLE color_transparency_styles ADD COLUMN `map_styles_id` int(11) NOT NULL COMMENT "地图样式id" AFTER id;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'occupy_flash', 'ALTER TABLE color_transparency_styles ADD COLUMN `occupy_flash` int(11) DEFAULT NULL COMMENT "占用时车位闪烁 0 不闪烁 1 闪烁" AFTER map_styles_id;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'free_flash', 'ALTER TABLE color_transparency_styles ADD COLUMN `free_flash` int(11) DEFAULT NULL COMMENT "空闲时车位闪烁开关  0 不闪烁 1 闪烁" AFTER occupy_flash;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'select_color', 'ALTER TABLE color_transparency_styles ADD COLUMN `select_color` varchar(32) DEFAULT NULL COMMENT "选中时颜色" AFTER free_flash;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'fill_color', 'ALTER TABLE color_transparency_styles ADD COLUMN `fill_color` varchar(32) DEFAULT NULL COMMENT "填充颜色" AFTER select_color;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'border_color', 'ALTER TABLE color_transparency_styles ADD COLUMN `border_color` varchar(32) DEFAULT NULL COMMENT "边框颜色" AFTER fill_color;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'transparency', 'ALTER TABLE color_transparency_styles ADD COLUMN `transparency` int(11) DEFAULT NULL COMMENT "透明度" AFTER border_color;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'type', 'ALTER TABLE color_transparency_styles ADD COLUMN `type` tinyint(4) DEFAULT NULL COMMENT "-1:柱子,-2:地面,-3:背景,1:普通车位,2:新能源车位,3:时租车,4:幼稚园班车,5:自定义元素,6:区域,7:立体车位" AFTER transparency;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'area_id', 'ALTER TABLE color_transparency_styles ADD COLUMN `area_id` int(11) DEFAULT NULL COMMENT "区域id" AFTER type;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'element_custom_id', 'ALTER TABLE color_transparency_styles ADD COLUMN `element_custom_id` int(11) DEFAULT NULL COMMENT "当type=5时，存放自定义元素id" AFTER area_id;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'is_show_name', 'ALTER TABLE color_transparency_styles ADD COLUMN `is_show_name` tinyint(1) DEFAULT "0" COMMENT "是否显示元素名称；0：不显示，1：显示" AFTER element_custom_id;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'deleted', 'ALTER TABLE color_transparency_styles ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除（0：未删除，1：已删除）" AFTER is_show_name;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'creator', 'ALTER TABLE color_transparency_styles ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER deleted;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'create_time', 'ALTER TABLE color_transparency_styles ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'updater', 'ALTER TABLE color_transparency_styles ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER create_time;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'update_time', 'ALTER TABLE color_transparency_styles ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');
CALL add_element_unless_exists('column', 'color_transparency_styles', 'occupy_fill_color', 'ALTER TABLE color_transparency_styles ADD COLUMN `occupy_fill_color` varchar(32) DEFAULT NULL COMMENT "车位占用时填充颜色" AFTER update_time;');
CALL add_element_unless_exists('index', 'color_transparency_styles', 'index_map_styles_id', 'ALTER TABLE color_transparency_styles ADD INDEX index_map_styles_id (map_styles_id) USING BTREE');

-- 更新表 coordinate 所有字段和索引
ALTER TABLE coordinate CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE coordinate COMMENT = '元素坐标表';
CALL add_element_unless_exists('column', 'coordinate', 'id', 'ALTER TABLE coordinate ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "自增，主键";');
CALL add_element_unless_exists('column', 'coordinate', 'lot_id', 'ALTER TABLE coordinate ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id" AFTER id;');
CALL add_element_unless_exists('column', 'coordinate', 'element_id', 'ALTER TABLE coordinate ADD COLUMN `element_id` int(11) DEFAULT NULL COMMENT "元素id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'coordinate', 'type', 'ALTER TABLE coordinate ADD COLUMN `type` tinyint(4) DEFAULT NULL COMMENT "元素类型详情见枚举1 地面  2 柱子  3 车位  4蓝牙信标  5路网 6找车机 7通行设施  8自定义元素  9不可通行路网  10子屏 11屏" AFTER element_id;');
CALL add_element_unless_exists('column', 'coordinate', 'attribute', 'ALTER TABLE coordinate ADD COLUMN `attribute` varchar(50) DEFAULT "" COMMENT "冗余字段 （当字段type=5,则begin表示起点，end表示终点）" AFTER type;');
CALL add_element_unless_exists('column', 'coordinate', 'x_point', 'ALTER TABLE coordinate ADD COLUMN `x_point` varchar(50) DEFAULT NULL COMMENT "x坐标" AFTER attribute;');
CALL add_element_unless_exists('column', 'coordinate', 'y_point', 'ALTER TABLE coordinate ADD COLUMN `y_point` varchar(50) DEFAULT NULL COMMENT "y坐标" AFTER x_point;');
CALL add_element_unless_exists('column', 'coordinate', 'deleted', 'ALTER TABLE coordinate ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除0未删除1已删除" AFTER y_point;');
CALL add_element_unless_exists('column', 'coordinate', 'creator', 'ALTER TABLE coordinate ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER deleted;');
CALL add_element_unless_exists('column', 'coordinate', 'create_time', 'ALTER TABLE coordinate ADD COLUMN `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('index', 'coordinate', 'idx_element_id', 'ALTER TABLE coordinate ADD INDEX idx_element_id (element_id) USING BTREE');

-- 更新表 device_escalation 所有字段和索引
ALTER TABLE device_escalation CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE device_escalation COMMENT = '设备信息上报表';
CALL add_element_unless_exists('column', 'device_escalation', 'id', 'ALTER TABLE device_escalation ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'device_escalation', 'device_ip', 'ALTER TABLE device_escalation ADD COLUMN `device_ip` varchar(255) DEFAULT NULL COMMENT "上报设备IP" AFTER id;');
CALL add_element_unless_exists('column', 'device_escalation', 'device_port', 'ALTER TABLE device_escalation ADD COLUMN `device_port` int(11) DEFAULT NULL COMMENT "上报设备端口" AFTER device_ip;');
CALL add_element_unless_exists('column', 'device_escalation', 'floor_name', 'ALTER TABLE device_escalation ADD COLUMN `floor_name` varchar(255) DEFAULT NULL COMMENT "楼层名称" AFTER device_port;');
CALL add_element_unless_exists('column', 'device_escalation', 'area_name', 'ALTER TABLE device_escalation ADD COLUMN `area_name` varchar(255) DEFAULT NULL COMMENT "区域名称" AFTER floor_name;');
CALL add_element_unless_exists('column', 'device_escalation', 'park_no', 'ALTER TABLE device_escalation ADD COLUMN `park_no` varchar(255) DEFAULT NULL COMMENT "车位编号" AFTER area_name;');
CALL add_element_unless_exists('column', 'device_escalation', 'create_time', 'ALTER TABLE device_escalation ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER park_no;');
CALL add_element_unless_exists('column', 'device_escalation', 'update_time', 'ALTER TABLE device_escalation ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER create_time;');
CALL add_element_unless_exists('column', 'device_escalation', 'exception', 'ALTER TABLE device_escalation ADD COLUMN `exception` tinyint(1) DEFAULT "0" COMMENT "异常问题(0：正常， 1：车位编号重复， 2：无车位编号)" AFTER update_time;');

-- 更新表 element_beacon 所有字段和索引
ALTER TABLE element_beacon CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_beacon COMMENT = '蓝牙信标';
CALL add_element_unless_exists('column', 'element_beacon', 'id', 'ALTER TABLE element_beacon ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'element_beacon', 'lot_id', 'ALTER TABLE element_beacon ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id lot_info id" AFTER id;');
CALL add_element_unless_exists('column', 'element_beacon', 'floor_id', 'ALTER TABLE element_beacon ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'element_beacon', 'name', 'ALTER TABLE element_beacon ADD COLUMN `name` varchar(255) DEFAULT NULL COMMENT "名称" AFTER floor_id;');
CALL add_element_unless_exists('column', 'element_beacon', 'uuid', 'ALTER TABLE element_beacon ADD COLUMN `uuid` varchar(50) DEFAULT NULL COMMENT "蓝牙信标的uuid" AFTER name;');
CALL add_element_unless_exists('column', 'element_beacon', 'minor', 'ALTER TABLE element_beacon ADD COLUMN `minor` varchar(30) DEFAULT NULL COMMENT "蓝牙信标的minor" AFTER uuid;');
CALL add_element_unless_exists('column', 'element_beacon', 'major', 'ALTER TABLE element_beacon ADD COLUMN `major` varchar(30) DEFAULT NULL COMMENT "蓝牙信标的major" AFTER minor;');
CALL add_element_unless_exists('column', 'element_beacon', 'deleted', 'ALTER TABLE element_beacon ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除0未删除1已删除" AFTER major;');
CALL add_element_unless_exists('column', 'element_beacon', 'creator', 'ALTER TABLE element_beacon ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER deleted;');
CALL add_element_unless_exists('column', 'element_beacon', 'create_time', 'ALTER TABLE element_beacon ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_beacon', 'updater', 'ALTER TABLE element_beacon ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_beacon', 'update_time', 'ALTER TABLE element_beacon ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');

-- 更新表 element_column 所有字段和索引
ALTER TABLE element_column CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_column COMMENT = '柱子元素表';
CALL add_element_unless_exists('column', 'element_column', 'id', 'ALTER TABLE element_column ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'element_column', 'lot_id', 'ALTER TABLE element_column ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id" AFTER id;');
CALL add_element_unless_exists('column', 'element_column', 'floor_id', 'ALTER TABLE element_column ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'element_column', 'name', 'ALTER TABLE element_column ADD COLUMN `name` varchar(255) DEFAULT NULL COMMENT "名称" AFTER floor_id;');
CALL add_element_unless_exists('column', 'element_column', 'height', 'ALTER TABLE element_column ADD COLUMN `height` double DEFAULT NULL COMMENT "高度 柱子高度2米" AFTER name;');
CALL add_element_unless_exists('column', 'element_column', 'deleted', 'ALTER TABLE element_column ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除0未删除1已删除" AFTER height;');
CALL add_element_unless_exists('column', 'element_column', 'creator', 'ALTER TABLE element_column ADD COLUMN `creator` varchar(255) DEFAULT NULL COMMENT "创建人" AFTER deleted;');
CALL add_element_unless_exists('column', 'element_column', 'create_time', 'ALTER TABLE element_column ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_column', 'updater', 'ALTER TABLE element_column ADD COLUMN `updater` varchar(255) DEFAULT NULL COMMENT "更新人" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_column', 'update_time', 'ALTER TABLE element_column ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');

-- 更新表 element_connector 所有字段和索引
ALTER TABLE element_connector CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_connector COMMENT = '通行设施';
CALL add_element_unless_exists('column', 'element_connector', 'id', 'ALTER TABLE element_connector ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'element_connector', 'lot_id', 'ALTER TABLE element_connector ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id lot_info id" AFTER id;');
CALL add_element_unless_exists('column', 'element_connector', 'floor_id', 'ALTER TABLE element_connector ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'element_connector', 'name', 'ALTER TABLE element_connector ADD COLUMN `name` varchar(255) DEFAULT NULL COMMENT "名称" AFTER floor_id;');
CALL add_element_unless_exists('column', 'element_connector', 'species', 'ALTER TABLE element_connector ADD COLUMN `species` tinyint(4) DEFAULT NULL COMMENT "种类 1：直梯 2：护梯 3：楼梯 4：出入口" AFTER name;');
CALL add_element_unless_exists('column', 'element_connector', 'associated_connector_ids', 'ALTER TABLE element_connector ADD COLUMN `associated_connector_ids` varchar(255) DEFAULT NULL COMMENT "关联设施ids" AFTER species;');
CALL add_element_unless_exists('column', 'element_connector', 'deleted', 'ALTER TABLE element_connector ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除0未删除1已删除" AFTER associated_connector_ids;');
CALL add_element_unless_exists('column', 'element_connector', 'create_time', 'ALTER TABLE element_connector ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'element_connector', 'creator', 'ALTER TABLE element_connector ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_connector', 'update_time', 'ALTER TABLE element_connector ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_connector', 'updater', 'ALTER TABLE element_connector ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'element_connector', 'index_map_floor_id', 'ALTER TABLE element_connector ADD INDEX index_map_floor_id (floor_id) USING BTREE');

-- 更新表 element_custom 所有字段和索引
ALTER TABLE element_custom CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_custom COMMENT = '自定义元素表';
CALL add_element_unless_exists('column', 'element_custom', 'id', 'ALTER TABLE element_custom ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'element_custom', 'lot_id', 'ALTER TABLE element_custom ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id" AFTER id;');
CALL add_element_unless_exists('column', 'element_custom', 'name', 'ALTER TABLE element_custom ADD COLUMN `name` varchar(255) DEFAULT "" COMMENT "名称" AFTER lot_id;');
CALL add_element_unless_exists('column', 'element_custom', 'height', 'ALTER TABLE element_custom ADD COLUMN `height` double DEFAULT "0.1" COMMENT "高度 默认0.1m" AFTER name;');
CALL add_element_unless_exists('column', 'element_custom', 'suspend_height', 'ALTER TABLE element_custom ADD COLUMN `suspend_height` double DEFAULT "0" COMMENT "离地高度 默认0m" AFTER height;');
CALL add_element_unless_exists('column', 'element_custom', 'deleted', 'ALTER TABLE element_custom ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除 0未删除 1已删除" AFTER suspend_height;');
CALL add_element_unless_exists('column', 'element_custom', 'creator', 'ALTER TABLE element_custom ADD COLUMN `creator` varchar(255) DEFAULT "" COMMENT "创建人" AFTER deleted;');
CALL add_element_unless_exists('column', 'element_custom', 'create_time', 'ALTER TABLE element_custom ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_custom', 'updater', 'ALTER TABLE element_custom ADD COLUMN `updater` varchar(255) DEFAULT "" COMMENT "更新人" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_custom', 'update_time', 'ALTER TABLE element_custom ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');
CALL add_element_unless_exists('index', 'element_custom', 'idx_lot_id', 'ALTER TABLE element_custom ADD INDEX idx_lot_id (lot_id) USING BTREE');

-- 更新表 element_custom_detail 所有字段和索引
ALTER TABLE element_custom_detail CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_custom_detail COMMENT = '自定义元素详情表';
CALL add_element_unless_exists('column', 'element_custom_detail', 'id', 'ALTER TABLE element_custom_detail ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'element_custom_detail', 'element_custom_id', 'ALTER TABLE element_custom_detail ADD COLUMN `element_custom_id` int(11) DEFAULT NULL COMMENT "自定义元素id" AFTER id;');
CALL add_element_unless_exists('column', 'element_custom_detail', 'lot_id', 'ALTER TABLE element_custom_detail ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id" AFTER element_custom_id;');
CALL add_element_unless_exists('column', 'element_custom_detail', 'floor_id', 'ALTER TABLE element_custom_detail ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'element_custom_detail', 'name', 'ALTER TABLE element_custom_detail ADD COLUMN `name` varchar(255) DEFAULT "" COMMENT "名称" AFTER floor_id;');
CALL add_element_unless_exists('column', 'element_custom_detail', 'deleted', 'ALTER TABLE element_custom_detail ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除 0未删除 1已删除" AFTER name;');
CALL add_element_unless_exists('column', 'element_custom_detail', 'creator', 'ALTER TABLE element_custom_detail ADD COLUMN `creator` varchar(255) DEFAULT "" COMMENT "创建人" AFTER deleted;');
CALL add_element_unless_exists('column', 'element_custom_detail', 'create_time', 'ALTER TABLE element_custom_detail ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_custom_detail', 'updater', 'ALTER TABLE element_custom_detail ADD COLUMN `updater` varchar(255) DEFAULT "" COMMENT "更新人" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_custom_detail', 'update_time', 'ALTER TABLE element_custom_detail ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');
CALL add_element_unless_exists('index', 'element_custom_detail', 'idx_element_custom_id', 'ALTER TABLE element_custom_detail ADD INDEX idx_element_custom_id (element_custom_id) USING BTREE');
CALL add_element_unless_exists('index', 'element_custom_detail', 'idx_floor_id', 'ALTER TABLE element_custom_detail ADD INDEX idx_floor_id (floor_id) USING BTREE');
CALL add_element_unless_exists('index', 'element_custom_detail', 'idx_lot_id', 'ALTER TABLE element_custom_detail ADD INDEX idx_lot_id (lot_id) USING BTREE');

-- 更新表 element_ground 所有字段和索引
ALTER TABLE element_ground CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_ground COMMENT = '地面元素表';
CALL add_element_unless_exists('column', 'element_ground', 'id', 'ALTER TABLE element_ground ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'element_ground', 'lot_id', 'ALTER TABLE element_ground ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id" AFTER id;');
CALL add_element_unless_exists('column', 'element_ground', 'floor_id', 'ALTER TABLE element_ground ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'element_ground', 'name', 'ALTER TABLE element_ground ADD COLUMN `name` varchar(255) DEFAULT NULL COMMENT "名称" AFTER floor_id;');
CALL add_element_unless_exists('column', 'element_ground', 'height', 'ALTER TABLE element_ground ADD COLUMN `height` double DEFAULT NULL COMMENT "高度 地面默认0.1米" AFTER name;');
CALL add_element_unless_exists('column', 'element_ground', 'deleted', 'ALTER TABLE element_ground ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除0未删除1已删除" AFTER height;');
CALL add_element_unless_exists('column', 'element_ground', 'creator', 'ALTER TABLE element_ground ADD COLUMN `creator` varchar(255) DEFAULT NULL COMMENT "创建人" AFTER deleted;');
CALL add_element_unless_exists('column', 'element_ground', 'create_time', 'ALTER TABLE element_ground ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_ground', 'updater', 'ALTER TABLE element_ground ADD COLUMN `updater` varchar(255) DEFAULT NULL COMMENT "更新人" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_ground', 'update_time', 'ALTER TABLE element_ground ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');
CALL add_element_unless_exists('index', 'element_ground', 'index_map_floor_id', 'ALTER TABLE element_ground ADD INDEX index_map_floor_id (floor_id) USING BTREE');

-- 更新表 element_impassable_path 所有字段和索引
ALTER TABLE element_impassable_path CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_impassable_path COMMENT = '不可通行路线';
CALL add_element_unless_exists('column', 'element_impassable_path', 'id', 'ALTER TABLE element_impassable_path ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'element_impassable_path', 'lot_id', 'ALTER TABLE element_impassable_path ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id lot_info id" AFTER id;');
CALL add_element_unless_exists('column', 'element_impassable_path', 'floor_id', 'ALTER TABLE element_impassable_path ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'element_impassable_path', 'deleted', 'ALTER TABLE element_impassable_path ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除，0未删除，1已删除" AFTER floor_id;');
CALL add_element_unless_exists('column', 'element_impassable_path', 'create_time', 'ALTER TABLE element_impassable_path ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'element_impassable_path', 'creator', 'ALTER TABLE element_impassable_path ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_impassable_path', 'update_time', 'ALTER TABLE element_impassable_path ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_impassable_path', 'updater', 'ALTER TABLE element_impassable_path ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'element_impassable_path', 'idx_floor_id', 'ALTER TABLE element_impassable_path ADD INDEX idx_floor_id (floor_id) USING BTREE');
CALL add_element_unless_exists('index', 'element_impassable_path', 'idx_lot_id', 'ALTER TABLE element_impassable_path ADD INDEX idx_lot_id (lot_id) USING BTREE');

-- 更新表 element_machine 所有字段和索引
ALTER TABLE element_machine CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_machine COMMENT = '找车机';
CALL add_element_unless_exists('column', 'element_machine', 'id', 'ALTER TABLE element_machine ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'element_machine', 'lot_id', 'ALTER TABLE element_machine ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id lot_info id" AFTER id;');
CALL add_element_unless_exists('column', 'element_machine', 'floor_id', 'ALTER TABLE element_machine ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'element_machine', 'name', 'ALTER TABLE element_machine ADD COLUMN `name` varchar(255) DEFAULT NULL COMMENT "名称" AFTER floor_id;');
CALL add_element_unless_exists('column', 'element_machine', 'species', 'ALTER TABLE element_machine ADD COLUMN `species` tinyint(4) DEFAULT NULL COMMENT "种类 1：立式找车机 2：壁式找车机" AFTER name;');
CALL add_element_unless_exists('column', 'element_machine', 'ip', 'ALTER TABLE element_machine ADD COLUMN `ip` varchar(32) DEFAULT NULL COMMENT "找车机ip" AFTER species;');
CALL add_element_unless_exists('column', 'element_machine', 'direction_num', 'ALTER TABLE element_machine ADD COLUMN `direction_num` int(11) DEFAULT "0" COMMENT "朝向(度数)" AFTER ip;');
CALL add_element_unless_exists('column', 'element_machine', 'unique_identification_field', 'ALTER TABLE element_machine ADD COLUMN `unique_identification_field` varchar(50) DEFAULT NULL COMMENT "唯一标识" AFTER direction_num;');
CALL add_element_unless_exists('column', 'element_machine', 'deleted', 'ALTER TABLE element_machine ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除0未删除1已删除" AFTER unique_identification_field;');
CALL add_element_unless_exists('column', 'element_machine', 'create_time', 'ALTER TABLE element_machine ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'element_machine', 'creator', 'ALTER TABLE element_machine ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_machine', 'update_time', 'ALTER TABLE element_machine ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_machine', 'updater', 'ALTER TABLE element_machine ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'element_machine', 'index_ip', 'ALTER TABLE element_machine ADD INDEX index_ip (ip) USING BTREE');

-- 更新表 element_model 所有字段和索引
ALTER TABLE element_model CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_model COMMENT = '模型';
CALL add_element_unless_exists('column', 'element_model', 'id', 'ALTER TABLE element_model ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT";');
CALL add_element_unless_exists('column', 'element_model', 'lot_id', 'ALTER TABLE element_model ADD COLUMN `lot_id` int(11) NOT NULL COMMENT "车场id" AFTER id;');
CALL add_element_unless_exists('column', 'element_model', 'floor_id', 'ALTER TABLE element_model ADD COLUMN `floor_id` int(11) NOT NULL COMMENT "楼层id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'element_model', 'element_type', 'ALTER TABLE element_model ADD COLUMN `element_type` int(11) DEFAULT NULL COMMENT "模型类型" AFTER floor_id;');
CALL add_element_unless_exists('column', 'element_model', 'element_name', 'ALTER TABLE element_model ADD COLUMN `element_name` varchar(255) DEFAULT NULL COMMENT "模型名称" AFTER element_type;');
CALL add_element_unless_exists('column', 'element_model', 'rotation_angle', 'ALTER TABLE element_model ADD COLUMN `rotation_angle` double DEFAULT "0" COMMENT "模型的朝向设置（0~360），实时预览，默认为0" AFTER element_name;');
CALL add_element_unless_exists('column', 'element_model', 'x_point', 'ALTER TABLE element_model ADD COLUMN `x_point` int(11) DEFAULT NULL COMMENT "X坐标" AFTER rotation_angle;');
CALL add_element_unless_exists('column', 'element_model', 'y_point', 'ALTER TABLE element_model ADD COLUMN `y_point` int(11) DEFAULT NULL COMMENT "y坐标" AFTER x_point;');
CALL add_element_unless_exists('column', 'element_model', 'scale', 'ALTER TABLE element_model ADD COLUMN `scale` double DEFAULT "1" COMMENT "缩放比例，模型的大小控制（0.5-2），实时预览，默认为1" AFTER y_point;');
CALL add_element_unless_exists('column', 'element_model', 'suspend_height', 'ALTER TABLE element_model ADD COLUMN `suspend_height` double DEFAULT "0" COMMENT "离地高度，模型底面离地面上表面的距离（0-10.0），默认为0" AFTER scale;');
CALL add_element_unless_exists('column', 'element_model', 'creator', 'ALTER TABLE element_model ADD COLUMN `creator` varchar(255) DEFAULT "" COMMENT "创建人" AFTER suspend_height;');
CALL add_element_unless_exists('column', 'element_model', 'create_time', 'ALTER TABLE element_model ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_model', 'updater', 'ALTER TABLE element_model ADD COLUMN `updater` varchar(255) DEFAULT "" COMMENT "更新人" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_model', 'update_time', 'ALTER TABLE element_model ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');
CALL add_element_unless_exists('index', 'element_model', 'idx_floor_id', 'ALTER TABLE element_model ADD INDEX idx_floor_id (floor_id) USING BTREE');
CALL add_element_unless_exists('index', 'element_model', 'idx_lot_id', 'ALTER TABLE element_model ADD INDEX idx_lot_id (lot_id) USING BTREE');

-- 更新表 element_park 所有字段和索引
ALTER TABLE element_park CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_park COMMENT = '车位';
CALL add_element_unless_exists('column', 'element_park', 'id', 'ALTER TABLE element_park ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'element_park', 'lot_id', 'ALTER TABLE element_park ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id lot_info id" AFTER id;');
CALL add_element_unless_exists('column', 'element_park', 'floor_id', 'ALTER TABLE element_park ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'element_park', 'name', 'ALTER TABLE element_park ADD COLUMN `name` varchar(255) DEFAULT NULL COMMENT "名称" AFTER floor_id;');
CALL add_element_unless_exists('column', 'element_park', 'height', 'ALTER TABLE element_park ADD COLUMN `height` double DEFAULT NULL COMMENT "高度 地面默认0.1米 车位默认高度0.1米 柱子默认2米" AFTER name;');
CALL add_element_unless_exists('column', 'element_park', 'park_category', 'ALTER TABLE element_park ADD COLUMN `park_category` tinyint(4) DEFAULT NULL COMMENT "车位种类1 为普通车位 2 为新能源车位 3 为立体车位 4共享车位" AFTER height;');
CALL add_element_unless_exists('column', 'element_park', 'stereoscopic_park_camera_addr', 'ALTER TABLE element_park ADD COLUMN `stereoscopic_park_camera_addr` int(11) DEFAULT NULL COMMENT "立体车位对应的相机地址" AFTER park_category;');
CALL add_element_unless_exists('column', 'element_park', 'park_no', 'ALTER TABLE element_park ADD COLUMN `park_no` varchar(50) DEFAULT NULL COMMENT "车位号编号" AFTER stereoscopic_park_camera_addr;');
CALL add_element_unless_exists('column', 'element_park', 'park_addr', 'ALTER TABLE element_park ADD COLUMN `park_addr` int(11) DEFAULT NULL COMMENT "车位地址" AFTER park_no;');
CALL add_element_unless_exists('column', 'element_park', 'x_center', 'ALTER TABLE element_park ADD COLUMN `x_center` varchar(100) DEFAULT NULL COMMENT "车位中心点坐标X" AFTER park_addr;');
CALL add_element_unless_exists('column', 'element_park', 'y_center', 'ALTER TABLE element_park ADD COLUMN `y_center` varchar(100) DEFAULT NULL COMMENT "车位中心点坐标y" AFTER x_center;');
CALL add_element_unless_exists('column', 'element_park', 'control', 'ALTER TABLE element_park ADD COLUMN `control` tinyint(4) DEFAULT "0" COMMENT "车位控制 0-自动控制 1-手动控制" AFTER y_center;');
CALL add_element_unless_exists('column', 'element_park', 'status', 'ALTER TABLE element_park ADD COLUMN `status` tinyint(1) DEFAULT "0" COMMENT "车位状态 0-空闲 1-占用 2-故障 3-停止服务" AFTER control;');
CALL add_element_unless_exists('column', 'element_park', 'area_id', 'ALTER TABLE element_park ADD COLUMN `area_id` int(11) DEFAULT NULL COMMENT "area_info区域id" AFTER status;');
CALL add_element_unless_exists('column', 'element_park', 'toward', 'ALTER TABLE element_park ADD COLUMN `toward` int(11) DEFAULT "0" COMMENT "方向朝向（0-360角度整数存值）" AFTER area_id;');
CALL add_element_unless_exists('column', 'element_park', 'warning', 'ALTER TABLE element_park ADD COLUMN `warning` tinyint(1) DEFAULT "0" COMMENT "告警状态  1：告警中  0：未告警" AFTER toward;');
CALL add_element_unless_exists('column', 'element_park', 'last_leave_time', 'ALTER TABLE element_park ADD COLUMN `last_leave_time` timestamp NULL DEFAULT NULL COMMENT "车位最近一次出车时间" AFTER warning;');
CALL add_element_unless_exists('column', 'element_park', 'cpp_report_count', 'ALTER TABLE element_park ADD COLUMN `cpp_report_count` int(11) DEFAULT "0" COMMENT "C++程序给这个车位连续上报异常状态的次数" AFTER last_leave_time;');
CALL add_element_unless_exists('column', 'element_park', 'unique_identification_field', 'ALTER TABLE element_park ADD COLUMN `unique_identification_field` varchar(32) DEFAULT NULL COMMENT "车位唯一标识字段" AFTER cpp_report_count;');
CALL add_element_unless_exists('column', 'element_park', 'change_push_flag', 'ALTER TABLE element_park ADD COLUMN `change_push_flag` tinyint(1) DEFAULT "0" COMMENT "车位状态变化推送标识（单车场接口使用）  0-无变化，无需推送  1-有变化，需推送" AFTER unique_identification_field;');
CALL add_element_unless_exists('column', 'element_park', 'change_push_time', 'ALTER TABLE element_park ADD COLUMN `change_push_time` datetime DEFAULT NULL COMMENT "车位状态变化时间（单车场接口使用）" AFTER change_push_flag;');
CALL add_element_unless_exists('column', 'element_park', 'deleted', 'ALTER TABLE element_park ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除0未删除1已删除" AFTER change_push_time;');
CALL add_element_unless_exists('column', 'element_park', 'creator', 'ALTER TABLE element_park ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER deleted;');
CALL add_element_unless_exists('column', 'element_park', 'create_time', 'ALTER TABLE element_park ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_park', 'updater', 'ALTER TABLE element_park ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_park', 'update_time', 'ALTER TABLE element_park ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');
CALL add_element_unless_exists('column', 'element_park', 'parking_capture', 'ALTER TABLE element_park ADD COLUMN `parking_capture` varchar(255) DEFAULT NULL COMMENT "车位相机抓拍照片路径" AFTER update_time;');
CALL add_element_unless_exists('index', 'element_park', 'idx_park_addr', 'ALTER TABLE element_park ADD INDEX idx_park_addr (park_addr) USING BTREE');
CALL add_element_unless_exists('index', 'element_park', 'index_area_id', 'ALTER TABLE element_park ADD INDEX index_area_id (area_id) USING BTREE');
CALL add_element_unless_exists('index', 'element_park', 'index_park_no', 'ALTER TABLE element_park ADD INDEX index_park_no (park_no) USING BTREE');

-- 更新表 element_path 所有字段和索引
ALTER TABLE element_path CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_path COMMENT = '路网';
CALL add_element_unless_exists('column', 'element_path', 'id', 'ALTER TABLE element_path ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'element_path', 'lot_id', 'ALTER TABLE element_path ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id lot_info id" AFTER id;');
CALL add_element_unless_exists('column', 'element_path', 'floor_id', 'ALTER TABLE element_path ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'element_path', 'entry', 'ALTER TABLE element_path ADD COLUMN `entry` tinyint(4) DEFAULT "0" COMMENT "方向，预留字段，0 双向通行，1 正向通行，2反向通行" AFTER floor_id;');
CALL add_element_unless_exists('column', 'element_path', 'distance', 'ALTER TABLE element_path ADD COLUMN `distance` varchar(255) DEFAULT NULL COMMENT "路线长度" AFTER entry;');
CALL add_element_unless_exists('column', 'element_path', 'road_type', 'ALTER TABLE element_path ADD COLUMN `road_type` tinyint(1) DEFAULT "3" COMMENT "1  人行  2   车行  3  人/车行" AFTER distance;');
CALL add_element_unless_exists('column', 'element_path', 'tag', 'ALTER TABLE element_path ADD COLUMN `tag` int(11) DEFAULT "0" COMMENT "权限标签" AFTER road_type;');
CALL add_element_unless_exists('column', 'element_path', 'weight', 'ALTER TABLE element_path ADD COLUMN `weight` int(11) DEFAULT NULL COMMENT "权重" AFTER tag;');
CALL add_element_unless_exists('column', 'element_path', 'roadnet_floor', 'ALTER TABLE element_path ADD COLUMN `roadnet_floor` int(11) DEFAULT "0" COMMENT "1，就是表示通行设施连接其他楼层通行设施路网" AFTER weight;');
CALL add_element_unless_exists('column', 'element_path', 'deleted', 'ALTER TABLE element_path ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除，0未删除，1已删除" AFTER roadnet_floor;');
CALL add_element_unless_exists('column', 'element_path', 'create_time', 'ALTER TABLE element_path ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'element_path', 'creator', 'ALTER TABLE element_path ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_path', 'update_time', 'ALTER TABLE element_path ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_path', 'updater', 'ALTER TABLE element_path ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'element_path', 'index_floor_id', 'ALTER TABLE element_path ADD INDEX index_floor_id (floor_id) USING BTREE');

-- 更新表 element_screen 所有字段和索引
ALTER TABLE element_screen CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_screen COMMENT = '屏';
CALL add_element_unless_exists('column', 'element_screen', 'id', 'ALTER TABLE element_screen ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'element_screen', 'lot_id', 'ALTER TABLE element_screen ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id lot_info id" AFTER id;');
CALL add_element_unless_exists('column', 'element_screen', 'floor_id', 'ALTER TABLE element_screen ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER lot_id;');
CALL add_element_unless_exists('column', 'element_screen', 'name', 'ALTER TABLE element_screen ADD COLUMN `name` varchar(255) DEFAULT NULL COMMENT "名称" AFTER floor_id;');
CALL add_element_unless_exists('column', 'element_screen', 'species', 'ALTER TABLE element_screen ADD COLUMN `species` tinyint(4) DEFAULT NULL COMMENT "种类 1：LED屏 2：LCD屏" AFTER name;');
CALL add_element_unless_exists('column', 'element_screen', 'screen_addr', 'ALTER TABLE element_screen ADD COLUMN `screen_addr` int(11) DEFAULT NULL COMMENT "屏地址" AFTER species;');
CALL add_element_unless_exists('column', 'element_screen', 'sub_screen_num', 'ALTER TABLE element_screen ADD COLUMN `sub_screen_num` tinyint(4) DEFAULT NULL COMMENT "子屏数 1：单向屏 2：双向屏 3：三向屏" AFTER screen_addr;');
CALL add_element_unless_exists('column', 'element_screen', 'screen_type', 'ALTER TABLE element_screen ADD COLUMN `screen_type` tinyint(4) DEFAULT NULL COMMENT "屏类型 1-单拼接屏 2-双拼接屏 3-三拼接屏" AFTER sub_screen_num;');
CALL add_element_unless_exists('column', 'element_screen', 'show_template', 'ALTER TABLE element_screen ADD COLUMN `show_template` tinyint(4) DEFAULT NULL COMMENT "展示模板" AFTER screen_type;');
CALL add_element_unless_exists('column', 'element_screen', 'remark', 'ALTER TABLE element_screen ADD COLUMN `remark` varchar(255) DEFAULT "" COMMENT "备注" AFTER show_template;');
CALL add_element_unless_exists('column', 'element_screen', 'deleted', 'ALTER TABLE element_screen ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除 0未删除 1已删除" AFTER remark;');
CALL add_element_unless_exists('column', 'element_screen', 'create_time', 'ALTER TABLE element_screen ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'element_screen', 'creator', 'ALTER TABLE element_screen ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_screen', 'update_time', 'ALTER TABLE element_screen ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_screen', 'updater', 'ALTER TABLE element_screen ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('column', 'element_screen', 'direction', 'ALTER TABLE element_screen ADD COLUMN `direction` int(11) DEFAULT "1" COMMENT "屏方向（屏顺序配置字段，用来控制屏从左到右地址是递增(1)还是递减(-1)）" AFTER updater;');
CALL add_element_unless_exists('index', 'element_screen', 'index_screen_addr', 'ALTER TABLE element_screen ADD INDEX index_screen_addr (screen_addr) USING BTREE');

-- 更新表 element_screen_child 所有字段和索引
ALTER TABLE element_screen_child CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_screen_child COMMENT = '子屏表';
CALL add_element_unless_exists('column', 'element_screen_child', 'id', 'ALTER TABLE element_screen_child ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'element_screen_child', 'parent_id', 'ALTER TABLE element_screen_child ADD COLUMN `parent_id` int(11) DEFAULT NULL COMMENT "主屏id" AFTER id;');
CALL add_element_unless_exists('column', 'element_screen_child', 'floor_id', 'ALTER TABLE element_screen_child ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id  冗余字段  屏配置好后不能更改楼层，所以冗余这个字段" AFTER parent_id;');
CALL add_element_unless_exists('column', 'element_screen_child', 'screen_addr', 'ALTER TABLE element_screen_child ADD COLUMN `screen_addr` int(11) DEFAULT NULL COMMENT "屏地址" AFTER floor_id;');
CALL add_element_unless_exists('column', 'element_screen_child', 'description', 'ALTER TABLE element_screen_child ADD COLUMN `description` varchar(255) DEFAULT NULL COMMENT "描述" AFTER screen_addr;');
CALL add_element_unless_exists('column', 'element_screen_child', 'screen_species', 'ALTER TABLE element_screen_child ADD COLUMN `screen_species` tinyint(4) DEFAULT NULL COMMENT "屏种类 1：LED屏 2：LCD屏" AFTER description;');
CALL add_element_unless_exists('column', 'element_screen_child', 'screen_category', 'ALTER TABLE element_screen_child ADD COLUMN `screen_category` tinyint(4) DEFAULT "1" COMMENT "屏类别   1：LED网络屏、  2：485总屏、3：485子屏" AFTER screen_species;');
CALL add_element_unless_exists('column', 'element_screen_child', 'screen_type', 'ALTER TABLE element_screen_child ADD COLUMN `screen_type` tinyint(4) DEFAULT "1" COMMENT "屏类型   1：普通屏、2：总屏" AFTER screen_category;');
CALL add_element_unless_exists('column', 'element_screen_child', 'show_type', 'ALTER TABLE element_screen_child ADD COLUMN `show_type` tinyint(4) DEFAULT "1" COMMENT "展示内容   1：关联车位空车位数、2：关联车位占用车位数、3：车场总空车位数、4：车位总占用车位数、5：固定显示数值" AFTER screen_type;');
CALL add_element_unless_exists('column', 'element_screen_child', 'area_id', 'ALTER TABLE element_screen_child ADD COLUMN `area_id` int(11) DEFAULT NULL COMMENT "区域id" AFTER show_type;');
CALL add_element_unless_exists('column', 'element_screen_child', 'revise_num', 'ALTER TABLE element_screen_child ADD COLUMN `revise_num` int(11) DEFAULT "0" COMMENT "校正数值 （结果数值加上这个值）" AFTER area_id;');
CALL add_element_unless_exists('column', 'element_screen_child', 'critical_num', 'ALTER TABLE element_screen_child ADD COLUMN `critical_num` int(11) DEFAULT "0" COMMENT "临界值（小于临界值直接输出0）" AFTER revise_num;');
CALL add_element_unless_exists('column', 'element_screen_child', 'constant_num', 'ALTER TABLE element_screen_child ADD COLUMN `constant_num` int(11) DEFAULT "0" COMMENT "固定显示数值" AFTER critical_num;');
CALL add_element_unless_exists('column', 'element_screen_child', 'arrow_position', 'ALTER TABLE element_screen_child ADD COLUMN `arrow_position` tinyint(4) DEFAULT "0" COMMENT "箭头位置   0：右   1：左" AFTER constant_num;');
CALL add_element_unless_exists('column', 'element_screen_child', 'arrow_direction', 'ALTER TABLE element_screen_child ADD COLUMN `arrow_direction` tinyint(4) DEFAULT "0" COMMENT "箭头方向   0：右   1：左   2：上   3：下   17：左上   18：左下   19：右上   20：右下" AFTER arrow_position;');
CALL add_element_unless_exists('column', 'element_screen_child', 'show_color', 'ALTER TABLE element_screen_child ADD COLUMN `show_color` tinyint(4) DEFAULT "0" COMMENT "显示颜色   0：红   1：橙   2：绿   3：根据数值" AFTER arrow_direction;');
CALL add_element_unless_exists('column', 'element_screen_child', 'park_type', 'ALTER TABLE element_screen_child ADD COLUMN `park_type` tinyint(4) DEFAULT "0" COMMENT "车位类型   0：正常、1：残障" AFTER show_color;');
CALL add_element_unless_exists('column', 'element_screen_child', 'show_num', 'ALTER TABLE element_screen_child ADD COLUMN `show_num` int(11) DEFAULT NULL COMMENT "显示数字（对应的屏应该展示的数字，定时任务以及进出车和车屏关系变动会更新这个字段）" AFTER park_type;');
CALL add_element_unless_exists('column', 'element_screen_child', 'deleted', 'ALTER TABLE element_screen_child ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "删除状态   0：未删除   1：已删除" AFTER show_num;');
CALL add_element_unless_exists('column', 'element_screen_child', 'create_time', 'ALTER TABLE element_screen_child ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'element_screen_child', 'creator', 'ALTER TABLE element_screen_child ADD COLUMN `creator` varchar(50) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'element_screen_child', 'update_time', 'ALTER TABLE element_screen_child ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'element_screen_child', 'updater', 'ALTER TABLE element_screen_child ADD COLUMN `updater` varchar(50) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'element_screen_child', 'index_parent_id', 'ALTER TABLE element_screen_child ADD INDEX index_parent_id (parent_id) USING BTREE');
CALL add_element_unless_exists('index', 'element_screen_child', 'index_screen_addr', 'ALTER TABLE element_screen_child ADD INDEX index_screen_addr (screen_addr) USING BTREE');

-- 更新表 element_screen_park_relation 所有字段和索引
ALTER TABLE element_screen_park_relation CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE element_screen_park_relation COMMENT = '屏和车位的关系表';
CALL add_element_unless_exists('column', 'element_screen_park_relation', 'id', 'ALTER TABLE element_screen_park_relation ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'element_screen_park_relation', 'screen_id', 'ALTER TABLE element_screen_park_relation ADD COLUMN `screen_id` int(11) DEFAULT NULL COMMENT "子屏id  element_screen_child表的id" AFTER id;');
CALL add_element_unless_exists('column', 'element_screen_park_relation', 'park_id', 'ALTER TABLE element_screen_park_relation ADD COLUMN `park_id` int(11) DEFAULT NULL COMMENT "车位id  element_park表的id" AFTER screen_id;');
CALL add_element_unless_exists('column', 'element_screen_park_relation', 'create_time', 'ALTER TABLE element_screen_park_relation ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER park_id;');
CALL add_element_unless_exists('column', 'element_screen_park_relation', 'creator', 'ALTER TABLE element_screen_park_relation ADD COLUMN `creator` varchar(255) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('index', 'element_screen_park_relation', 'idx_screen_id', 'ALTER TABLE element_screen_park_relation ADD INDEX idx_screen_id (screen_id) USING BTREE');
CALL add_element_unless_exists('index', 'element_screen_park_relation', 'idx_park_id', 'ALTER TABLE element_screen_park_relation ADD INDEX idx_park_id (park_id) USING BTREE');

-- 更新表 f_config 所有字段和索引
ALTER TABLE f_config CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE f_config COMMENT = '系统配置表';
CALL add_element_unless_exists('column', 'f_config', 'id', 'ALTER TABLE f_config ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'f_config', 'config_code', 'ALTER TABLE f_config ADD COLUMN `config_code` varchar(64) DEFAULT "" COMMENT "配置编码" AFTER id;');
CALL add_element_unless_exists('column', 'f_config', 'config_value', 'ALTER TABLE f_config ADD COLUMN `config_value` varchar(64) DEFAULT "" COMMENT "配置值" AFTER config_code;');
CALL add_element_unless_exists('column', 'f_config', 'config_desc', 'ALTER TABLE f_config ADD COLUMN `config_desc` varchar(255) DEFAULT "" COMMENT "配置描述" AFTER config_value;');
CALL add_element_unless_exists('column', 'f_config', 'attribute', 'ALTER TABLE f_config ADD COLUMN `attribute` varchar(64) DEFAULT "" COMMENT "额外字段" AFTER config_desc;');
CALL add_element_unless_exists('column', 'f_config', 'deleted', 'ALTER TABLE f_config ADD COLUMN `deleted` tinyint(1) NOT NULL DEFAULT "0" COMMENT "是否删除（0：未删除，1：已删除）" AFTER attribute;');
CALL add_element_unless_exists('column', 'f_config', 'create_time', 'ALTER TABLE f_config ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'f_config', 'creator', 'ALTER TABLE f_config ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'f_config', 'update_time', 'ALTER TABLE f_config ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'f_config', 'updater', 'ALTER TABLE f_config ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('column', 'f_config', 'aws_enable_switch', 'ALTER TABLE f_config ADD COLUMN `aws_enable_switch` tinyint(1) DEFAULT "1" COMMENT "是否上传车场问题图片到ai中心 0:开启  1:关闭" AFTER updater;');
CALL add_element_unless_exists('column', 'f_config', 'guidance_swagger_switch', 'ALTER TABLE f_config ADD COLUMN `guidance_swagger_switch` tinyint(1) DEFAULT "1" COMMENT "parking_guidance服务swagger配置开关 0:开启  1:关闭" AFTER aws_enable_switch;');
CALL add_element_unless_exists('column', 'f_config', 'channel_swagger_switch', 'ALTER TABLE f_config ADD COLUMN `channel_swagger_switch` tinyint(1) DEFAULT "1" COMMENT "channel_service服务swagger配置开关 0:开启  1:关闭" AFTER guidance_swagger_switch;');
CALL add_element_unless_exists('index', 'f_config', 'idx_config_code', 'ALTER TABLE f_config ADD INDEX idx_config_code (config_code) USING BTREE');

-- 更新表 face_info 所有字段和索引
ALTER TABLE face_info CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE face_info COMMENT = '人脸信息表';
CALL add_element_unless_exists('column', 'face_info', 'id', 'ALTER TABLE face_info ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT";');
CALL add_element_unless_exists('column', 'face_info', 'plate_no', 'ALTER TABLE face_info ADD COLUMN `plate_no` varchar(50) DEFAULT "" COMMENT "车牌号码" AFTER id;');
CALL add_element_unless_exists('column', 'face_info', 'face_info', 'ALTER TABLE face_info ADD COLUMN `face_info` longtext COMMENT "人脸信息数据" AFTER plate_no;');
CALL add_element_unless_exists('column', 'face_info', 'is_temp', 'ALTER TABLE face_info ADD COLUMN `is_temp` int(11) DEFAULT "0" COMMENT "是否临时数据" AFTER face_info;');
CALL add_element_unless_exists('column', 'face_info', 'face_id', 'ALTER TABLE face_info ADD COLUMN `face_id` varchar(50) DEFAULT "" COMMENT "人脸信息唯一值" AFTER is_temp;');
CALL add_element_unless_exists('column', 'face_info', 'deleted', 'ALTER TABLE face_info ADD COLUMN `deleted` tinyint(1) NOT NULL DEFAULT "0" COMMENT "是否删除（0：未删除，1：已删除）" AFTER face_id;');
CALL add_element_unless_exists('column', 'face_info', 'create_time', 'ALTER TABLE face_info ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'face_info', 'update_time', 'ALTER TABLE face_info ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER create_time;');

-- 更新表 floor_info 所有字段和索引
ALTER TABLE floor_info CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE floor_info COMMENT = '楼层信息';
CALL add_element_unless_exists('column', 'floor_info', 'id', 'ALTER TABLE floor_info ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'floor_info', 'lot_id', 'ALTER TABLE floor_info ADD COLUMN `lot_id` int(11) NOT NULL COMMENT "车场id lot_info id" AFTER id;');
CALL add_element_unless_exists('column', 'floor_info', 'floor_name', 'ALTER TABLE floor_info ADD COLUMN `floor_name` varchar(255) NOT NULL COMMENT "楼层名称" AFTER lot_id;');
CALL add_element_unless_exists('column', 'floor_info', 'status', 'ALTER TABLE floor_info ADD COLUMN `status` int(11) DEFAULT NULL COMMENT "状态 1启用 2停用" AFTER floor_name;');
CALL add_element_unless_exists('column', 'floor_info', 'sort', 'ALTER TABLE floor_info ADD COLUMN `sort` int(11) NOT NULL COMMENT "楼层顺序（数字越大，楼层越高）" AFTER status;');
CALL add_element_unless_exists('column', 'floor_info', 'scroll_ratio', 'ALTER TABLE floor_info ADD COLUMN `scroll_ratio` int(11) DEFAULT "10" COMMENT "缩放比例（%）" AFTER sort;');
CALL add_element_unless_exists('column', 'floor_info', 'deleted', 'ALTER TABLE floor_info ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除（0：未删除，1：已删除）" AFTER scroll_ratio;');
CALL add_element_unless_exists('column', 'floor_info', 'updater', 'ALTER TABLE floor_info ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER deleted;');
CALL add_element_unless_exists('column', 'floor_info', 'creator', 'ALTER TABLE floor_info ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER updater;');
CALL add_element_unless_exists('column', 'floor_info', 'create_time', 'ALTER TABLE floor_info ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'floor_info', 'update_time', 'ALTER TABLE floor_info ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER create_time;');
CALL add_element_unless_exists('column', 'floor_info', 'remark', 'ALTER TABLE floor_info ADD COLUMN `remark` varchar(255) DEFAULT NULL COMMENT "备注" AFTER update_time;');
CALL add_element_unless_exists('column', 'floor_info', 'floor_unique_identification', 'ALTER TABLE floor_info ADD COLUMN `floor_unique_identification` varchar(32) DEFAULT NULL COMMENT "楼层唯一标识字段" AFTER remark;');
CALL add_element_unless_exists('column', 'floor_info', 'floor_capture', 'ALTER TABLE floor_info ADD COLUMN `floor_capture` varchar(255) DEFAULT NULL COMMENT "楼层底图截图保存URL" AFTER floor_unique_identification;');
CALL add_element_unless_exists('column', 'floor_info', 'capture_source', 'ALTER TABLE floor_info ADD COLUMN `capture_source` tinyint(1) DEFAULT "0" COMMENT "楼层底图来源方式，0:3D手动截图 1:2D地图照片迁移" AFTER floor_capture;');

-- 更新表 general_config 所有字段和索引
ALTER TABLE general_config CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE general_config COMMENT = '通用参数配置信息表';
CALL add_element_unless_exists('column', 'general_config', 'id', 'ALTER TABLE general_config ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'general_config', 'config_key', 'ALTER TABLE general_config ADD COLUMN `config_key` varchar(255) DEFAULT NULL COMMENT "字段唯一标识，禁止重复" AFTER id;');
CALL add_element_unless_exists('column', 'general_config', 'description', 'ALTER TABLE general_config ADD COLUMN `description` varchar(255) DEFAULT NULL COMMENT "字段详细作用描述" AFTER config_key;');
CALL add_element_unless_exists('column', 'general_config', 'config_value', 'ALTER TABLE general_config ADD COLUMN `config_value` varchar(255) DEFAULT NULL COMMENT "字段具体配置信息" AFTER description;');
CALL add_element_unless_exists('column', 'general_config', 'create_time', 'ALTER TABLE general_config ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER config_value;');
CALL add_element_unless_exists('column', 'general_config', 'update_time', 'ALTER TABLE general_config ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER create_time;');

-- 更新表 image_styles 所有字段和索引
ALTER TABLE image_styles CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE image_styles COMMENT = '图标配置表';
CALL add_element_unless_exists('column', 'image_styles', 'id', 'ALTER TABLE image_styles ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'image_styles', 'map_styles_id', 'ALTER TABLE image_styles ADD COLUMN `map_styles_id` int(11) NOT NULL COMMENT "地图样式id" AFTER id;');
CALL add_element_unless_exists('column', 'image_styles', 'record_beacon', 'ALTER TABLE image_styles ADD COLUMN `record_beacon` varchar(255) DEFAULT NULL COMMENT "已录入蓝牙图标url" AFTER map_styles_id;');
CALL add_element_unless_exists('column', 'image_styles', 'no_record_beacon', 'ALTER TABLE image_styles ADD COLUMN `no_record_beacon` varchar(255) DEFAULT NULL COMMENT "未录入蓝牙图标url" AFTER record_beacon;');
CALL add_element_unless_exists('column', 'image_styles', 'vertical_machine', 'ALTER TABLE image_styles ADD COLUMN `vertical_machine` varchar(255) DEFAULT NULL COMMENT "立式找车机图标url" AFTER no_record_beacon;');
CALL add_element_unless_exists('column', 'image_styles', 'wall_machine', 'ALTER TABLE image_styles ADD COLUMN `wall_machine` varchar(255) DEFAULT NULL COMMENT "壁挂式找车机图标url" AFTER vertical_machine;');
CALL add_element_unless_exists('column', 'image_styles', 'vertical_ladder_connector', 'ALTER TABLE image_styles ADD COLUMN `vertical_ladder_connector` varchar(255) DEFAULT NULL COMMENT "直梯图标url" AFTER wall_machine;');
CALL add_element_unless_exists('column', 'image_styles', 'escalator_connector', 'ALTER TABLE image_styles ADD COLUMN `escalator_connector` varchar(255) DEFAULT NULL COMMENT "扶梯图标url" AFTER vertical_ladder_connector;');
CALL add_element_unless_exists('column', 'image_styles', 'stairs_connector', 'ALTER TABLE image_styles ADD COLUMN `stairs_connector` varchar(255) DEFAULT NULL COMMENT "楼梯图标url" AFTER escalator_connector;');
CALL add_element_unless_exists('column', 'image_styles', 'passageway_connector', 'ALTER TABLE image_styles ADD COLUMN `passageway_connector` varchar(255) DEFAULT NULL COMMENT "出入口图标url" AFTER stairs_connector;');
CALL add_element_unless_exists('column', 'image_styles', 'screen_lcd_url', 'ALTER TABLE image_styles ADD COLUMN `screen_lcd_url` varchar(255) DEFAULT "" COMMENT "LCD屏图标URL" AFTER passageway_connector;');
CALL add_element_unless_exists('column', 'image_styles', 'screen_led_url', 'ALTER TABLE image_styles ADD COLUMN `screen_led_url` varchar(255) DEFAULT "" COMMENT "LED屏图标URL" AFTER screen_lcd_url;');
CALL add_element_unless_exists('column', 'image_styles', 'is_show_name_machine', 'ALTER TABLE image_styles ADD COLUMN `is_show_name_machine` tinyint(1) DEFAULT "0" COMMENT "找车机是否显示元素名称  0：不显示  1：显示" AFTER screen_led_url;');
CALL add_element_unless_exists('column', 'image_styles', 'is_show_name_connector', 'ALTER TABLE image_styles ADD COLUMN `is_show_name_connector` tinyint(1) DEFAULT "0" COMMENT "通行设施是否显示元素名称  0：不显示  1：显示" AFTER is_show_name_machine;');
CALL add_element_unless_exists('column', 'image_styles', 'deleted', 'ALTER TABLE image_styles ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除（0：未删除，1：已删除）" AFTER is_show_name_connector;');
CALL add_element_unless_exists('column', 'image_styles', 'updater', 'ALTER TABLE image_styles ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER deleted;');
CALL add_element_unless_exists('column', 'image_styles', 'creator', 'ALTER TABLE image_styles ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER updater;');
CALL add_element_unless_exists('column', 'image_styles', 'create_time', 'ALTER TABLE image_styles ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'image_styles', 'update_time', 'ALTER TABLE image_styles ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER create_time;');
CALL add_element_unless_exists('index', 'image_styles', 'index_map_styles_id', 'ALTER TABLE image_styles ADD INDEX index_map_styles_id (map_styles_id) USING BTREE');

-- 更新表 info_across_floor 所有字段和索引
ALTER TABLE info_across_floor CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE info_across_floor COMMENT = '跨层寻车用指引设置表';
CALL add_element_unless_exists('column', 'info_across_floor', 'id', 'ALTER TABLE info_across_floor ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT";');
CALL add_element_unless_exists('column', 'info_across_floor', 'start_id', 'ALTER TABLE info_across_floor ADD COLUMN `start_id` int(11) DEFAULT NULL COMMENT "起点楼层ID" AFTER id;');
CALL add_element_unless_exists('column', 'info_across_floor', 'end_id', 'ALTER TABLE info_across_floor ADD COLUMN `end_id` int(11) DEFAULT NULL COMMENT "终点楼层ID" AFTER start_id;');
CALL add_element_unless_exists('column', 'info_across_floor', 'end_name', 'ALTER TABLE info_across_floor ADD COLUMN `end_name` varchar(255) DEFAULT NULL COMMENT "终点楼层名称" AFTER end_id;');
CALL add_element_unless_exists('column', 'info_across_floor', 'start_name', 'ALTER TABLE info_across_floor ADD COLUMN `start_name` varchar(255) DEFAULT NULL COMMENT "起点楼层名称" AFTER end_name;');
CALL add_element_unless_exists('column', 'info_across_floor', 'across_elevator_id', 'ALTER TABLE info_across_floor ADD COLUMN `across_elevator_id` int(11) DEFAULT NULL COMMENT "通行设施ID" AFTER start_name;');
CALL add_element_unless_exists('column', 'info_across_floor', 'across_elevator_name', 'ALTER TABLE info_across_floor ADD COLUMN `across_elevator_name` varchar(255) DEFAULT NULL COMMENT "通行设施名称" AFTER across_elevator_id;');
CALL add_element_unless_exists('column', 'info_across_floor', 'img_src', 'ALTER TABLE info_across_floor ADD COLUMN `img_src` varchar(255) DEFAULT NULL COMMENT "提示图片" AFTER across_elevator_name;');
CALL add_element_unless_exists('column', 'info_across_floor', 'across_type', 'ALTER TABLE info_across_floor ADD COLUMN `across_type` int(11) DEFAULT "0" COMMENT "跨层类型(0:楼层到楼层 1:查询机到楼层)" AFTER img_src;');
CALL add_element_unless_exists('column', 'info_across_floor', 'deleted', 'ALTER TABLE info_across_floor ADD COLUMN `deleted` tinyint(1) NOT NULL DEFAULT "0" COMMENT "是否删除（0：未删除，1：已删除）" AFTER across_type;');
CALL add_element_unless_exists('column', 'info_across_floor', 'creator', 'ALTER TABLE info_across_floor ADD COLUMN `creator` varchar(255) DEFAULT NULL COMMENT "创建人" AFTER deleted;');
CALL add_element_unless_exists('column', 'info_across_floor', 'create_time', 'ALTER TABLE info_across_floor ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'info_across_floor', 'updater', 'ALTER TABLE info_across_floor ADD COLUMN `updater` varchar(255) DEFAULT NULL COMMENT "更新人" AFTER create_time;');
CALL add_element_unless_exists('column', 'info_across_floor', 'update_time', 'ALTER TABLE info_across_floor ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');

-- 更新表 info_machine_config 所有字段和索引
ALTER TABLE info_machine_config CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE info_machine_config COMMENT = '找车机常用参数表';
CALL add_element_unless_exists('column', 'info_machine_config', 'id', 'ALTER TABLE info_machine_config ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT";');
CALL add_element_unless_exists('column', 'info_machine_config', 'inquire_ways', 'ALTER TABLE info_machine_config ADD COLUMN `inquire_ways` varchar(200) DEFAULT NULL COMMENT "查询方式" AFTER id;');
CALL add_element_unless_exists('column', 'info_machine_config', 'empty_plate_record_count', 'ALTER TABLE info_machine_config ADD COLUMN `empty_plate_record_count` int(11) DEFAULT "25" COMMENT "空车牌查询显示记录上限" AFTER inquire_ways;');
CALL add_element_unless_exists('column', 'info_machine_config', 'plate_max_num', 'ALTER TABLE info_machine_config ADD COLUMN `plate_max_num` int(11) DEFAULT "6" COMMENT "车牌号输入上限" AFTER empty_plate_record_count;');
CALL add_element_unless_exists('column', 'info_machine_config', 'park_max_num', 'ALTER TABLE info_machine_config ADD COLUMN `park_max_num` int(11) DEFAULT "6" COMMENT "车位号输入上限" AFTER plate_max_num;');
CALL add_element_unless_exists('column', 'info_machine_config', 'deleted', 'ALTER TABLE info_machine_config ADD COLUMN `deleted` tinyint(1) NOT NULL DEFAULT "0" COMMENT "是否删除（0：未删除，1：已删除）" AFTER park_max_num;');
CALL add_element_unless_exists('column', 'info_machine_config', 'creator', 'ALTER TABLE info_machine_config ADD COLUMN `creator` varchar(255) DEFAULT NULL COMMENT "创建人" AFTER deleted;');
CALL add_element_unless_exists('column', 'info_machine_config', 'create_time', 'ALTER TABLE info_machine_config ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'info_machine_config', 'updater', 'ALTER TABLE info_machine_config ADD COLUMN `updater` varchar(255) DEFAULT NULL COMMENT "更新人" AFTER create_time;');
CALL add_element_unless_exists('column', 'info_machine_config', 'update_time', 'ALTER TABLE info_machine_config ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');
CALL add_element_unless_exists('column', 'info_machine_config', 'websocket_version_code', 'ALTER TABLE info_machine_config ADD COLUMN `websocket_version_code` varchar(32) DEFAULT NULL COMMENT "用于判断当前人脸信息和找车机上是否一致，这个随机值下发给找车机进行判断" AFTER update_time;');
CALL add_element_unless_exists('column', 'info_machine_config', 'is_open_print', 'ALTER TABLE info_machine_config ADD COLUMN `is_open_print` tinyint(1) DEFAULT "1" COMMENT "是否启用停车打印功能 0:不启用 1:启用" AFTER websocket_version_code;');
CALL add_element_unless_exists('column', 'info_machine_config', 'machine_map_switch', 'ALTER TABLE info_machine_config ADD COLUMN `machine_map_switch` tinyint(1) DEFAULT "1" COMMENT "找车机是否开启3D地图(1为开启  0 为关闭)" AFTER is_open_print;');
CALL add_element_unless_exists('column', 'info_machine_config', 'schedule_face', 'ALTER TABLE info_machine_config ADD COLUMN `schedule_face` tinyint(1) DEFAULT "1" COMMENT "定时给找车机推送车辆出场，删除人脸数据(0为开启  1为关闭)" AFTER machine_map_switch;');
CALL add_element_unless_exists('column', 'info_machine_config', 'is_open_qrcode', 'ALTER TABLE info_machine_config ADD COLUMN `is_open_qrcode` tinyint(1) DEFAULT "0" COMMENT "是否显示找车二维码(0：否，1：是)" AFTER schedule_face;');
CALL add_element_unless_exists('column', 'info_machine_config', 'rotation_switch', 'ALTER TABLE info_machine_config ADD COLUMN `rotation_switch` int(11) DEFAULT "1" COMMENT "初始化时找车机地图是否根据找车机朝向旋转(0为开启  1为关闭)，默认关闭" AFTER is_open_qrcode;');
CALL add_element_unless_exists('column', 'info_machine_config', 'rotation_angle', 'ALTER TABLE info_machine_config ADD COLUMN `rotation_angle` int(11) DEFAULT "0" COMMENT "初始化时找车机旋转角度，0-360" AFTER rotation_switch;');
CALL add_element_unless_exists('column', 'info_machine_config', 'language_support', 'ALTER TABLE info_machine_config ADD COLUMN `language_support` tinyint(4) DEFAULT "0" COMMENT "语言支持  0=中文+英文  1=中文  2=英文" AFTER rotation_angle;');
CALL add_element_unless_exists('column', 'info_machine_config', 'foregin_language', 'ALTER TABLE info_machine_config ADD COLUMN `foregin_language` varchar(50) DEFAULT NULL COMMENT "设置的第三种语言支持 ms=马来西亚 esp=西班牙 未设置则返回空" AFTER language_support;');
CALL add_element_unless_exists('column', 'info_machine_config', 'route_qr_switch', 'ALTER TABLE info_machine_config ADD COLUMN `route_qr_switch` tinyint(4) DEFAULT "0" COMMENT "找车路线二维码开关  0=关  1=开" AFTER foregin_language;');
CALL add_element_unless_exists('column', 'info_machine_config', 'route_qr_type', 'ALTER TABLE info_machine_config ADD COLUMN `route_qr_type` tinyint(4) DEFAULT "0" COMMENT "找车路线二维码类型  0=自定义二维码" AFTER route_qr_switch;');
CALL add_element_unless_exists('column', 'info_machine_config', 'route_qr_url', 'ALTER TABLE info_machine_config ADD COLUMN `route_qr_url` varchar(255) DEFAULT NULL COMMENT "找车路线二维码图片路径" AFTER route_qr_type;');

-- 更新表 ini_config 所有字段和索引
ALTER TABLE ini_config CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE ini_config COMMENT = 'C++参数配置表';
CALL add_element_unless_exists('column', 'ini_config', 'id', 'ALTER TABLE ini_config ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'ini_config', 'dsp_recog', 'ALTER TABLE ini_config ADD COLUMN `dsp_recog` tinyint(1) DEFAULT "0" COMMENT "控制软识别与硬识别 0 软识别, 1 硬识别" AFTER id;');
CALL add_element_unless_exists('column', 'ini_config', 'witch', 'ALTER TABLE ini_config ADD COLUMN `witch` tinyint(1) DEFAULT "0" COMMENT "控制故障状态的设备的开关 0 关闭， 1 开启" AFTER dsp_recog;');
CALL add_element_unless_exists('column', 'ini_config', 'comname', 'ALTER TABLE ini_config ADD COLUMN `comname` varchar(255) DEFAULT NULL COMMENT "连接服务器的端口号 windows下是COM5, linux下是 /dev/ttyS0" AFTER witch;');
CALL add_element_unless_exists('column', 'ini_config', 'ret', 'ALTER TABLE ini_config ADD COLUMN `ret` tinyint(1) DEFAULT "0" COMMENT "控制TCP还是485通讯 0 tcp, 1 485" AFTER comname;');
CALL add_element_unless_exists('column', 'ini_config', 'province', 'ALTER TABLE ini_config ADD COLUMN `province` varchar(255) DEFAULT NULL COMMENT "车牌的默认省份(省份简称汉字) 默认为空" AFTER ret;');
CALL add_element_unless_exists('column', 'ini_config', 'pic_switch', 'ALTER TABLE ini_config ADD COLUMN `pic_switch` tinyint(1) DEFAULT "0" COMMENT "是否开启空车牌图片收集功能  1 开启,  0 关闭" AFTER province;');
CALL add_element_unless_exists('column', 'ini_config', 'creator', 'ALTER TABLE ini_config ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER pic_switch;');
CALL add_element_unless_exists('column', 'ini_config', 'create_time', 'ALTER TABLE ini_config ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'ini_config', 'updater', 'ALTER TABLE ini_config ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER create_time;');
CALL add_element_unless_exists('column', 'ini_config', 'update_time', 'ALTER TABLE ini_config ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');

-- 更新表 internationalization 所有字段和索引
ALTER TABLE internationalization CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE internationalization COMMENT = '国际化';
CALL add_element_unless_exists('column', 'internationalization', 'id', 'ALTER TABLE internationalization ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'internationalization', 'code', 'ALTER TABLE internationalization ADD COLUMN `code` varchar(100) NOT NULL COMMENT "代码，前缀是front.的为前端，前缀是server.的为后端" AFTER id;');
CALL add_element_unless_exists('column', 'internationalization', 'description', 'ALTER TABLE internationalization ADD COLUMN `description` varchar(100) DEFAULT NULL COMMENT "描述" AFTER code;');
CALL add_element_unless_exists('column', 'internationalization', 'chinese', 'ALTER TABLE internationalization ADD COLUMN `chinese` varchar(500) DEFAULT NULL COMMENT "简体中文" AFTER description;');
CALL add_element_unless_exists('column', 'internationalization', 'english', 'ALTER TABLE internationalization ADD COLUMN `english` varchar(500) DEFAULT NULL COMMENT "英文" AFTER chinese;');
CALL add_element_unless_exists('column', 'internationalization', 'other1', 'ALTER TABLE internationalization ADD COLUMN `other1` varchar(500) DEFAULT NULL COMMENT "其他语言1，预留字段" AFTER english;');
CALL add_element_unless_exists('column', 'internationalization', 'other2', 'ALTER TABLE internationalization ADD COLUMN `other2` varchar(500) DEFAULT NULL COMMENT "其他语言2，预留字段" AFTER other1;');
CALL add_element_unless_exists('column', 'internationalization', 'other3', 'ALTER TABLE internationalization ADD COLUMN `other3` varchar(500) DEFAULT NULL COMMENT "其他语言3，预留字段" AFTER other2;');
CALL add_element_unless_exists('column', 'internationalization', 'other4', 'ALTER TABLE internationalization ADD COLUMN `other4` varchar(500) DEFAULT NULL COMMENT "其他语言4，预留字段" AFTER other3;');
CALL add_element_unless_exists('column', 'internationalization', 'deleted', 'ALTER TABLE internationalization ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "删除状态  0：未删除   1：已删除" AFTER other4;');
CALL add_element_unless_exists('column', 'internationalization', 'create_time', 'ALTER TABLE internationalization ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'internationalization', 'update_time', 'ALTER TABLE internationalization ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER create_time;');
CALL add_element_unless_exists('index', 'internationalization', 'udx_code', 'ALTER TABLE internationalization ADD UNIQUE INDEX udx_code (code) USING BTREE');

-- 更新表 internationalization_relation 所有字段和索引
ALTER TABLE internationalization_relation CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE internationalization_relation COMMENT = '国际化字段与语言关系表';
CALL add_element_unless_exists('column', 'internationalization_relation', 'id', 'ALTER TABLE internationalization_relation ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'internationalization_relation', 'name', 'ALTER TABLE internationalization_relation ADD COLUMN `name` varchar(100) DEFAULT "待配置" COMMENT "语言名称，用于显示在前端用于选择语言" AFTER id;');
CALL add_element_unless_exists('column', 'internationalization_relation', 'field', 'ALTER TABLE internationalization_relation ADD COLUMN `field` varchar(100) DEFAULT NULL COMMENT "internationalization表的字段名" AFTER name;');
CALL add_element_unless_exists('column', 'internationalization_relation', 'shorthand', 'ALTER TABLE internationalization_relation ADD COLUMN `shorthand` varchar(100) DEFAULT NULL COMMENT "语言简称，用于前端组件自带的国际化，如：zh_CN：简体中文  en_GB：英语" AFTER field;');
CALL add_element_unless_exists('column', 'internationalization_relation', 'sort', 'ALTER TABLE internationalization_relation ADD COLUMN `sort` int(11) DEFAULT "0" COMMENT "排序" AFTER shorthand;');
CALL add_element_unless_exists('column', 'internationalization_relation', 'status', 'ALTER TABLE internationalization_relation ADD COLUMN `status` tinyint(1) DEFAULT "0" COMMENT "状态  0：未启用   1：启用" AFTER sort;');
CALL add_element_unless_exists('column', 'internationalization_relation', 'update_package_status', 'ALTER TABLE internationalization_relation ADD COLUMN `update_package_status` tinyint(1) DEFAULT "0" COMMENT "上传语言包状态  0：未上传   1：已上传" AFTER status;');
CALL add_element_unless_exists('column', 'internationalization_relation', 'create_time', 'ALTER TABLE internationalization_relation ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER update_package_status;');
CALL add_element_unless_exists('column', 'internationalization_relation', 'update_time', 'ALTER TABLE internationalization_relation ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER create_time;');

-- 更新表 lcd_advertisement_config 所有字段和索引
ALTER TABLE lcd_advertisement_config CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE lcd_advertisement_config COMMENT = 'LCD屏广告配置表';
CALL add_element_unless_exists('column', 'lcd_advertisement_config', 'id', 'ALTER TABLE lcd_advertisement_config ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'lcd_advertisement_config', 'lcd_advertisement_scheme_id', 'ALTER TABLE lcd_advertisement_config ADD COLUMN `lcd_advertisement_scheme_id` int(11) DEFAULT NULL COMMENT "LCD屏广告方案id" AFTER id;');
CALL add_element_unless_exists('column', 'lcd_advertisement_config', 'remark', 'ALTER TABLE lcd_advertisement_config ADD COLUMN `remark` varchar(255) DEFAULT "" COMMENT "备注" AFTER lcd_advertisement_scheme_id;');
CALL add_element_unless_exists('column', 'lcd_advertisement_config', 'play_sort', 'ALTER TABLE lcd_advertisement_config ADD COLUMN `play_sort` int(11) DEFAULT NULL COMMENT "播放顺序" AFTER remark;');
CALL add_element_unless_exists('column', 'lcd_advertisement_config', 'file_name', 'ALTER TABLE lcd_advertisement_config ADD COLUMN `file_name` varchar(255) DEFAULT "" COMMENT "文件名" AFTER play_sort;');
CALL add_element_unless_exists('column', 'lcd_advertisement_config', 'deleted', 'ALTER TABLE lcd_advertisement_config ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除0未删除1已删除" AFTER file_name;');
CALL add_element_unless_exists('column', 'lcd_advertisement_config', 'create_time', 'ALTER TABLE lcd_advertisement_config ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'lcd_advertisement_config', 'creator', 'ALTER TABLE lcd_advertisement_config ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'lcd_advertisement_config', 'update_time', 'ALTER TABLE lcd_advertisement_config ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'lcd_advertisement_config', 'updater', 'ALTER TABLE lcd_advertisement_config ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'lcd_advertisement_config', 'index_lcd_advertisement_scheme_id', 'ALTER TABLE lcd_advertisement_config ADD INDEX index_lcd_advertisement_scheme_id (lcd_advertisement_scheme_id) USING BTREE');

-- 更新表 lcd_advertisement_scheme 所有字段和索引
ALTER TABLE lcd_advertisement_scheme CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE lcd_advertisement_scheme COMMENT = 'LCD屏广告方案表';
CALL add_element_unless_exists('column', 'lcd_advertisement_scheme', 'id', 'ALTER TABLE lcd_advertisement_scheme ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'lcd_advertisement_scheme', 'name', 'ALTER TABLE lcd_advertisement_scheme ADD COLUMN `name` varchar(255) DEFAULT "" COMMENT "方案名称" AFTER id;');
CALL add_element_unless_exists('column', 'lcd_advertisement_scheme', 'species', 'ALTER TABLE lcd_advertisement_scheme ADD COLUMN `species` tinyint(4) DEFAULT NULL COMMENT "类型 1：图片 2：视频" AFTER name;');
CALL add_element_unless_exists('column', 'lcd_advertisement_scheme', 'carousel_seconds', 'ALTER TABLE lcd_advertisement_scheme ADD COLUMN `carousel_seconds` int(11) DEFAULT "0" COMMENT "轮播时间 单位s(秒)" AFTER species;');
CALL add_element_unless_exists('column', 'lcd_advertisement_scheme', 'deleted', 'ALTER TABLE lcd_advertisement_scheme ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除0未删除1已删除" AFTER carousel_seconds;');
CALL add_element_unless_exists('column', 'lcd_advertisement_scheme', 'create_time', 'ALTER TABLE lcd_advertisement_scheme ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'lcd_advertisement_scheme', 'creator', 'ALTER TABLE lcd_advertisement_scheme ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'lcd_advertisement_scheme', 'update_time', 'ALTER TABLE lcd_advertisement_scheme ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'lcd_advertisement_scheme', 'updater', 'ALTER TABLE lcd_advertisement_scheme ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');

-- 更新表 lcd_screen_config 所有字段和索引
ALTER TABLE lcd_screen_config CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE lcd_screen_config COMMENT = 'LCD屏配置';
CALL add_element_unless_exists('column', 'lcd_screen_config', 'id', 'ALTER TABLE lcd_screen_config ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'lcd_screen_config', 'element_screen_id', 'ALTER TABLE lcd_screen_config ADD COLUMN `element_screen_id` int(11) DEFAULT NULL COMMENT "主屏id" AFTER id;');
CALL add_element_unless_exists('column', 'lcd_screen_config', 'show_type', 'ALTER TABLE lcd_screen_config ADD COLUMN `show_type` tinyint(4) DEFAULT NULL COMMENT "显示内容 1：引导内容 2：广告" AFTER element_screen_id;');
CALL add_element_unless_exists('column', 'lcd_screen_config', 'attribute_id', 'ALTER TABLE lcd_screen_config ADD COLUMN `attribute_id` int(11) DEFAULT NULL COMMENT "若显示内容是 1，则为子屏id， 若显示内容为2 则为广告id" AFTER show_type;');
CALL add_element_unless_exists('column', 'lcd_screen_config', 'show_sort', 'ALTER TABLE lcd_screen_config ADD COLUMN `show_sort` int(11) DEFAULT NULL COMMENT "显示顺序" AFTER attribute_id;');
CALL add_element_unless_exists('column', 'lcd_screen_config', 'belong_id', 'ALTER TABLE lcd_screen_config ADD COLUMN `belong_id` tinyint(4) DEFAULT NULL COMMENT "所属id id相同表示属于同一个物理屏" AFTER show_sort;');
CALL add_element_unless_exists('column', 'lcd_screen_config', 'deleted', 'ALTER TABLE lcd_screen_config ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除0未删除1已删除" AFTER belong_id;');
CALL add_element_unless_exists('column', 'lcd_screen_config', 'create_time', 'ALTER TABLE lcd_screen_config ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'lcd_screen_config', 'creator', 'ALTER TABLE lcd_screen_config ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'lcd_screen_config', 'update_time', 'ALTER TABLE lcd_screen_config ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'lcd_screen_config', 'updater', 'ALTER TABLE lcd_screen_config ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'lcd_screen_config', 'index_element_screen_id', 'ALTER TABLE lcd_screen_config ADD INDEX index_element_screen_id (element_screen_id) USING BTREE');

-- 更新表 light_scheme_plan 所有字段和索引
ALTER TABLE light_scheme_plan CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE light_scheme_plan COMMENT = '车位灯方案下发计划';
CALL add_element_unless_exists('column', 'light_scheme_plan', 'id', 'ALTER TABLE light_scheme_plan ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'light_scheme_plan', 'name', 'ALTER TABLE light_scheme_plan ADD COLUMN `name` varchar(50) DEFAULT NULL COMMENT "方案名称" AFTER id;');
CALL add_element_unless_exists('column', 'light_scheme_plan', 'system_type', 'ALTER TABLE light_scheme_plan ADD COLUMN `system_type` tinyint(4) DEFAULT "1" COMMENT "设备类型  0-DSP车位相机   1-NODE节点控制器" AFTER name;');
CALL add_element_unless_exists('column', 'light_scheme_plan', 'light_type', 'ALTER TABLE light_scheme_plan ADD COLUMN `light_type` tinyint(4) DEFAULT "1" COMMENT "灯类型   1-有线多彩灯  2-有线双色灯" AFTER system_type;');
CALL add_element_unless_exists('column', 'light_scheme_plan', 'occupy_color', 'ALTER TABLE light_scheme_plan ADD COLUMN `occupy_color` tinyint(4) DEFAULT NULL COMMENT "占用颜色" AFTER light_type;');
CALL add_element_unless_exists('column', 'light_scheme_plan', 'free_color', 'ALTER TABLE light_scheme_plan ADD COLUMN `free_color` tinyint(4) DEFAULT NULL COMMENT "空闲颜色" AFTER occupy_color;');
CALL add_element_unless_exists('column', 'light_scheme_plan', 'warning_color', 'ALTER TABLE light_scheme_plan ADD COLUMN `warning_color` tinyint(4) DEFAULT NULL COMMENT "告警颜色" AFTER free_color;');
CALL add_element_unless_exists('column', 'light_scheme_plan', 'send_time', 'ALTER TABLE light_scheme_plan ADD COLUMN `send_time` datetime DEFAULT NULL COMMENT "下发时间" AFTER warning_color;');
CALL add_element_unless_exists('column', 'light_scheme_plan', 'status', 'ALTER TABLE light_scheme_plan ADD COLUMN `status` tinyint(4) DEFAULT "1" COMMENT "下发状态  1-未生效  2-下发成功  3-下发失败  4-取消" AFTER send_time;');
CALL add_element_unless_exists('column', 'light_scheme_plan', 'create_time', 'ALTER TABLE light_scheme_plan ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER status;');
CALL add_element_unless_exists('column', 'light_scheme_plan', 'creator', 'ALTER TABLE light_scheme_plan ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'light_scheme_plan', 'update_time', 'ALTER TABLE light_scheme_plan ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'light_scheme_plan', 'updater', 'ALTER TABLE light_scheme_plan ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');

-- 更新表 light_scheme_plan_park_relation 所有字段和索引
ALTER TABLE light_scheme_plan_park_relation CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE light_scheme_plan_park_relation COMMENT = '车位灯方案下发计划与车位关系表';
CALL add_element_unless_exists('column', 'light_scheme_plan_park_relation', 'id', 'ALTER TABLE light_scheme_plan_park_relation ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'light_scheme_plan_park_relation', 'plan_id', 'ALTER TABLE light_scheme_plan_park_relation ADD COLUMN `plan_id` int(11) DEFAULT NULL COMMENT "车位灯方案下发计划id" AFTER id;');
CALL add_element_unless_exists('column', 'light_scheme_plan_park_relation', 'element_park_id', 'ALTER TABLE light_scheme_plan_park_relation ADD COLUMN `element_park_id` int(11) DEFAULT NULL COMMENT "车位id" AFTER plan_id;');
CALL add_element_unless_exists('column', 'light_scheme_plan_park_relation', 'create_time', 'ALTER TABLE light_scheme_plan_park_relation ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER element_park_id;');
CALL add_element_unless_exists('column', 'light_scheme_plan_park_relation', 'creator', 'ALTER TABLE light_scheme_plan_park_relation ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');

-- 更新表 lot_info 所有字段和索引
ALTER TABLE lot_info CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE lot_info COMMENT = '车场信息';
CALL add_element_unless_exists('column', 'lot_info', 'id', 'ALTER TABLE lot_info ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'lot_info', 'lot_code', 'ALTER TABLE lot_info ADD COLUMN `lot_code` varchar(100) DEFAULT NULL COMMENT "车场编码" AFTER id;');
CALL add_element_unless_exists('column', 'lot_info', 'lot_name', 'ALTER TABLE lot_info ADD COLUMN `lot_name` varchar(255) NOT NULL COMMENT "车场名称" AFTER lot_code;');
CALL add_element_unless_exists('column', 'lot_info', 'device_id', 'ALTER TABLE lot_info ADD COLUMN `device_id` varchar(100) DEFAULT NULL COMMENT "场端设备id，用于统一接口通信" AFTER lot_name;');
CALL add_element_unless_exists('column', 'lot_info', 'addr', 'ALTER TABLE lot_info ADD COLUMN `addr` varchar(1000) DEFAULT NULL COMMENT "车场地址" AFTER device_id;');
CALL add_element_unless_exists('column', 'lot_info', 'tel', 'ALTER TABLE lot_info ADD COLUMN `tel` varchar(50) DEFAULT NULL COMMENT "联系电话" AFTER addr;');
CALL add_element_unless_exists('column', 'lot_info', 'secret', 'ALTER TABLE lot_info ADD COLUMN `secret` varchar(50) DEFAULT NULL COMMENT "密钥（接口加密使用）" AFTER tel;');
CALL add_element_unless_exists('column', 'lot_info', 'create_time', 'ALTER TABLE lot_info ADD COLUMN `create_time` datetime NOT NULL COMMENT "创建时间" AFTER secret;');
CALL add_element_unless_exists('column', 'lot_info', 'update_time', 'ALTER TABLE lot_info ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER create_time;');
CALL add_element_unless_exists('column', 'lot_info', 'system_type', 'ALTER TABLE lot_info ADD COLUMN `system_type` tinyint(1) DEFAULT "3" COMMENT "C++端部署形式  1:引导系统  2:找车系统  3:引导系统和找车系统同时部署" AFTER update_time;');
CALL add_element_unless_exists('column', 'lot_info', 'server_ip', 'ALTER TABLE lot_info ADD COLUMN `server_ip` varchar(32) DEFAULT "127.0.0.1" COMMENT "服务器IP" AFTER system_type;');
CALL add_element_unless_exists('column', 'lot_info', 'device_ip_prefix', 'ALTER TABLE lot_info ADD COLUMN `device_ip_prefix` varchar(32) DEFAULT "192.168." COMMENT "设备IP网段前缀" AFTER server_ip;');
CALL add_element_unless_exists('column', 'lot_info', 'park_repeat_switch', 'ALTER TABLE lot_info ADD COLUMN `park_repeat_switch` tinyint(1) DEFAULT "0" COMMENT "车位编号限制 0:不允许重复的车位编号  1:允许重复车位编号" AFTER device_ip_prefix;');
CALL add_element_unless_exists('column', 'lot_info', 'map_type', 'ALTER TABLE lot_info ADD COLUMN `map_type` tinyint(1) DEFAULT "1" COMMENT "地图类型 0:2D地图 1:3D地图" AFTER park_repeat_switch;');
CALL add_element_unless_exists('column', 'lot_info', 'status', 'ALTER TABLE lot_info ADD COLUMN `status` int(11) DEFAULT "1" COMMENT "车场状态(0 禁用  1 启用） " AFTER map_type;');
CALL add_element_unless_exists('column', 'lot_info', 'machine_debug', 'ALTER TABLE lot_info ADD COLUMN `machine_debug` int(11) DEFAULT "0" COMMENT "找车机是否为调试模式(0 关闭 1 开启)" AFTER status;');
CALL add_element_unless_exists('column', 'lot_info', 'lisence_authorize_code', 'ALTER TABLE lot_info ADD COLUMN `lisence_authorize_code` varchar(1024) DEFAULT NULL COMMENT "Lisence授权码" AFTER machine_debug;');
CALL add_element_unless_exists('column', 'lot_info', 'lisence_trial_period', 'ALTER TABLE lot_info ADD COLUMN `lisence_trial_period` datetime DEFAULT NULL COMMENT "Lisence首次默认30天试用期(寻车服务首次启动时，开始生效)，开始试用时间" AFTER lisence_authorize_code;');

-- 更新表 machine_advertisement_config 所有字段和索引
ALTER TABLE machine_advertisement_config CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE machine_advertisement_config COMMENT = '找车机广告配置';
CALL add_element_unless_exists('column', 'machine_advertisement_config', 'id', 'ALTER TABLE machine_advertisement_config ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'machine_advertisement_config', 'machine_ad_scheme_id', 'ALTER TABLE machine_advertisement_config ADD COLUMN `machine_ad_scheme_id` int(11) DEFAULT NULL COMMENT "找车机广告方案id" AFTER id;');
CALL add_element_unless_exists('column', 'machine_advertisement_config', 'screen_ad_scheme_id', 'ALTER TABLE machine_advertisement_config ADD COLUMN `screen_ad_scheme_id` int(11) DEFAULT NULL COMMENT "广告屏广告方案id" AFTER machine_ad_scheme_id;');
CALL add_element_unless_exists('column', 'machine_advertisement_config', 'machine_ip', 'ALTER TABLE machine_advertisement_config ADD COLUMN `machine_ip` varchar(64) DEFAULT "" COMMENT "找车机ip" AFTER screen_ad_scheme_id;');
CALL add_element_unless_exists('column', 'machine_advertisement_config', 'type', 'ALTER TABLE machine_advertisement_config ADD COLUMN `type` tinyint(4) DEFAULT "0" COMMENT "类型 0-全局 1-单独配置" AFTER machine_ip;');
CALL add_element_unless_exists('column', 'machine_advertisement_config', 'create_time', 'ALTER TABLE machine_advertisement_config ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER type;');
CALL add_element_unless_exists('column', 'machine_advertisement_config', 'creator', 'ALTER TABLE machine_advertisement_config ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'machine_advertisement_config', 'update_time', 'ALTER TABLE machine_advertisement_config ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'machine_advertisement_config', 'updater', 'ALTER TABLE machine_advertisement_config ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'machine_advertisement_config', 'idx_machine_ad_scheme_id', 'ALTER TABLE machine_advertisement_config ADD INDEX idx_machine_ad_scheme_id (machine_ad_scheme_id) USING BTREE');
CALL add_element_unless_exists('index', 'machine_advertisement_config', 'idx_machine_ip', 'ALTER TABLE machine_advertisement_config ADD INDEX idx_machine_ip (machine_ip) USING BTREE');
CALL add_element_unless_exists('index', 'machine_advertisement_config', 'idx_screen_ad_scheme_id', 'ALTER TABLE machine_advertisement_config ADD INDEX idx_screen_ad_scheme_id (screen_ad_scheme_id) USING BTREE');

-- 更新表 map_styles 所有字段和索引
ALTER TABLE map_styles CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE map_styles COMMENT = '地图样式配置表';
CALL add_element_unless_exists('column', 'map_styles', 'id', 'ALTER TABLE map_styles ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'map_styles', 'lot_id', 'ALTER TABLE map_styles ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id" AFTER id;');
CALL add_element_unless_exists('column', 'map_styles', 'name', 'ALTER TABLE map_styles ADD COLUMN `name` varchar(32) NOT NULL COMMENT "样式名称" AFTER lot_id;');
CALL add_element_unless_exists('column', 'map_styles', 'remark', 'ALTER TABLE map_styles ADD COLUMN `remark` varchar(32) DEFAULT NULL COMMENT "备注" AFTER name;');
CALL add_element_unless_exists('column', 'map_styles', 'is_using', 'ALTER TABLE map_styles ADD COLUMN `is_using` tinyint(1) DEFAULT "0" COMMENT "当前配置使用状态 0：未使用，1：正在使用" AFTER remark;');
CALL add_element_unless_exists('column', 'map_styles', 'deleted', 'ALTER TABLE map_styles ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "true：启用，false：禁用（原作为是否删除表示，但此处做逻辑删除，遂复用这字段，真正删除使用的物理删除）" AFTER is_using;');
CALL add_element_unless_exists('column', 'map_styles', 'updater', 'ALTER TABLE map_styles ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER deleted;');
CALL add_element_unless_exists('column', 'map_styles', 'creator', 'ALTER TABLE map_styles ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER updater;');
CALL add_element_unless_exists('column', 'map_styles', 'create_time', 'ALTER TABLE map_styles ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'map_styles', 'update_time', 'ALTER TABLE map_styles ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER create_time;');

-- 更新表 node_device 所有字段和索引
ALTER TABLE node_device CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE node_device COMMENT = '节点设备';
CALL add_element_unless_exists('column', 'node_device', 'id', 'ALTER TABLE node_device ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'node_device', 'addr', 'ALTER TABLE node_device ADD COLUMN `addr` int(11) DEFAULT NULL COMMENT "IPCAM总地址|DSP总地址" AFTER id;');
CALL add_element_unless_exists('column', 'node_device', 'device_type', 'ALTER TABLE node_device ADD COLUMN `device_type` int(11) DEFAULT NULL COMMENT "节点设备类型：1：相机  2：485节点 3：网络4字节 4：网络8字节 5：网络10 字节" AFTER addr;');
CALL add_element_unless_exists('column', 'node_device', 'relate_park_num', 'ALTER TABLE node_device ADD COLUMN `relate_park_num` int(11) DEFAULT NULL COMMENT "关联车位数" AFTER device_type;');
CALL add_element_unless_exists('column', 'node_device', 'status', 'ALTER TABLE node_device ADD COLUMN `status` int(11) DEFAULT "0" COMMENT "状态（0 离线  1在线）" AFTER relate_park_num;');
CALL add_element_unless_exists('column', 'node_device', 'congestion_status', 'ALTER TABLE node_device ADD COLUMN `congestion_status` int(11) DEFAULT NULL COMMENT "区域相机拥堵状态（0 不拥堵   1 拥堵）" AFTER status;');
CALL add_element_unless_exists('column', 'node_device', 'online_start_time', 'ALTER TABLE node_device ADD COLUMN `online_start_time` datetime DEFAULT NULL COMMENT "最近一次在线开始时间" AFTER congestion_status;');
CALL add_element_unless_exists('column', 'node_device', 'remark', 'ALTER TABLE node_device ADD COLUMN `remark` varchar(255) DEFAULT NULL COMMENT "备注" AFTER online_start_time;');
CALL add_element_unless_exists('column', 'node_device', 'type', 'ALTER TABLE node_device ADD COLUMN `type` int(11) DEFAULT NULL COMMENT "用于区分节点设备和区域设备， 1：节点设备、  2： 区域设备 " AFTER remark;');
CALL add_element_unless_exists('column', 'node_device', 'create_time', 'ALTER TABLE node_device ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER type;');
CALL add_element_unless_exists('column', 'node_device', 'creator', 'ALTER TABLE node_device ADD COLUMN `creator` varchar(255) DEFAULT NULL COMMENT "创建人" AFTER create_time;');
CALL add_element_unless_exists('column', 'node_device', 'update_time', 'ALTER TABLE node_device ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'node_device', 'updater', 'ALTER TABLE node_device ADD COLUMN `updater` varchar(255) DEFAULT NULL COMMENT "最近一次更新人" AFTER update_time;');
CALL add_element_unless_exists('column', 'node_device', 'deleted', 'ALTER TABLE node_device ADD COLUMN `deleted` int(11) DEFAULT "0" COMMENT "是否删除  0：未删除、  1：已删除" AFTER updater;');
CALL add_element_unless_exists('column', 'node_device', 'floor_id', 'ALTER TABLE node_device ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER deleted;');

-- 更新表 node_device_relate 所有字段和索引
ALTER TABLE node_device_relate CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE node_device_relate COMMENT = '区域设备与区域的关系表';
CALL add_element_unless_exists('column', 'node_device_relate', 'id', 'ALTER TABLE node_device_relate ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'node_device_relate', 'area_device_id', 'ALTER TABLE node_device_relate ADD COLUMN `area_device_id` int(11) DEFAULT NULL COMMENT "区域设备id  node_device表的id" AFTER id;');
CALL add_element_unless_exists('column', 'node_device_relate', 'floor_id', 'ALTER TABLE node_device_relate ADD COLUMN `floor_id` int(11) DEFAULT NULL COMMENT "楼层id" AFTER area_device_id;');
CALL add_element_unless_exists('column', 'node_device_relate', 'area_id', 'ALTER TABLE node_device_relate ADD COLUMN `area_id` int(11) DEFAULT NULL COMMENT "区域id" AFTER floor_id;');
CALL add_element_unless_exists('column', 'node_device_relate', 'entrance_exit', 'ALTER TABLE node_device_relate ADD COLUMN `entrance_exit` tinyint(4) DEFAULT NULL COMMENT "相机放置类型  1：入口   2：出口   3：出入口" AFTER area_id;');
CALL add_element_unless_exists('column', 'node_device_relate', 'entrance_exit_name', 'ALTER TABLE node_device_relate ADD COLUMN `entrance_exit_name` varchar(255) DEFAULT NULL COMMENT "枚举类型：  入口   出口  出入口" AFTER entrance_exit;');

-- 更新表 parking_light_area_relation 所有字段和索引
ALTER TABLE parking_light_area_relation CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE parking_light_area_relation COMMENT = '车位灯方案和区域的关系表';
CALL add_element_unless_exists('column', 'parking_light_area_relation', 'id', 'ALTER TABLE parking_light_area_relation ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'parking_light_area_relation', 'parking_light_scheme_id', 'ALTER TABLE parking_light_area_relation ADD COLUMN `parking_light_scheme_id` int(11) DEFAULT NULL COMMENT "车位灯方案id" AFTER id;');
CALL add_element_unless_exists('column', 'parking_light_area_relation', 'area_id', 'ALTER TABLE parking_light_area_relation ADD COLUMN `area_id` int(11) DEFAULT NULL COMMENT "区域id" AFTER parking_light_scheme_id;');
CALL add_element_unless_exists('column', 'parking_light_area_relation', 'area_name', 'ALTER TABLE parking_light_area_relation ADD COLUMN `area_name` varchar(64) DEFAULT NULL COMMENT "区域名称" AFTER area_id;');
CALL add_element_unless_exists('column', 'parking_light_area_relation', 'create_time', 'ALTER TABLE parking_light_area_relation ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER area_name;');
CALL add_element_unless_exists('column', 'parking_light_area_relation', 'creator', 'ALTER TABLE parking_light_area_relation ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'parking_light_area_relation', 'update_time', 'ALTER TABLE parking_light_area_relation ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'parking_light_area_relation', 'updater', 'ALTER TABLE parking_light_area_relation ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'parking_light_area_relation', 'index_area_id', 'ALTER TABLE parking_light_area_relation ADD INDEX index_area_id (area_id) USING BTREE');
CALL add_element_unless_exists('index', 'parking_light_area_relation', 'index_parking_light_scheme_id', 'ALTER TABLE parking_light_area_relation ADD INDEX index_parking_light_scheme_id (parking_light_scheme_id) USING BTREE');

-- 更新表 parking_light_scheme 所有字段和索引
ALTER TABLE parking_light_scheme CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE parking_light_scheme COMMENT = '车位灯方案';
CALL add_element_unless_exists('column', 'parking_light_scheme', 'id', 'ALTER TABLE parking_light_scheme ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'name', 'ALTER TABLE parking_light_scheme ADD COLUMN `name` varchar(255) DEFAULT "" COMMENT "名称" AFTER id;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'lot_id', 'ALTER TABLE parking_light_scheme ADD COLUMN `lot_id` int(11) DEFAULT NULL COMMENT "车场id" AFTER name;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'occupy_color', 'ALTER TABLE parking_light_scheme ADD COLUMN `occupy_color` tinyint(4) DEFAULT "0" COMMENT "占用颜色" AFTER lot_id;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'free_color', 'ALTER TABLE parking_light_scheme ADD COLUMN `free_color` tinyint(4) DEFAULT "0" COMMENT "空闲颜色" AFTER occupy_color;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'warning_color', 'ALTER TABLE parking_light_scheme ADD COLUMN `warning_color` tinyint(4) DEFAULT "0" COMMENT "告警颜色" AFTER free_color;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'type', 'ALTER TABLE parking_light_scheme ADD COLUMN `type` tinyint(4) DEFAULT NULL COMMENT "设备类型  0-DSP车位相机   1-NODE节点控制器" AFTER warning_color;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'light_type', 'ALTER TABLE parking_light_scheme ADD COLUMN `light_type` tinyint(4) DEFAULT "1" COMMENT "灯类型   1-有线多彩灯  2-有线双色灯" AFTER type;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'deleted', 'ALTER TABLE parking_light_scheme ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除0未删除1已删除" AFTER light_type;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'create_time', 'ALTER TABLE parking_light_scheme ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'creator', 'ALTER TABLE parking_light_scheme ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'update_time', 'ALTER TABLE parking_light_scheme ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'updater', 'ALTER TABLE parking_light_scheme ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'custom_occupy_color', 'ALTER TABLE parking_light_scheme ADD COLUMN `custom_occupy_color` varchar(32) DEFAULT NULL COMMENT "自定义占用颜色" AFTER updater;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'custom_warning_color', 'ALTER TABLE parking_light_scheme ADD COLUMN `custom_warning_color` varchar(32) DEFAULT NULL COMMENT "自定义告警颜色" AFTER custom_occupy_color;');
CALL add_element_unless_exists('column', 'parking_light_scheme', 'custom_free_color', 'ALTER TABLE parking_light_scheme ADD COLUMN `custom_free_color` varchar(32) DEFAULT NULL COMMENT "自定义空闲颜色" AFTER custom_warning_color;');

-- 更新表 permissions 所有字段和索引
ALTER TABLE permissions CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE permissions COMMENT = '权限';
CALL add_element_unless_exists('column', 'permissions', 'id', 'ALTER TABLE permissions ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'permissions', 'name', 'ALTER TABLE permissions ADD COLUMN `name` varchar(255) DEFAULT NULL COMMENT "名称" AFTER id;');
CALL add_element_unless_exists('column', 'permissions', 'router', 'ALTER TABLE permissions ADD COLUMN `router` varchar(255) DEFAULT NULL COMMENT "路由" AFTER name;');
CALL add_element_unless_exists('column', 'permissions', 'type', 'ALTER TABLE permissions ADD COLUMN `type` tinyint(4) DEFAULT NULL COMMENT "权限类型 1:菜单 2:权限抽象功能 3:按钮 4:普通接口 5:基础权限接口（所有角色都可以访问） " AFTER router;');
CALL add_element_unless_exists('column', 'permissions', 'icon', 'ALTER TABLE permissions ADD COLUMN `icon` varchar(255) DEFAULT NULL COMMENT "图标" AFTER type;');
CALL add_element_unless_exists('column', 'permissions', 'permission_code', 'ALTER TABLE permissions ADD COLUMN `permission_code` varchar(255) DEFAULT NULL COMMENT "权限标识 " AFTER icon;');
CALL add_element_unless_exists('column', 'permissions', 'internationalization_code', 'ALTER TABLE permissions ADD COLUMN `internationalization_code` varchar(255) DEFAULT NULL COMMENT "国际化code" AFTER permission_code;');
CALL add_element_unless_exists('column', 'permissions', 'parent_id', 'ALTER TABLE permissions ADD COLUMN `parent_id` int(11) DEFAULT NULL COMMENT "父权限id" AFTER internationalization_code;');
CALL add_element_unless_exists('column', 'permissions', 'status', 'ALTER TABLE permissions ADD COLUMN `status` tinyint(4) DEFAULT NULL COMMENT "开关（1开0关）" AFTER parent_id;');
CALL add_element_unless_exists('column', 'permissions', 'sort', 'ALTER TABLE permissions ADD COLUMN `sort` int(11) DEFAULT "0" COMMENT "排序字段" AFTER status;');
CALL add_element_unless_exists('column', 'permissions', 'deleted', 'ALTER TABLE permissions ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除 0未删除 1已删除" AFTER sort;');
CALL add_element_unless_exists('column', 'permissions', 'create_time', 'ALTER TABLE permissions ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'permissions', 'creator', 'ALTER TABLE permissions ADD COLUMN `creator` varchar(255) DEFAULT NULL COMMENT "创建时间" AFTER create_time;');
CALL add_element_unless_exists('column', 'permissions', 'update_time', 'ALTER TABLE permissions ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'permissions', 'updator', 'ALTER TABLE permissions ADD COLUMN `updator` varchar(255) DEFAULT NULL COMMENT "更新人" AFTER update_time;');

-- 更新表 role 所有字段和索引
ALTER TABLE role CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE role COMMENT = '角色';
CALL add_element_unless_exists('column', 'role', 'id', 'ALTER TABLE role ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'role', 'name', 'ALTER TABLE role ADD COLUMN `name` varchar(255) DEFAULT NULL COMMENT "角色名称" AFTER id;');
CALL add_element_unless_exists('column', 'role', 'description', 'ALTER TABLE role ADD COLUMN `description` varchar(255) DEFAULT NULL COMMENT "备注" AFTER name;');
CALL add_element_unless_exists('column', 'role', 'enable', 'ALTER TABLE role ADD COLUMN `enable` tinyint(1) DEFAULT "0" COMMENT "启用状态  1：启用  0：禁用" AFTER description;');
CALL add_element_unless_exists('column', 'role', 'deleted', 'ALTER TABLE role ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "删除状态  1：已删除  0：未删除" AFTER enable;');
CALL add_element_unless_exists('column', 'role', 'create_time', 'ALTER TABLE role ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'role', 'creator', 'ALTER TABLE role ADD COLUMN `creator` varchar(50) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'role', 'update_time', 'ALTER TABLE role ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'role', 'updater', 'ALTER TABLE role ADD COLUMN `updater` varchar(50) DEFAULT NULL COMMENT "更新者" AFTER update_time;');

-- 更新表 role_permission_relation 所有字段和索引
ALTER TABLE role_permission_relation CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE role_permission_relation COMMENT = '角色权限关系表';
CALL add_element_unless_exists('column', 'role_permission_relation', 'id', 'ALTER TABLE role_permission_relation ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'role_permission_relation', 'role_id', 'ALTER TABLE role_permission_relation ADD COLUMN `role_id` int(11) DEFAULT NULL COMMENT "角色id" AFTER id;');
CALL add_element_unless_exists('column', 'role_permission_relation', 'permission_id', 'ALTER TABLE role_permission_relation ADD COLUMN `permission_id` int(11) DEFAULT NULL COMMENT "权限id" AFTER role_id;');
CALL add_element_unless_exists('column', 'role_permission_relation', 'create_time', 'ALTER TABLE role_permission_relation ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER permission_id;');
CALL add_element_unless_exists('column', 'role_permission_relation', 'creator', 'ALTER TABLE role_permission_relation ADD COLUMN `creator` varchar(50) DEFAULT NULL COMMENT "创建者" AFTER create_time;');

-- 更新表 schedule_config 所有字段和索引
ALTER TABLE schedule_config CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE schedule_config COMMENT = '参数配置表';
CALL add_element_unless_exists('column', 'schedule_config', 'id', 'ALTER TABLE schedule_config ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'schedule_config', 'create_time', 'ALTER TABLE schedule_config ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "更新时间" AFTER id;');
CALL add_element_unless_exists('column', 'schedule_config', 'update_time', 'ALTER TABLE schedule_config ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER create_time;');
CALL add_element_unless_exists('column', 'schedule_config', 'park_img_duration', 'ALTER TABLE schedule_config ADD COLUMN `park_img_duration` int(11) DEFAULT NULL COMMENT "车位照片定时清理" AFTER update_time;');
CALL add_element_unless_exists('column', 'schedule_config', 'area_park_img_duration', 'ALTER TABLE schedule_config ADD COLUMN `area_park_img_duration` int(11) DEFAULT NULL COMMENT "区域在场车辆定时清理" AFTER park_img_duration;');
CALL add_element_unless_exists('column', 'schedule_config', 'in_car_push_switch', 'ALTER TABLE schedule_config ADD COLUMN `in_car_push_switch` tinyint(1) DEFAULT "0" COMMENT "车位入车延迟上报，0开启，1关闭" AFTER area_park_img_duration;');
CALL add_element_unless_exists('column', 'schedule_config', 'out_car_push_switch', 'ALTER TABLE schedule_config ADD COLUMN `out_car_push_switch` tinyint(1) DEFAULT "0" COMMENT "车位出车延迟上报，0开启，1关闭" AFTER in_car_push_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'update_plate_push_switch', 'ALTER TABLE schedule_config ADD COLUMN `update_plate_push_switch` tinyint(1) DEFAULT "1" COMMENT "更新车牌上报，0开启，1关闭" AFTER out_car_push_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'empty_park_push_switch', 'ALTER TABLE schedule_config ADD COLUMN `empty_park_push_switch` tinyint(1) DEFAULT NULL COMMENT "空车位上报，0开启，1关闭" AFTER update_plate_push_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'empty_park_push_lot', 'ALTER TABLE schedule_config ADD COLUMN `empty_park_push_lot` varchar(255) DEFAULT NULL COMMENT "空车位上报车场id" AFTER empty_park_push_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'empty_park_push_url', 'ALTER TABLE schedule_config ADD COLUMN `empty_park_push_url` varchar(2000) DEFAULT NULL COMMENT "空车位上报url  多个url直接用英语逗号隔开" AFTER empty_park_push_lot;');
CALL add_element_unless_exists('column', 'schedule_config', 'park_change_push_switch', 'ALTER TABLE schedule_config ADD COLUMN `park_change_push_switch` tinyint(1) DEFAULT NULL COMMENT "车位状态变更上报" AFTER empty_park_push_url;');
CALL add_element_unless_exists('column', 'schedule_config', 'park_change_push_lot', 'ALTER TABLE schedule_config ADD COLUMN `park_change_push_lot` varchar(255) DEFAULT NULL COMMENT "车位状态变更上报车场id" AFTER park_change_push_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'park_change_push_url', 'ALTER TABLE schedule_config ADD COLUMN `park_change_push_url` varchar(2000) DEFAULT NULL COMMENT "车位状态变更上报url  多个url直接用英语逗号隔开" AFTER park_change_push_lot;');
CALL add_element_unless_exists('column', 'schedule_config', 'creator', 'ALTER TABLE schedule_config ADD COLUMN `creator` varchar(255) DEFAULT NULL COMMENT "更新者" AFTER park_change_push_url;');
CALL add_element_unless_exists('column', 'schedule_config', 'url_prefix_config', 'ALTER TABLE schedule_config ADD COLUMN `url_prefix_config` varchar(255) DEFAULT NULL COMMENT "单车场查询返回图片URL拼接前缀地址" AFTER creator;');
CALL add_element_unless_exists('column', 'schedule_config', 'free_space_num_switch', 'ALTER TABLE schedule_config ADD COLUMN `free_space_num_switch` tinyint(1) DEFAULT "1" COMMENT "实时剩余车位数本地文件对接开关，0开启，1关闭" AFTER url_prefix_config;');
CALL add_element_unless_exists('column', 'schedule_config', 'image_upload_switch', 'ALTER TABLE schedule_config ADD COLUMN `image_upload_switch` tinyint(1) DEFAULT "0" COMMENT "图片上传OSS开关(0:开启,1:关闭)" AFTER free_space_num_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'unified_image_prefix', 'ALTER TABLE schedule_config ADD COLUMN `unified_image_prefix` varchar(255) DEFAULT NULL COMMENT "统一接口查询返回图片URL前缀" AFTER image_upload_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'post_bus_in_out', 'ALTER TABLE schedule_config ADD COLUMN `post_bus_in_out` tinyint(1) DEFAULT "1" COMMENT "上报出入车 0:开启  1:关闭" AFTER unified_image_prefix;');
CALL add_element_unless_exists('column', 'schedule_config', 'post_node_device_status', 'ALTER TABLE schedule_config ADD COLUMN `post_node_device_status` tinyint(1) DEFAULT "1" COMMENT "节点设备状态变更上报 0:开启  1:关闭" AFTER post_bus_in_out;');
CALL add_element_unless_exists('column', 'schedule_config', 'clean_stereoscopic_park_switch', 'ALTER TABLE schedule_config ADD COLUMN `clean_stereoscopic_park_switch` tinyint(1) DEFAULT "1" COMMENT "定时清理立体车位的车牌识别记录 0:开启  1:关闭" AFTER post_node_device_status;');
CALL add_element_unless_exists('column', 'schedule_config', 'free_space_switch', 'ALTER TABLE schedule_config ADD COLUMN `free_space_switch` tinyint(1) DEFAULT "1" COMMENT "剩余车位数上报收费系统开关 0:开启  1:关闭" AFTER clean_stereoscopic_park_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'post_node_device_url', 'ALTER TABLE schedule_config ADD COLUMN `post_node_device_url` varchar(2000) DEFAULT NULL COMMENT "节点设备状态变更上报url  多个url直接用英语逗号隔开" AFTER free_space_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'clean_stereoscopic_park_duration', 'ALTER TABLE schedule_config ADD COLUMN `clean_stereoscopic_park_duration` int(11) DEFAULT NULL COMMENT "清理立体车位的车牌识别记录(天)" AFTER post_node_device_url;');
CALL add_element_unless_exists('column', 'schedule_config', 'car_loc_info_switch', 'ALTER TABLE schedule_config ADD COLUMN `car_loc_info_switch` tinyint(1) DEFAULT "1" COMMENT "车辆停放位置查询接口开关 0:开启  1:关闭" AFTER clean_stereoscopic_park_duration;');
CALL add_element_unless_exists('column', 'schedule_config', 'area_push_switch', 'ALTER TABLE schedule_config ADD COLUMN `area_push_switch` tinyint(1) DEFAULT "1" COMMENT "区域进出车上报开关 0:开启  1:关闭" AFTER car_loc_info_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'tank_warn_push_switch', 'ALTER TABLE schedule_config ADD COLUMN `tank_warn_push_switch` tinyint(1) DEFAULT "1" COMMENT "油车告警上报开关 0:开启  1:关闭" AFTER area_push_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'light_scheme_duration', 'ALTER TABLE schedule_config ADD COLUMN `light_scheme_duration` int(11) DEFAULT "60" COMMENT "车位灯方案删除 " AFTER tank_warn_push_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'grpc_switch', 'ALTER TABLE schedule_config ADD COLUMN `grpc_switch` tinyint(1) DEFAULT "1" COMMENT "gRPC连接云端C++用于统一接口开关 0:开启  1:关闭" AFTER light_scheme_duration;');
CALL add_element_unless_exists('column', 'schedule_config', 'screen_cmd_interval', 'ALTER TABLE schedule_config ADD COLUMN `screen_cmd_interval` int(11) DEFAULT "30" COMMENT "屏指令下发间隔时间（低频），默认30分钟" AFTER grpc_switch;');
CALL add_element_unless_exists('column', 'schedule_config', 'screen_cmd_interval_fast', 'ALTER TABLE schedule_config ADD COLUMN `screen_cmd_interval_fast` int(11) NOT NULL DEFAULT "8" COMMENT "屏指令下发间隔时间（高频），默认8秒钟" AFTER screen_cmd_interval;');
CALL add_element_unless_exists('column', 'schedule_config', 'statistic_screen_type', 'ALTER TABLE schedule_config ADD COLUMN `statistic_screen_type` tinyint(4) NOT NULL DEFAULT "1" COMMENT "统计屏数据方式  0=定时统计 1=进出车触发 " AFTER screen_cmd_interval_fast;');
CALL add_element_unless_exists('column', 'schedule_config', 'query_recognize_record', 'ALTER TABLE schedule_config ADD COLUMN `query_recognize_record` tinyint(1) DEFAULT "0" COMMENT "是否查询识别记录 0:开启  1:关闭（开启查询识别记录，关闭查询实时在场车）" AFTER statistic_screen_type;');
CALL add_element_unless_exists('column', 'schedule_config', 'plate_match_rule', 'ALTER TABLE schedule_config ADD COLUMN `plate_match_rule` int(11) DEFAULT "1" COMMENT "车牌匹配规则（0 【完全匹配】只返回除汉字部分完全一致的车牌）;1 【全匹配】 查2222可能返回12222或22221" AFTER query_recognize_record;');
CALL add_element_unless_exists('column', 'schedule_config', 'clean_temp_picture', 'ALTER TABLE schedule_config ADD COLUMN `clean_temp_picture` int(11) DEFAULT "1" COMMENT "清理n天以前的临时识别文件" AFTER plate_match_rule;');
CALL add_element_unless_exists('column', 'schedule_config', 'clean_recognition_table', 'ALTER TABLE schedule_config ADD COLUMN `clean_recognition_table` int(11) DEFAULT "30" COMMENT "车牌识别日志表定时清理（单位：天）" AFTER clean_temp_picture;');
CALL add_element_unless_exists('column', 'schedule_config', 'clean_area_picture', 'ALTER TABLE schedule_config ADD COLUMN `clean_area_picture` int(11) DEFAULT "1" COMMENT "区域照片文件定时清理（单位：天）" AFTER clean_recognition_table;');
CALL add_element_unless_exists('column', 'schedule_config', 'warn_switch', 'ALTER TABLE schedule_config ADD COLUMN `warn_switch` int(11) NOT NULL DEFAULT "1" COMMENT "告警开关 1=开 0=关" AFTER clean_area_picture;');

-- 更新表 t_access_config 所有字段和索引
ALTER TABLE t_access_config CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE t_access_config COMMENT = 'C++重构配置信息表';
CALL add_element_unless_exists('column', 't_access_config', 'id', 'ALTER TABLE t_access_config ADD COLUMN `id` int(10) unsigned NOT NULL AUTO_INCREMENT" COMMENT "唯一id";');
CALL add_element_unless_exists('column', 't_access_config', 'dsp_port', 'ALTER TABLE t_access_config ADD COLUMN `dsp_port` int(11) DEFAULT NULL COMMENT "dsp 连接端口" AFTER id;');
CALL add_element_unless_exists('column', 't_access_config', 'node_port', 'ALTER TABLE t_access_config ADD COLUMN `node_port` int(11) DEFAULT NULL COMMENT "node tcp节点连接端口" AFTER dsp_port;');
CALL add_element_unless_exists('column', 't_access_config', 'ip_Pre', 'ALTER TABLE t_access_config ADD COLUMN `ip_Pre` varchar(255) DEFAULT NULL COMMENT "tcp地址拼接前缀" AFTER node_port;');
CALL add_element_unless_exists('column', 't_access_config', 'broadcast_times', 'ALTER TABLE t_access_config ADD COLUMN `broadcast_times` int(11) DEFAULT NULL COMMENT "广播次数" AFTER ip_Pre;');
CALL add_element_unless_exists('column', 't_access_config', 'broadcast_interval', 'ALTER TABLE t_access_config ADD COLUMN `broadcast_interval` int(11) DEFAULT NULL COMMENT "播放间隔" AFTER broadcast_times;');
CALL add_element_unless_exists('column', 't_access_config', 'channel_http', 'ALTER TABLE t_access_config ADD COLUMN `channel_http` varchar(255) DEFAULT NULL COMMENT "channel服务url地址" AFTER broadcast_interval;');
CALL add_element_unless_exists('column', 't_access_config', 'serial_port', 'ALTER TABLE t_access_config ADD COLUMN `serial_port` varchar(64) DEFAULT NULL COMMENT "串口地址" AFTER channel_http;');
CALL add_element_unless_exists('column', 't_access_config', 'baud_rate', 'ALTER TABLE t_access_config ADD COLUMN `baud_rate` int(11) DEFAULT NULL COMMENT "波特率" AFTER serial_port;');
CALL add_element_unless_exists('column', 't_access_config', 'A', 'ALTER TABLE t_access_config ADD COLUMN `A` int(11) DEFAULT NULL COMMENT "识别模式A" AFTER baud_rate;');
CALL add_element_unless_exists('column', 't_access_config', 'B', 'ALTER TABLE t_access_config ADD COLUMN `B` int(11) DEFAULT NULL COMMENT "识别模式B" AFTER A;');
CALL add_element_unless_exists('column', 't_access_config', 'C', 'ALTER TABLE t_access_config ADD COLUMN `C` int(11) DEFAULT NULL COMMENT "识别模式C" AFTER B;');
CALL add_element_unless_exists('column', 't_access_config', 'pr_num', 'ALTER TABLE t_access_config ADD COLUMN `pr_num` int(11) DEFAULT NULL COMMENT "车牌类型长度" AFTER C;');
CALL add_element_unless_exists('column', 't_access_config', 'army_car', 'ALTER TABLE t_access_config ADD COLUMN `army_car` int(11) DEFAULT NULL COMMENT "军车车牌" AFTER pr_num;');
CALL add_element_unless_exists('column', 't_access_config', 'police_car', 'ALTER TABLE t_access_config ADD COLUMN `police_car` int(11) DEFAULT NULL COMMENT "警车车牌" AFTER army_car;');
CALL add_element_unless_exists('column', 't_access_config', 'wujing_car', 'ALTER TABLE t_access_config ADD COLUMN `wujing_car` int(11) DEFAULT NULL COMMENT "武警车牌" AFTER police_car;');
CALL add_element_unless_exists('column', 't_access_config', 'farm_car', 'ALTER TABLE t_access_config ADD COLUMN `farm_car` int(11) DEFAULT NULL COMMENT "农用车牌" AFTER wujing_car;');
CALL add_element_unless_exists('column', 't_access_config', 'embassy_car', 'ALTER TABLE t_access_config ADD COLUMN `embassy_car` int(11) DEFAULT NULL COMMENT "大使馆车牌" AFTER farm_car;');
CALL add_element_unless_exists('column', 't_access_config', 'personality_car', 'ALTER TABLE t_access_config ADD COLUMN `personality_car` int(11) DEFAULT NULL COMMENT "个性化车牌" AFTER embassy_car;');
CALL add_element_unless_exists('column', 't_access_config', 'civil_car', 'ALTER TABLE t_access_config ADD COLUMN `civil_car` int(11) DEFAULT NULL COMMENT "民航车牌" AFTER personality_car;');
CALL add_element_unless_exists('column', 't_access_config', 'new_energy_car', 'ALTER TABLE t_access_config ADD COLUMN `new_energy_car` int(11) DEFAULT NULL COMMENT "新能源车牌" AFTER civil_car;');
CALL add_element_unless_exists('column', 't_access_config', 'type_pr_num', 'ALTER TABLE t_access_config ADD COLUMN `type_pr_num` int(11) DEFAULT NULL COMMENT "车牌长度" AFTER new_energy_car;');
CALL add_element_unless_exists('column', 't_access_config', 'set_lr_num', 'ALTER TABLE t_access_config ADD COLUMN `set_lr_num` int(11) DEFAULT NULL COMMENT "车牌数组长度" AFTER type_pr_num;');
CALL add_element_unless_exists('column', 't_access_config', 'set_lpr_cs', 'ALTER TABLE t_access_config ADD COLUMN `set_lpr_cs` int(11) DEFAULT NULL COMMENT "识别种类（0:裁剪，1：A版，2：B版，3：A+B版，4：C版 5：A+C版，6：B+C，7：A+B+C）" AFTER set_lr_num;');
CALL add_element_unless_exists('column', 't_access_config', 'province', 'ALTER TABLE t_access_config ADD COLUMN `province` varchar(12) DEFAULT NULL COMMENT "默认省份" AFTER set_lpr_cs;');
CALL add_element_unless_exists('column', 't_access_config', 'set_priority', 'ALTER TABLE t_access_config ADD COLUMN `set_priority` int(11) DEFAULT "0" COMMENT "设置三地车牌输出优先级:1:MO 2:HK 3:CN 4:CN>HK>MO 5:MO>CN>HK 6:MO>HK>CN 7:HK>CN>MO 8:HK>MO>CN other:CN>MO>HK" AFTER province;');
CALL add_element_unless_exists('column', 't_access_config', 'original_picture_path', 'ALTER TABLE t_access_config ADD COLUMN `original_picture_path` varchar(255) DEFAULT NULL COMMENT "原图保存路径" AFTER set_priority;');
CALL add_element_unless_exists('column', 't_access_config', 'front_save_path', 'ALTER TABLE t_access_config ADD COLUMN `front_save_path` varchar(255) DEFAULT NULL COMMENT "前端保存路径" AFTER original_picture_path;');
CALL add_element_unless_exists('column', 't_access_config', 'temp_rcv_path', 'ALTER TABLE t_access_config ADD COLUMN `temp_rcv_path` varchar(255) DEFAULT NULL COMMENT "临时文件路径" AFTER front_save_path;');
CALL add_element_unless_exists('column', 't_access_config', 'recognition_path', 'ALTER TABLE t_access_config ADD COLUMN `recognition_path` varchar(255) DEFAULT NULL COMMENT "识别文件路径" AFTER temp_rcv_path;');
CALL add_element_unless_exists('column', 't_access_config', 'recognition_lib_path', 'ALTER TABLE t_access_config ADD COLUMN `recognition_lib_path` varchar(255) DEFAULT NULL COMMENT "识别库地址" AFTER recognition_path;');
CALL add_element_unless_exists('column', 't_access_config', 'switch_serial_port', 'ALTER TABLE t_access_config ADD COLUMN `switch_serial_port` tinyint(1) DEFAULT "1" COMMENT "485节点串口扫描开关（0：关闭  1：开启）" AFTER recognition_lib_path;');
CALL add_element_unless_exists('column', 't_access_config', 'region_picture_path', 'ALTER TABLE t_access_config ADD COLUMN `region_picture_path` varchar(255) DEFAULT NULL COMMENT "区域相机照片保存路径" AFTER switch_serial_port;');
CALL add_element_unless_exists('column', 't_access_config', 'snap_picture_path', 'ALTER TABLE t_access_config ADD COLUMN `snap_picture_path` varchar(255) DEFAULT NULL COMMENT "相机抓拍照片保存路径" AFTER region_picture_path;');
CALL add_element_unless_exists('column', 't_access_config', 'quality_inspection_picture_path', 'ALTER TABLE t_access_config ADD COLUMN `quality_inspection_picture_path` varchar(255) DEFAULT NULL COMMENT "质检中心抓拍照片保存路径" AFTER snap_picture_path;');
CALL add_element_unless_exists('column', 't_access_config', 'recognition_switch', 'ALTER TABLE t_access_config ADD COLUMN `recognition_switch` tinyint(1) DEFAULT "1" COMMENT "识别库开关，0:关闭 1:开启" AFTER quality_inspection_picture_path;');
CALL add_element_unless_exists('column', 't_access_config', 'free_occupy_switch', 'ALTER TABLE t_access_config ADD COLUMN `free_occupy_switch` tinyint(1) DEFAULT "0" COMMENT "找车系统-有车 和找车系统-无车数据接口上报开关 (0：关闭，1：开启)" AFTER recognition_switch;');

-- 更新表 t_car_in_out_statistics 所有字段和索引
ALTER TABLE t_car_in_out_statistics CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE t_car_in_out_statistics COMMENT = '出入车流量统计';
CALL add_element_unless_exists('column', 't_car_in_out_statistics', 'id', 'ALTER TABLE t_car_in_out_statistics ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 't_car_in_out_statistics', 'floor_id', 'ALTER TABLE t_car_in_out_statistics ADD COLUMN `floor_id` int(11) NOT NULL COMMENT "楼层id" AFTER id;');
CALL add_element_unless_exists('column', 't_car_in_out_statistics', 'floor_name', 'ALTER TABLE t_car_in_out_statistics ADD COLUMN `floor_name` varchar(64) DEFAULT NULL COMMENT "楼层名称" AFTER floor_id;');
CALL add_element_unless_exists('column', 't_car_in_out_statistics', 'general_num', 'ALTER TABLE t_car_in_out_statistics ADD COLUMN `general_num` int(11) DEFAULT "0" COMMENT "普通车数量" AFTER floor_name;');
CALL add_element_unless_exists('column', 't_car_in_out_statistics', 'energy_num', 'ALTER TABLE t_car_in_out_statistics ADD COLUMN `energy_num` int(11) DEFAULT "0" COMMENT "新能源车数量" AFTER general_num;');
CALL add_element_unless_exists('column', 't_car_in_out_statistics', 'record_start_time', 'ALTER TABLE t_car_in_out_statistics ADD COLUMN `record_start_time` datetime DEFAULT NULL COMMENT "记录开始时间" AFTER energy_num;');
CALL add_element_unless_exists('column', 't_car_in_out_statistics', 'record_end_time', 'ALTER TABLE t_car_in_out_statistics ADD COLUMN `record_end_time` datetime DEFAULT NULL COMMENT "记录结束时间" AFTER record_start_time;');
CALL add_element_unless_exists('column', 't_car_in_out_statistics', 'type', 'ALTER TABLE t_car_in_out_statistics ADD COLUMN `type` tinyint(4) DEFAULT "1" COMMENT "统计类型:入车-1 出车-0" AFTER record_end_time;');
CALL add_element_unless_exists('column', 't_car_in_out_statistics', 'create_time', 'ALTER TABLE t_car_in_out_statistics ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER type;');
CALL add_element_unless_exists('column', 't_car_in_out_statistics', 'creator', 'ALTER TABLE t_car_in_out_statistics ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 't_car_in_out_statistics', 'update_time', 'ALTER TABLE t_car_in_out_statistics ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 't_car_in_out_statistics', 'updater', 'ALTER TABLE t_car_in_out_statistics ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 't_car_in_out_statistics', 'idx_record_time', 'ALTER TABLE t_car_in_out_statistics ADD INDEX idx_record_time (record_end_time) USING BTREE');

-- 更新表 t_login_log 所有字段和索引
ALTER TABLE t_login_log CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE t_login_log COMMENT = '登陆日志表';
CALL add_element_unless_exists('column', 't_login_log', 'id', 'ALTER TABLE t_login_log ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 't_login_log', 'user_name', 'ALTER TABLE t_login_log ADD COLUMN `user_name` varchar(64) DEFAULT "" COMMENT "用户名" AFTER id;');
CALL add_element_unless_exists('column', 't_login_log', 'user_account', 'ALTER TABLE t_login_log ADD COLUMN `user_account` varchar(64) DEFAULT "" COMMENT "用户账号" AFTER user_name;');
CALL add_element_unless_exists('column', 't_login_log', 'user_phone', 'ALTER TABLE t_login_log ADD COLUMN `user_phone` varchar(64) DEFAULT "" COMMENT "用户电话" AFTER user_account;');
CALL add_element_unless_exists('column', 't_login_log', 'login_ip', 'ALTER TABLE t_login_log ADD COLUMN `login_ip` varchar(64) DEFAULT "" COMMENT "登陆ip" AFTER user_phone;');
CALL add_element_unless_exists('column', 't_login_log', 'login_time', 'ALTER TABLE t_login_log ADD COLUMN `login_time` datetime DEFAULT NULL COMMENT "登陆时间" AFTER login_ip;');
CALL add_element_unless_exists('column', 't_login_log', 'type', 'ALTER TABLE t_login_log ADD COLUMN `type` tinyint(4) DEFAULT "0" COMMENT "类型 0-登陆" AFTER login_time;');
CALL add_element_unless_exists('column', 't_login_log', 'create_time', 'ALTER TABLE t_login_log ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER type;');
CALL add_element_unless_exists('column', 't_login_log', 'creator', 'ALTER TABLE t_login_log ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 't_login_log', 'update_time', 'ALTER TABLE t_login_log ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 't_login_log', 'updater', 'ALTER TABLE t_login_log ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 't_login_log', 'idx_user_account', 'ALTER TABLE t_login_log ADD INDEX idx_user_account (user_account) USING BTREE');
CALL add_element_unless_exists('index', 't_login_log', 'idx_user_name', 'ALTER TABLE t_login_log ADD INDEX idx_user_name (user_name) USING BTREE');

-- 更新表 t_server_log 所有字段和索引
ALTER TABLE t_server_log CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE t_server_log COMMENT = '服务日志表';
CALL add_element_unless_exists('column', 't_server_log', 'id', 'ALTER TABLE t_server_log ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 't_server_log', 'file_name', 'ALTER TABLE t_server_log ADD COLUMN `file_name` varchar(64) DEFAULT "" COMMENT "文件名" AFTER id;');
CALL add_element_unless_exists('column', 't_server_log', 'file_path', 'ALTER TABLE t_server_log ADD COLUMN `file_path` varchar(255) DEFAULT "" COMMENT "文件路径" AFTER file_name;');
CALL add_element_unless_exists('column', 't_server_log', 'type', 'ALTER TABLE t_server_log ADD COLUMN `type` tinyint(4) DEFAULT "0" COMMENT "类型 0-管理后台" AFTER file_path;');
CALL add_element_unless_exists('column', 't_server_log', 'log_time', 'ALTER TABLE t_server_log ADD COLUMN `log_time` datetime DEFAULT NULL COMMENT "日志时间" AFTER type;');
CALL add_element_unless_exists('column', 't_server_log', 'create_time', 'ALTER TABLE t_server_log ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER log_time;');
CALL add_element_unless_exists('column', 't_server_log', 'creator', 'ALTER TABLE t_server_log ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 't_server_log', 'update_time', 'ALTER TABLE t_server_log ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 't_server_log', 'updater', 'ALTER TABLE t_server_log ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 't_server_log', 'idx_file_name', 'ALTER TABLE t_server_log ADD INDEX idx_file_name (file_name) USING BTREE');
CALL add_element_unless_exists('index', 't_server_log', 'idx_log_time', 'ALTER TABLE t_server_log ADD INDEX idx_log_time (log_time) USING BTREE');

-- 更新表 user 所有字段和索引
ALTER TABLE user CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE user COMMENT = '用户';
CALL add_element_unless_exists('column', 'user', 'id', 'ALTER TABLE user ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键id";');
CALL add_element_unless_exists('column', 'user', 'name', 'ALTER TABLE user ADD COLUMN `name` varchar(50) DEFAULT NULL COMMENT "用户名" AFTER id;');
CALL add_element_unless_exists('column', 'user', 'account', 'ALTER TABLE user ADD COLUMN `account` varchar(50) DEFAULT NULL COMMENT "账号" AFTER name;');
CALL add_element_unless_exists('column', 'user', 'password', 'ALTER TABLE user ADD COLUMN `password` varchar(500) DEFAULT NULL COMMENT "密码" AFTER account;');
CALL add_element_unless_exists('column', 'user', 'phone', 'ALTER TABLE user ADD COLUMN `phone` varchar(11) DEFAULT NULL COMMENT "手机号" AFTER password;');
CALL add_element_unless_exists('column', 'user', 'remark', 'ALTER TABLE user ADD COLUMN `remark` varchar(200) DEFAULT NULL COMMENT "备注" AFTER phone;');
CALL add_element_unless_exists('column', 'user', 'status', 'ALTER TABLE user ADD COLUMN `status` tinyint(1) DEFAULT "1" COMMENT "状态 1 启用  0 禁用" AFTER remark;');
CALL add_element_unless_exists('column', 'user', 'user_type', 'ALTER TABLE user ADD COLUMN `user_type` tinyint(4) DEFAULT "2" COMMENT "用户类型  1 超级管理员  2 普通用户" AFTER status;');
CALL add_element_unless_exists('column', 'user', 'role_id', 'ALTER TABLE user ADD COLUMN `role_id` int(11) DEFAULT NULL COMMENT "角色id （一个用户只对应一个角色）" AFTER user_type;');
CALL add_element_unless_exists('column', 'user', 'wrong_password_count', 'ALTER TABLE user ADD COLUMN `wrong_password_count` int(11) DEFAULT "0" COMMENT "密码错误次数" AFTER role_id;');
CALL add_element_unless_exists('column', 'user', 'locked', 'ALTER TABLE user ADD COLUMN `locked` tinyint(1) DEFAULT "0" COMMENT "账号是否被锁定  1：是  0：否" AFTER wrong_password_count;');
CALL add_element_unless_exists('column', 'user', 'lock_start_time', 'ALTER TABLE user ADD COLUMN `lock_start_time` datetime DEFAULT NULL COMMENT "锁定开始时间" AFTER locked;');
CALL add_element_unless_exists('column', 'user', 'unlock_time', 'ALTER TABLE user ADD COLUMN `unlock_time` datetime DEFAULT NULL COMMENT "解锁时间" AFTER lock_start_time;');
CALL add_element_unless_exists('column', 'user', 'deleted', 'ALTER TABLE user ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除 0 未删除 1已删除" AFTER unlock_time;');
CALL add_element_unless_exists('column', 'user', 'creator', 'ALTER TABLE user ADD COLUMN `creator` varchar(64) DEFAULT NULL COMMENT "创建者" AFTER deleted;');
CALL add_element_unless_exists('column', 'user', 'create_time', 'ALTER TABLE user ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER creator;');
CALL add_element_unless_exists('column', 'user', 'updater', 'ALTER TABLE user ADD COLUMN `updater` varchar(64) DEFAULT NULL COMMENT "更新者" AFTER create_time;');
CALL add_element_unless_exists('column', 'user', 'update_time', 'ALTER TABLE user ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER updater;');
CALL add_element_unless_exists('column', 'user', 'password_record', 'ALTER TABLE user ADD COLUMN `password_record` varchar(255) DEFAULT NULL COMMENT "密码修改信息记录(默认保存最近5条更新数据)" AFTER update_time;');

-- 更新表 warn_illegal_park 所有字段和索引
ALTER TABLE warn_illegal_park CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE warn_illegal_park COMMENT = '车辆违停告警配置';
CALL add_element_unless_exists('column', 'warn_illegal_park', 'id', 'ALTER TABLE warn_illegal_park ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'warn_illegal_park', 'plate_no', 'ALTER TABLE warn_illegal_park ADD COLUMN `plate_no` varchar(50) DEFAULT NULL COMMENT "车牌号" AFTER id;');
CALL add_element_unless_exists('column', 'warn_illegal_park', 'bind_type', 'ALTER TABLE warn_illegal_park ADD COLUMN `bind_type` tinyint(4) DEFAULT NULL COMMENT "绑定类型  1：绑定车位  2：绑定区域" AFTER plate_no;');
CALL add_element_unless_exists('column', 'warn_illegal_park', 'deleted', 'ALTER TABLE warn_illegal_park ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除  0：未删除  1：已删除" AFTER bind_type;');
CALL add_element_unless_exists('column', 'warn_illegal_park', 'create_time', 'ALTER TABLE warn_illegal_park ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'warn_illegal_park', 'creator', 'ALTER TABLE warn_illegal_park ADD COLUMN `creator` varchar(255) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'warn_illegal_park', 'update_time', 'ALTER TABLE warn_illegal_park ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'warn_illegal_park', 'updater', 'ALTER TABLE warn_illegal_park ADD COLUMN `updater` varchar(50) DEFAULT NULL COMMENT "更新者" AFTER update_time;');

-- 更新表 warn_illegal_park_relate 所有字段和索引
ALTER TABLE warn_illegal_park_relate CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE warn_illegal_park_relate COMMENT = '车辆违停告警配置关系表';
CALL add_element_unless_exists('column', 'warn_illegal_park_relate', 'id', 'ALTER TABLE warn_illegal_park_relate ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'warn_illegal_park_relate', 'warn_illegal_park_id', 'ALTER TABLE warn_illegal_park_relate ADD COLUMN `warn_illegal_park_id` int(11) DEFAULT NULL COMMENT "warn_illegal_park表的id" AFTER id;');
CALL add_element_unless_exists('column', 'warn_illegal_park_relate', 'park_area_id', 'ALTER TABLE warn_illegal_park_relate ADD COLUMN `park_area_id` int(11) DEFAULT NULL COMMENT "车位id或者区域id，具体要看绑定类型" AFTER warn_illegal_park_id;');
CALL add_element_unless_exists('column', 'warn_illegal_park_relate', 'create_time', 'ALTER TABLE warn_illegal_park_relate ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER park_area_id;');
CALL add_element_unless_exists('column', 'warn_illegal_park_relate', 'creator', 'ALTER TABLE warn_illegal_park_relate ADD COLUMN `creator` varchar(50) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'warn_illegal_park_relate', 'update_time', 'ALTER TABLE warn_illegal_park_relate ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'warn_illegal_park_relate', 'updater', 'ALTER TABLE warn_illegal_park_relate ADD COLUMN `updater` varchar(50) DEFAULT NULL COMMENT "更新者" AFTER update_time;');

-- 更新表 warn_log 所有字段和索引
ALTER TABLE warn_log CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE warn_log COMMENT = '告警记录';
CALL add_element_unless_exists('column', 'warn_log', 'id', 'ALTER TABLE warn_log ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'warn_log', 'park_id', 'ALTER TABLE warn_log ADD COLUMN `park_id` int(11) DEFAULT NULL COMMENT "车位id" AFTER id;');
CALL add_element_unless_exists('column', 'warn_log', 'park_no', 'ALTER TABLE warn_log ADD COLUMN `park_no` varchar(50) DEFAULT NULL COMMENT "车位编号" AFTER park_id;');
CALL add_element_unless_exists('column', 'warn_log', 'park_plate_no', 'ALTER TABLE warn_log ADD COLUMN `park_plate_no` varchar(50) DEFAULT NULL COMMENT "违停车牌" AFTER park_no;');
CALL add_element_unless_exists('column', 'warn_log', 'bind_plate_no', 'ALTER TABLE warn_log ADD COLUMN `bind_plate_no` varchar(50) DEFAULT NULL COMMENT "绑定车牌" AFTER park_plate_no;');
CALL add_element_unless_exists('column', 'warn_log', 'warn_type', 'ALTER TABLE warn_log ADD COLUMN `warn_type` tinyint(4) DEFAULT NULL COMMENT "告警类型  1：车位占用告警   2：车辆违停告警  3：特殊车辆入车  4：特殊车辆出车  5：车辆压线" AFTER bind_plate_no;');
CALL add_element_unless_exists('column', 'warn_log', 'warn_source', 'ALTER TABLE warn_log ADD COLUMN `warn_source` tinyint(1) NOT NULL DEFAULT "0" COMMENT "告警来源 0-寻车系统 1-第三方" AFTER warn_type;');
CALL add_element_unless_exists('column', 'warn_log', 'bind_park_area', 'ALTER TABLE warn_log ADD COLUMN `bind_park_area` varchar(1024) DEFAULT NULL COMMENT "绑定的车位编号或者区域的名称  多个之间用英语分号隔开" AFTER warn_source;');
CALL add_element_unless_exists('column', 'warn_log', 'park_time', 'ALTER TABLE warn_log ADD COLUMN `park_time` datetime DEFAULT NULL COMMENT "停入时间" AFTER bind_park_area;');
CALL add_element_unless_exists('column', 'warn_log', 'warn_time', 'ALTER TABLE warn_log ADD COLUMN `warn_time` datetime DEFAULT NULL COMMENT "告警时间" AFTER park_time;');
CALL add_element_unless_exists('column', 'warn_log', 'warn_status', 'ALTER TABLE warn_log ADD COLUMN `warn_status` tinyint(4) DEFAULT NULL COMMENT "告警状态  1：告警中  2：手动停止  3：自动停止" AFTER warn_time;');
CALL add_element_unless_exists('column', 'warn_log', 'car_image_url', 'ALTER TABLE warn_log ADD COLUMN `car_image_url` varchar(255) DEFAULT NULL COMMENT "车辆抓拍照片地址" AFTER warn_status;');
CALL add_element_unless_exists('column', 'warn_log', 'present_car_record_id', 'ALTER TABLE warn_log ADD COLUMN `present_car_record_id` int(11) DEFAULT NULL COMMENT "在场车id b_present_car_record表的id 用来标识唯一入车事件" AFTER car_image_url;');
CALL add_element_unless_exists('column', 'warn_log', 'create_time', 'ALTER TABLE warn_log ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER present_car_record_id;');
CALL add_element_unless_exists('column', 'warn_log', 'creator', 'ALTER TABLE warn_log ADD COLUMN `creator` varchar(50) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'warn_log', 'update_time', 'ALTER TABLE warn_log ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'warn_log', 'updater', 'ALTER TABLE warn_log ADD COLUMN `updater` varchar(50) DEFAULT NULL COMMENT "更新者" AFTER update_time;');
CALL add_element_unless_exists('index', 'warn_log', 'idx_park_id', 'ALTER TABLE warn_log ADD INDEX idx_park_id (park_id) USING BTREE');
CALL add_element_unless_exists('index', 'warn_log', 'idx_present_car_record_id', 'ALTER TABLE warn_log ADD INDEX idx_present_car_record_id (present_car_record_id) USING BTREE');

-- 更新表 warn_space_occupy 所有字段和索引
ALTER TABLE warn_space_occupy CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE warn_space_occupy COMMENT = '车位占用告警配置';
CALL add_element_unless_exists('column', 'warn_space_occupy', 'id', 'ALTER TABLE warn_space_occupy ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'warn_space_occupy', 'park_id', 'ALTER TABLE warn_space_occupy ADD COLUMN `park_id` int(11) DEFAULT NULL COMMENT "车位id" AFTER id;');
CALL add_element_unless_exists('column', 'warn_space_occupy', 'plate_no', 'ALTER TABLE warn_space_occupy ADD COLUMN `plate_no` varchar(1024) DEFAULT NULL COMMENT "绑定车牌号，多个车牌号中间用英文分号隔开" AFTER park_id;');
CALL add_element_unless_exists('column', 'warn_space_occupy', 'deleted', 'ALTER TABLE warn_space_occupy ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除  0：未删除  1：已删除" AFTER plate_no;');
CALL add_element_unless_exists('column', 'warn_space_occupy', 'create_time', 'ALTER TABLE warn_space_occupy ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'warn_space_occupy', 'creator', 'ALTER TABLE warn_space_occupy ADD COLUMN `creator` varchar(50) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'warn_space_occupy', 'update_time', 'ALTER TABLE warn_space_occupy ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'warn_space_occupy', 'updater', 'ALTER TABLE warn_space_occupy ADD COLUMN `updater` varchar(50) DEFAULT NULL COMMENT "更新者" AFTER update_time;');

-- 更新表 warn_special_car 所有字段和索引
ALTER TABLE warn_special_car CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE warn_special_car COMMENT = '特殊车辆配置';
CALL add_element_unless_exists('column', 'warn_special_car', 'id', 'ALTER TABLE warn_special_car ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'warn_special_car', 'plate_no', 'ALTER TABLE warn_special_car ADD COLUMN `plate_no` varchar(50) DEFAULT NULL COMMENT "车牌号" AFTER id;');
CALL add_element_unless_exists('column', 'warn_special_car', 'remark', 'ALTER TABLE warn_special_car ADD COLUMN `remark` varchar(255) DEFAULT NULL COMMENT "备注" AFTER plate_no;');
CALL add_element_unless_exists('column', 'warn_special_car', 'warn_type', 'ALTER TABLE warn_special_car ADD COLUMN `warn_type` tinyint(4) DEFAULT NULL COMMENT "告警类型  1：入车告警  2：出车告警  3：入车和出车都告警" AFTER remark;');
CALL add_element_unless_exists('column', 'warn_special_car', 'light_warn_witch', 'ALTER TABLE warn_special_car ADD COLUMN `light_warn_witch` tinyint(1) DEFAULT "0" COMMENT "车位灯告警开关   1：开  0：关" AFTER warn_type;');
CALL add_element_unless_exists('column', 'warn_special_car', 'deleted', 'ALTER TABLE warn_special_car ADD COLUMN `deleted` tinyint(1) DEFAULT "0" COMMENT "是否删除  0：未删除  1：已删除" AFTER light_warn_witch;');
CALL add_element_unless_exists('column', 'warn_special_car', 'create_time', 'ALTER TABLE warn_special_car ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER deleted;');
CALL add_element_unless_exists('column', 'warn_special_car', 'creator', 'ALTER TABLE warn_special_car ADD COLUMN `creator` varchar(50) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'warn_special_car', 'update_time', 'ALTER TABLE warn_special_car ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'warn_special_car', 'updater', 'ALTER TABLE warn_special_car ADD COLUMN `updater` varchar(50) DEFAULT NULL COMMENT "更新者" AFTER update_time;');

-- 更新表 warn_time 所有字段和索引
ALTER TABLE warn_time CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE warn_time COMMENT = '固定车绑定告警时间';
CALL add_element_unless_exists('column', 'warn_time', 'id', 'ALTER TABLE warn_time ADD COLUMN `id` int(11) NOT NULL AUTO_INCREMENT" COMMENT "主键";');
CALL add_element_unless_exists('column', 'warn_time', 'warn_config_id', 'ALTER TABLE warn_time ADD COLUMN `warn_config_id` int(11) DEFAULT NULL COMMENT "关联的配置表的id （warn_occupy，warn_park，warn_spacial）表的id" AFTER id;');
CALL add_element_unless_exists('column', 'warn_time', 'warn_config_type', 'ALTER TABLE warn_time ADD COLUMN `warn_config_type` tinyint(4) DEFAULT NULL COMMENT "关联类型  1：warn_occupy车位占用告警   2：warn_park车辆违停告警  3：warn_spacial特殊车告警" AFTER warn_config_id;');
CALL add_element_unless_exists('column', 'warn_time', 'day_of_week', 'ALTER TABLE warn_time ADD COLUMN `day_of_week` int(11) DEFAULT NULL COMMENT "一周的第几天（星期几）" AFTER warn_config_type;');
CALL add_element_unless_exists('column', 'warn_time', 'start_time', 'ALTER TABLE warn_time ADD COLUMN `start_time` varchar(50) DEFAULT NULL COMMENT "开始时间  HH:mm:ss" AFTER day_of_week;');
CALL add_element_unless_exists('column', 'warn_time', 'end_time', 'ALTER TABLE warn_time ADD COLUMN `end_time` varchar(50) DEFAULT NULL COMMENT "结束时间  HH:mm:ss" AFTER start_time;');
CALL add_element_unless_exists('column', 'warn_time', 'create_time', 'ALTER TABLE warn_time ADD COLUMN `create_time` datetime DEFAULT NULL COMMENT "创建时间" AFTER end_time;');
CALL add_element_unless_exists('column', 'warn_time', 'creator', 'ALTER TABLE warn_time ADD COLUMN `creator` varchar(50) DEFAULT NULL COMMENT "创建者" AFTER create_time;');
CALL add_element_unless_exists('column', 'warn_time', 'update_time', 'ALTER TABLE warn_time ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间" AFTER creator;');
CALL add_element_unless_exists('column', 'warn_time', 'updater', 'ALTER TABLE warn_time ADD COLUMN `updater` varchar(50) DEFAULT NULL COMMENT "更新者" AFTER update_time;');


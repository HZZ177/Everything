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
-- 构造表 areapointled
CREATE TABLE IF NOT EXISTS `areapointled` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Lid` int(11) DEFAULT '0' COMMENT '屏ID',
  `Aid` int(11) DEFAULT '0' COMMENT '区域ID',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='区域和屏的对应关系,主要用于屏直接统计关联区域的剩余车位数';

-- 构造表 buspointled
CREATE TABLE IF NOT EXISTS `buspointled` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `PAddr` int(11) DEFAULT NULL COMMENT '车位地址',
  `LAddr` int(11) DEFAULT NULL COMMENT '屏地址',
  `pid` int(11) DEFAULT '0' COMMENT '车位ID',
  `lid` int(11) DEFAULT '0' COMMENT '屏ID',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='车位和屏的对应关系,主要用于屏直接统计关联车位的剩余车位数';

-- 构造表 buspointrecorder
CREATE TABLE IF NOT EXISTS `buspointrecorder` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Paddr` int(11) DEFAULT '0' COMMENT '车位地址',
  `Rid` int(11) DEFAULT '0' COMMENT '刻录机ID',
  `Rport` int(11) DEFAULT '0' COMMENT '刻录机_哪一路',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 构造表 carcolor
CREATE TABLE IF NOT EXISTS `carcolor` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `LedOne` int(10) unsigned DEFAULT '0' COMMENT '灯一颜色(已停用)',
  `LedTwo` int(10) unsigned DEFAULT '0' COMMENT '灯二颜色(已停用)',
  `ACar` int(10) unsigned DEFAULT '0' COMMENT '有车时灯颜色(0当前颜色不变；1红；2绿；3蓝；4橙；5黄；6青；7紫；8白；10不亮)',
  `NoCar` int(10) unsigned DEFAULT '0' COMMENT '无车时灯颜色(0当前颜色不变；1红；2绿；3蓝；4橙；5黄；6青；7紫；8白；10不亮)',
  `CarType` int(10) unsigned DEFAULT '0' COMMENT '车位类型标识 0:Ordinary 1:Monthly  2:Disabled',
  `TypeNamect` varchar(45) DEFAULT '' COMMENT '类型名称(中文)',
  `TypeNameen` varchar(45) DEFAULT '' COMMENT '类型名称(英文)',
  `IfCount` int(11) DEFAULT '0' COMMENT '是否参与屏计数 0:不统计 1:统计',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='车位灯类型表';

-- 构造表 carfindencrypt
CREATE TABLE IF NOT EXISTS `carfindencrypt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CarNum` varchar(10) NOT NULL DEFAULT '' COMMENT '车牌号码',
  `password` varchar(10) NOT NULL DEFAULT '' COMMENT '查询密码',
  `ValidityFromDate` datetime DEFAULT NULL COMMENT '有效日期从',
  `ValidityToDate` datetime DEFAULT NULL COMMENT '有效日期至',
  `CreateTime` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_carfindencrypt_CarNum` (`CarNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='找车查询加密';

-- 构造表 columns_priv
CREATE TABLE IF NOT EXISTS `columns_priv` (
  `Host` char(60) COLLATE utf8_bin NOT NULL DEFAULT '',
  `Db` char(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `User` char(16) COLLATE utf8_bin NOT NULL DEFAULT '',
  `Table_name` char(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `Column_name` char(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Column_priv` set('Select','Insert','Update','References') CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`Host`,`Db`,`User`,`Table_name`,`Column_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Column privileges';

-- 构造表 controlset
CREATE TABLE IF NOT EXISTS `controlset` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `LNumber` varchar(50) DEFAULT '' COMMENT '屏控制字',
  `Location` varchar(50) DEFAULT '0' COMMENT '箭头位置(0:左边 1:右边)',
  `Direction` varchar(50) DEFAULT '0' COMMENT '箭头方向(0:向左 1:向右 2:向上 3:向下)',
  `Color` varchar(50) DEFAULT '3' COMMENT '数字颜色(0:红 1:橙 2:绿 3:根据数值)',
  `BusType` varchar(50) DEFAULT '1' COMMENT '车位类型(1:正常车位 0:残障人车位)',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='屏控制字描述';

-- 构造表 cy2
CREATE TABLE IF NOT EXISTS `cy2` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT '楼层指引ID',
  `CIP` varchar(50) NOT NULL COMMENT '要设置的查询机ip',
  `OtherMid` int(11) unsigned NOT NULL COMMENT '要对应的其他楼层的地图id',
  `FloorPoint` varchar(50) NOT NULL COMMENT '楼层指引图片名称',
  `fstate` int(11) unsigned NOT NULL DEFAULT '1',
  `otherselfmac` int(10) NOT NULL DEFAULT '0' COMMENT '其他楼层的默认的查询机id',
  `DirType` int(1) NOT NULL DEFAULT '0' COMMENT '方向',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0未上传；1上传中；2上传成功；3回写成功)',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0 未删除,1 已删除',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='楼层指引';

-- 构造表 cy_cx_a
CREATE TABLE IF NOT EXISTS `cy_cx_a` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `CName` varchar(50) NOT NULL DEFAULT '' COMMENT '查询机名称',
  `CIP` varchar(50) NOT NULL DEFAULT '' COMMENT '查询机地址',
  `MID` int(11) NOT NULL DEFAULT '0' COMMENT '楼层ID',
  `lukou` int(11) NOT NULL DEFAULT '0',
  `mapfile` varchar(45) NOT NULL DEFAULT '' COMMENT '查询机使用的地图文件',
  `angle` int(11) NOT NULL DEFAULT '0' COMMENT '查询机摆向角度',
  `Direction` int(6) NOT NULL DEFAULT '45' COMMENT '查询机方向',
  `PosX` int(11) NOT NULL DEFAULT '0' COMMENT 'X坐标',
  `PosY` int(11) NOT NULL DEFAULT '0' COMMENT 'Y坐标',
  `AreaId` int(11) NOT NULL DEFAULT '0' COMMENT '区域ID',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0未上传；1上传中；2上传成功；3回写成功)',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0 未删除,1 已删除',
  `route_ip` varchar(50) DEFAULT '' COMMENT '查询机请求服务器路线ip',
  `up_point` varchar(50) DEFAULT '' COMMENT '上方坐标',
  `down_point` varchar(50) DEFAULT '' COMMENT '下方坐标',
  `left_point` varchar(50) DEFAULT '' COMMENT '左方坐标',
  `right_point` varchar(50) DEFAULT '' COMMENT '右方坐标',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='找车机信息表';

-- 构造表 dspinfolog
CREATE TABLE IF NOT EXISTS `dspinfolog` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `CarplateNum` varchar(50) DEFAULT '' COMMENT '车牌',
  `CarAddr` int(11) DEFAULT '0' COMMENT '车位地址',
  `ImgName` varchar(100) DEFAULT '' COMMENT '图片名称',
  `PdataTime` varchar(40) DEFAULT NULL COMMENT '抓拍时间',
  PRIMARY KEY (`ID`),
  KEY `IDX_dspinfolog` (`CarAddr`,`PdataTime`),
  KEY `IDX_dspinfolog_PdataTime` (`PdataTime`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='车辆历史抓拍记录';

-- 构造表 infoarea
CREATE TABLE IF NOT EXISTS `infoarea` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `AreaName` varchar(30) NOT NULL DEFAULT '' COMMENT '中文区域名称',
  `AreaName2` varchar(30) NOT NULL DEFAULT '' COMMENT '英文区域名称',
  `MapId` int(11) DEFAULT '0' COMMENT '区域对应楼层ID',
  `MapName` varchar(30) DEFAULT '' COMMENT '地图名称',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0未上传；1上传中；2上传成功；3回写成功)',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0 未删除,1 已删除',
  `PosX` int(11) DEFAULT '0' COMMENT '区域X坐标',
  `PosY` int(11) DEFAULT '0' COMMENT '区域Y坐标',
  `TotalNum` int(11) DEFAULT '0' COMMENT '区域总车位数',
  `FreeNum` int(11) DEFAULT '0' COMMENT '区域剩余车位数',
  `AreaType` int(11) DEFAULT '0' COMMENT '0:普通区域 1:立体车库区域',
  `LimitNum` int(11) DEFAULT '0' COMMENT '区域限制车位数',
  `AreaName3` varchar(30) DEFAULT '' COMMENT '其他区域名称',
  `ClientUpdateTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='区域信息表';

-- 构造表 infobus
CREATE TABLE IF NOT EXISTS `infobus` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `BusNumber` varchar(40) DEFAULT '0',
  `Addr` int(11) DEFAULT '0',
  `state` int(11) DEFAULT '0' COMMENT '0:无车；1有车；2故障',
  `LeaveTime` varchar(40) DEFAULT NULL,
  `ComeTime` varchar(40) DEFAULT NULL,
  `carplatenum` varchar(50) DEFAULT NULL,
  `ImgName` varchar(50) DEFAULT NULL,
  `AreaID` int(11) DEFAULT '0',
  `Flag` int(10) unsigned NOT NULL DEFAULT '0',
  `PreLeaveTime` varchar(40) DEFAULT NULL,
  `PreComeTime` varchar(40) DEFAULT NULL,
  `PreCarplateNum` varchar(50) DEFAULT NULL,
  `CarType` int(11) DEFAULT '0',
  `ifchange` int(11) DEFAULT '0',
  `ifsend` int(11) DEFAULT '0',
  `CarplateDigital` varchar(45) DEFAULT NULL,
  `Mid` int(10) unsigned NOT NULL DEFAULT '0',
  `Trun` int(10) unsigned NOT NULL DEFAULT '0',
  `PosX` int(10) unsigned NOT NULL DEFAULT '0',
  `PosY` int(10) unsigned NOT NULL DEFAULT '0',
  `IfSetRoute` varchar(255) DEFAULT '0' COMMENT '1-预设路线 0-自动路线',
  `PSPlaceNum` varchar(30) NOT NULL DEFAULT '' COMMENT '车位编号',
  `PSPlaceName` varchar(30) NOT NULL DEFAULT '' COMMENT '车位名称',
  `WDCloudFlag` int(4) NOT NULL DEFAULT '0' COMMENT '万达云上传标志：0未上传；1已上传',
  `WDCloudDate` datetime DEFAULT NULL COMMENT '云异动时间',
  `parktype` int(1) DEFAULT '0' COMMENT '0普通车位，1产权车位',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0未上传；1上传中；2上传成功；3回写成功)',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0 未删除,1 已删除',
  `ClientUpdateTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `IDX_BusNo_CarNo` (`BusNumber`,`carplatenum`),
  KEY `Idx_infobus_Addr_AreaId` (`Addr`,`AreaID`),
  KEY `IX_infobus` (`Addr`,`state`),
  KEY `IX_infobus_Addr` (`Addr`)
) ENGINE=MyISAM AUTO_INCREMENT=1043 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=123;

-- 构造表 infoconfig
CREATE TABLE IF NOT EXISTS `infoconfig` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inquireWays` varchar(200) DEFAULT NULL COMMENT '查询方式',
  `openAlreadyTime` tinyint(1) DEFAULT NULL COMMENT '是否显示已停放时长',
  `chargePort` int(11) DEFAULT '8080' COMMENT '收费框架端口',
  `openParingTime` tinyint(1) DEFAULT NULL COMMENT '是否显示停放时间',
  `openBusiness` tinyint(1) DEFAULT NULL COMMENT '是否启用商家查询',
  `openCarPwd` tinyint(1) DEFAULT NULL COMMENT '是否启用车牌加密',
  `cloudPort` int(11) DEFAULT '8099' COMMENT '云计费端口',
  `plugInCard` tinyint(1) DEFAULT '0' COMMENT '是否支持插卡',
  `swipingCard` tinyint(1) DEFAULT '0' COMMENT '是否支持刷卡',
  `snapCard` tinyint(1) DEFAULT '0' COMMENT '是否支持闪付',
  `aliPay` tinyint(1) DEFAULT '0' COMMENT '是否支持支付宝',
  `weiXin` tinyint(1) DEFAULT '0' COMMENT '是否支持微信支付',
  `cloudChargeServiceAdd` varchar(50) DEFAULT '' COMMENT '云收费服务端地址',
  `chargeServiceAdd` varchar(50) DEFAULT '' COMMENT '提前缴费服务端地址',
  `recordCount` int(11) DEFAULT '25' COMMENT '空车牌查询显示记录上限',
  `routeType` tinyint(1) DEFAULT '1' COMMENT '查询机路线样式(0静态1动态)',
  `phoneServiceAdd` varchar(50) DEFAULT '' COMMENT '找车服务器IP',
  `ifSubSeller` tinyint(4) DEFAULT NULL COMMENT '是否子商户',
  `plateMaxNum` int(11) DEFAULT '5' COMMENT '车牌号输入上限',
  `parkMaxNum` int(11) DEFAULT '5' COMMENT '车位号输入上限',
  `isOpenPrint` tinyint(4) DEFAULT NULL COMMENT '是否启用停车打印',
  `isOpenPickUp` tinyint(4) DEFAULT NULL COMMENT '是否启用取车功能',
  `languageSupport` int(11) DEFAULT '0' COMMENT '0中文+英文 1中文 2英文',
  `foreginLanguage` varchar(30) DEFAULT '' COMMENT '支持的第三种语言缩写',
  `isOpenQrcode` tinyint(1) DEFAULT '0' COMMENT '是否显示找车二维码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='找车机常用参数表';

-- 构造表 infofloor
CREATE TABLE IF NOT EXISTS `infofloor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `curmid` int(11) DEFAULT '0' COMMENT '起始层平面ID',
  `othermid` int(11) DEFAULT '0' COMMENT '终点层平面ID',
  `imgsrc` varchar(255) DEFAULT NULL COMMENT '跨层图名称',
  `ftype` int(11) DEFAULT '0' COMMENT '跨层类型(0:楼层到楼层 1:查询机到楼层)',
  `pointid` int(11) DEFAULT '0' COMMENT '跨层指定的电梯口ID ftype为1时，需要指定查询机对应要走的电梯口',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='跨层寻车用指引设置表';

-- 构造表 infohint
CREATE TABLE IF NOT EXISTS `infohint` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `FindOption` int(11) DEFAULT '0' COMMENT '查询方式 (0:快捷 1:全车牌 2:时间 3:车位 4:空车牌)',
  `SubOption` int(11) DEFAULT '0' COMMENT '子分支',
  `Memo` varchar(255) DEFAULT '' COMMENT '描述信息',
  `cnWarnInfo` varchar(255) DEFAULT '' COMMENT '中文提示信息',
  `enWarnInfo` varchar(255) DEFAULT '' COMMENT '英文提示信息',
  `otherWarnInfo` varchar(255) DEFAULT '' COMMENT '其他语言提示信息',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='寻车机常用提示信息配置表';

-- 构造表 infoled
CREATE TABLE IF NOT EXISTS `infoled` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Addr` int(11) DEFAULT '0' COMMENT '屏地址',
  `LMemo` varchar(255) DEFAULT '' COMMENT '屏描述',
  `LType` varchar(2) DEFAULT NULL COMMENT '屏控制字',
  `ShowNum` smallint(6) DEFAULT NULL COMMENT '固定显示数值',
  `ShowType` int(11) DEFAULT '0',
  `State` int(11) DEFAULT '0',
  `EmptyBus` int(11) DEFAULT '0' COMMENT '统计的剩余车位数',
  `last_update` datetime DEFAULT NULL,
  `ifclosed` int(11) DEFAULT '0',
  `ifsend` int(11) unsigned DEFAULT '0',
  `ledsz` int(11) unsigned NOT NULL DEFAULT '0',
  `allbusaddr` int(11) unsigned NOT NULL DEFAULT '0',
  `lotid` int(11) NOT NULL DEFAULT '0' COMMENT '楼层ID',
  `posx` int(11) DEFAULT '0' COMMENT 'X坐标',
  `posy` int(11) DEFAULT '0' COMMENT 'Y坐标',
  `checknum` int(11) DEFAULT '0' COMMENT '屏校正数值',
  `ledtype` int(11) DEFAULT '0' COMMENT '0:普通屏 1:总屏',
  `criticalval` int(11) DEFAULT '0' COMMENT '临界值(统计出来低于临界值直接统计为0)',
  `levaddr` int(11) DEFAULT '0' COMMENT '主屏地址',
  `inoutledip` varchar(255) DEFAULT '' COMMENT '出入口LED屏IP',
  `ledkind` int(2) DEFAULT '0' COMMENT '0:代表485总屏 1:代表485子屏 3:代表LED网络屏',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='屏信息(子屏)配置表';

-- 构造表 infoledlev
CREATE TABLE IF NOT EXISTS `infoledlev` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Addr` int(11) DEFAULT '0' COMMENT '主屏地址',
  `LMemo` varchar(255) DEFAULT '' COMMENT '主屏描述',
  `LType` varchar(2) DEFAULT NULL COMMENT '主屏控制字',
  `ShowNum` smallint(6) DEFAULT NULL,
  `ShowType` int(11) DEFAULT '0',
  `State` int(11) DEFAULT '0',
  `EmptyBus` int(11) DEFAULT '0',
  `last_update` datetime DEFAULT NULL,
  `ifclosed` int(11) DEFAULT '0',
  `ifsend` int(11) unsigned DEFAULT '0',
  `ledsz` int(11) unsigned NOT NULL DEFAULT '0',
  `allbusaddr` int(11) unsigned NOT NULL DEFAULT '0',
  `lotid` int(11) NOT NULL DEFAULT '0' COMMENT '楼层ID',
  `posx` int(11) DEFAULT '0' COMMENT 'X坐标',
  `posy` int(11) DEFAULT '0' COMMENT 'Y坐标',
  `checknum` int(11) DEFAULT '0',
  `ledtype` int(11) DEFAULT '3' COMMENT '屏类型(1:单向屏 2:双向屏 3:三向屏)',
  `criticalval` int(11) DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='主屏信息表';

-- 构造表 infomap
CREATE TABLE IF NOT EXISTS `infomap` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Mapname` varchar(30) NOT NULL DEFAULT '',
  `Mapfile` varchar(60) NOT NULL DEFAULT '',
  `Big` int(11) unsigned NOT NULL DEFAULT '0',
  `FloorPoint` varchar(50) NOT NULL DEFAULT '',
  `MapDeclare` varchar(50) NOT NULL DEFAULT '',
  `SpaceL` int(8) NOT NULL DEFAULT '0' COMMENT '车位长',
  `SpaceW` int(8) NOT NULL DEFAULT '0' COMMENT '车位宽',
  `orderNo` tinyint(4) NOT NULL DEFAULT '0' COMMENT '排序字段',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0未上传；1上传中；2上传成功；3回写成功)',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0 未删除,1 已删除',
  `total` int(11) DEFAULT '0',
  `angle` float DEFAULT NULL COMMENT '与正北的偏差角度',
  `Disperpixel` float DEFAULT '1' COMMENT '每像素对应的实际距离',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='楼层地图信息表';

-- 构造表 infonode
CREATE TABLE IF NOT EXISTS `infonode` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Addr` int(11) DEFAULT '0' COMMENT 'IPCAM总地址|DSP总地址',
  `BusNum` int(11) DEFAULT '0' COMMENT 'IPCAM下挂车位数|DSP下挂车位数',
  `NMemo` mediumtext COMMENT '描述',
  `State` int(11) DEFAULT '0' COMMENT '是否在线 0:离线 1:在线',
  `LastRecData` varchar(30) DEFAULT NULL,
  `LastRecTime` varchar(40) DEFAULT NULL,
  `PowerIp` varchar(255) DEFAULT NULL COMMENT '相机对应电源板IP',
  `PowerSend` varchar(255) DEFAULT NULL COMMENT '0常规状态 1待发送灭灯 2已发送灭灯,待发送开灯(等待5秒钟后发送) 3已发送开灯,待重启(等待3分钟后未变化则重新发送)',
  `PowerSendTime` datetime DEFAULT NULL COMMENT '上次发送时间',
  `DeviceType` int(11) DEFAULT '0' COMMENT '设备类型0 IPCAM 1 节点',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='相机信息或节点信息表';

-- 构造表 infopic
CREATE TABLE IF NOT EXISTS `infopic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `imgsrc` varchar(255) DEFAULT '' COMMENT '图片资源',
  `imgname` varchar(255) DEFAULT NULL COMMENT '图片名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='图片信息表';

-- 构造表 inforecorder
CREATE TABLE IF NOT EXISTS `inforecorder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(255) DEFAULT NULL COMMENT '刻录机IP',
  `Memo` varchar(255) DEFAULT NULL COMMENT '描述',
  `loginname` varchar(255) DEFAULT NULL COMMENT '登陆名称',
  `loginpwd` varchar(255) DEFAULT NULL COMMENT '登陆密码',
  `port` int(11) DEFAULT '0' COMMENT 'TCP端口号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='刻录机表';

-- 构造表 infoserlog
CREATE TABLE IF NOT EXISTS `infoserlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usetime` datetime DEFAULT NULL COMMENT '使用时间',
  `usetype` int(11) DEFAULT '0' COMMENT '使用类型',
  `useval` varchar(255) DEFAULT NULL COMMENT '查询参数',
  `cip` varchar(255) DEFAULT '' COMMENT '查询机IP',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='查询机使用记录统计表';

-- 构造表 infosystem
CREATE TABLE IF NOT EXISTS `infosystem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) DEFAULT '0' COMMENT '类型',
  `memo` varchar(255) DEFAULT '' COMMENT '名称',
  `value` varchar(255) DEFAULT '' COMMENT '数值',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统常用参数配置表';

-- 构造表 log_carinout
CREATE TABLE IF NOT EXISTS `log_carinout` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT '自动增长',
  `ParkDate` date DEFAULT NULL COMMENT '停车日期',
  `ParkHour` int(11) NOT NULL DEFAULT '0' COMMENT '停车小时',
  `FlowIn` int(11) NOT NULL DEFAULT '0' COMMENT '全部车位入车数',
  `FlowOut` int(11) NOT NULL DEFAULT '0' COMMENT '全部车位出车数',
  `FlowIn1` int(11) NOT NULL DEFAULT '0' COMMENT '普通时租入车数',
  `FlowOut1` int(11) NOT NULL DEFAULT '0' COMMENT '普通时租出车数',
  `FlowIn2` int(11) NOT NULL DEFAULT '0' COMMENT '固定专用入车数',
  `FlowOut2` int(11) NOT NULL DEFAULT '0' COMMENT '固定专用出车数',
  `FlowIn3` int(11) NOT NULL DEFAULT '0' COMMENT '非固定专用入车数',
  `FlowOut3` int(11) NOT NULL DEFAULT '0' COMMENT '非固定专用出车数',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='进出流量统计表';

-- 构造表 log_hourcount
CREATE TABLE IF NOT EXISTS `log_hourcount` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `StaticDate` date DEFAULT NULL COMMENT '统计时间',
  `StaticHour` int(11) DEFAULT NULL COMMENT '统计小时',
  `ParkLong` double DEFAULT NULL COMMENT '全部车位合计时长',
  `ParkLong1` double DEFAULT NULL COMMENT '普通时租车位合计时长',
  `ParkLong2` double DEFAULT NULL COMMENT '固定专用车位合计时长',
  `ParkLong3` double DEFAULT NULL COMMENT '非固定专用车位合计时长',
  `ParkCount` int(11) DEFAULT '0' COMMENT '全部车位合计数',
  `ParkCount1` int(11) DEFAULT '0' COMMENT '普通时租车位合计数',
  `ParkCount2` int(11) DEFAULT '0' COMMENT '固定专用车位合计数',
  `ParkCount3` int(11) DEFAULT '0' COMMENT '非固定专用车位合计数',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='泊位使用率报表';

-- 构造表 log_login
CREATE TABLE IF NOT EXISTS `log_login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `login_account` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '登录账号',
  `login_time` datetime DEFAULT NULL COMMENT '登录时间',
  `login_desc` varchar(200) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '登录描述',
  `login_ip` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '登录ip',
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=4096 COMMENT='登录日志';

-- 构造表 log_operate
CREATE TABLE IF NOT EXISTS `log_operate` (
  `ope_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '操作ID',
  `ope_user_id` varchar(11) DEFAULT NULL COMMENT '操作用户',
  `ope_time` datetime DEFAULT NULL COMMENT '操作时间',
  `ope_ip` varchar(50) DEFAULT NULL COMMENT '操作ip',
  `ope_action` int(1) DEFAULT NULL COMMENT '操作行为 (1=新增 2=删除 3=修改)',
  `ope_content` longtext COMMENT '操作内容',
  PRIMARY KEY (`ope_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志';

-- 构造表 log_parkcount
CREATE TABLE IF NOT EXISTS `log_parkcount` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT '自动增长',
  `AreaId` int(11) NOT NULL DEFAULT '0' COMMENT '区域ID',
  `AreaName` varchar(50) NOT NULL DEFAULT '' COMMENT '区域名称',
  `ParkDate` datetime DEFAULT NULL COMMENT '停车日期',
  `ParkHour` int(11) NOT NULL DEFAULT '0' COMMENT '停车小时',
  `ParkCount` int(11) NOT NULL DEFAULT '0' COMMENT '占用数',
  `FlowIn` int(11) NOT NULL DEFAULT '0' COMMENT '入车数',
  `FlowOut` int(11) NOT NULL DEFAULT '0' COMMENT '出车数',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0:未上传 1:上传中 2:上传成功 3:回写成功)',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0:未删除 1:已删除',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `UK_log_parkcount` (`AreaId`,`ParkDate`,`ParkHour`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='车流量统计表';

-- 构造表 log_parkinglotlog
CREATE TABLE IF NOT EXISTS `log_parkinglotlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自动增长',
  `CarplateNum` varchar(20) NOT NULL DEFAULT '' COMMENT '车牌号',
  `CarAddr` int(11) NOT NULL DEFAULT '0' COMMENT '车位地址',
  `ImgName` varchar(255) NOT NULL DEFAULT '' COMMENT '图片',
  `InTime` datetime DEFAULT NULL COMMENT '入场时间',
  `OutTime` datetime DEFAULT NULL COMMENT '出场时间',
  `longTime` int(11) NOT NULL DEFAULT '0' COMMENT '停车时长',
  `AreaId` int(11) NOT NULL DEFAULT '0' COMMENT '区域',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0:未上传 1:上传中 2:上传成功 3:回写成功)',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0:未删除 1:已删除',
  PRIMARY KEY (`id`),
  KEY `IDX_log_parkinglotlog_OutTime` (`OutTime`),
  KEY `IX_log_parkinglotlog_InTime` (`InTime`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='历史停放记录统计报表';

-- 构造表 log_temp
CREATE TABLE IF NOT EXISTS `log_temp` (
  `ID` int(11) DEFAULT '0' COMMENT '自动增长',
  `temp` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 构造表 parklampgroup
CREATE TABLE IF NOT EXISTS `parklampgroup` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `groupname` varchar(45) NOT NULL DEFAULT '' COMMENT '分组名称',
  `lampId` varchar(4096) DEFAULT '0' COMMENT '组内相机灯信息',
  `parkId` varchar(4096) DEFAULT '0' COMMENT '组内探测器信息',
  `empty` int(10) unsigned DEFAULT '0',
  `state` int(10) unsigned DEFAULT '0',
  `lastULTime` datetime DEFAULT '2013-01-01 00:00:00' COMMENT '最後一次發送燈指令時間',
  `lotid` int(11) DEFAULT '0' COMMENT '楼层ID',
  `lotname` varchar(50) DEFAULT '',
  `total` int(11) DEFAULT '0' COMMENT '总探测器数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='车位分组表';

-- 构造表 parkmsglog
CREATE TABLE IF NOT EXISTS `parkmsglog` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `areaid` int(11) DEFAULT NULL COMMENT '区域ID',
  `busnumber` varchar(255) DEFAULT '' COMMENT '车位编号',
  `plate` varchar(255) DEFAULT '' COMMENT '车牌号码',
  `cometime` datetime DEFAULT NULL COMMENT '进场时间',
  `parklong` int(11) DEFAULT '0' COMMENT 'cometime与统计的时间（一般为当天0点0分0秒）的时间差，单位为分钟',
  `imgname` varchar(255) DEFAULT '' COMMENT '图片信息',
  `toltype` int(11) DEFAULT '1' COMMENT '1-过夜 2-超时',
  `statictime` datetime DEFAULT NULL COMMENT '统计时间（一般为当天0点0分0秒）',
  PRIMARY KEY (`id`),
  KEY `IDX_parkmsglog_statictime` (`statictime`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='过夜车统计表';

-- 构造表 parkwarnlog
CREATE TABLE IF NOT EXISTS `parkwarnlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `areaid` int(11) DEFAULT NULL COMMENT '区域ID',
  `busnumber` varchar(255) DEFAULT NULL COMMENT '车位编号',
  `plate` varchar(255) DEFAULT NULL COMMENT '车牌',
  `cometime` datetime DEFAULT NULL COMMENT '入场时间',
  `parklong` int(11) DEFAULT '0' COMMENT '停放时长',
  `imgname` varchar(255) DEFAULT NULL COMMENT '图片名称',
  `toltype` int(11) DEFAULT '0' COMMENT '1:过夜 2:超时',
  `statictime` datetime DEFAULT NULL COMMENT '统计时间',
  PRIMARY KEY (`id`),
  KEY `IDX_parkwarnlog_statictime` (`statictime`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='超时停车记录统计表';

-- 构造表 sys_assign
CREATE TABLE IF NOT EXISTS `sys_assign` (
  `assign_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `assign_rela_id` char(32) DEFAULT NULL COMMENT '授权ID',
  `assign_role` int(11) DEFAULT NULL COMMENT '授权角色',
  `assign_type` int(1) DEFAULT NULL COMMENT '授权类型 1 菜单 2 功能节点',
  `create_time` datetime DEFAULT NULL COMMENT '授权时间',
  PRIMARY KEY (`assign_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1825 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=183 COMMENT='系统授权';

-- 构造表 sys_i18n_message
CREATE TABLE IF NOT EXISTS `sys_i18n_message` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一标识',
  `CODE` varchar(100) DEFAULT NULL COMMENT '代码',
  `DESCRIPTION` varchar(500) DEFAULT NULL COMMENT '描述',
  `MODULE` varchar(100) DEFAULT NULL COMMENT '模块',
  `ZH_CN` varchar(500) DEFAULT NULL COMMENT '中文简体-中国',
  `ZH_HK` varchar(500) DEFAULT NULL COMMENT '中文繁体-香港',
  `ZH_TW` varchar(500) DEFAULT NULL COMMENT '中文繁体-台湾',
  `EN_US` varchar(500) DEFAULT NULL COMMENT '英文-美国',
  `QT_LAN` varchar(500) DEFAULT NULL COMMENT '其他语言',
  `CREATE_TIME` datetime DEFAULT NULL COMMENT '创建时间',
  `UPDATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `UK_sys_i18n_message_CODE` (`CODE`)
) ENGINE=InnoDB AUTO_INCREMENT=2671 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=251 COMMENT='国际化消息表';

-- 构造表 sys_module
CREATE TABLE IF NOT EXISTS `sys_module` (
  `module_id` char(32) NOT NULL COMMENT '主键ID',
  `module_pid` char(32) DEFAULT NULL COMMENT '父级ID',
  `module_name` varchar(50) DEFAULT NULL COMMENT '模块名称',
  `module_url` varchar(200) DEFAULT NULL COMMENT '模块URL',
  `module_desc` varchar(200) DEFAULT NULL COMMENT '模块描述',
  `module_order` int(5) DEFAULT NULL COMMENT '模块排序号',
  `module_show` int(1) DEFAULT NULL COMMENT '模块显示状态 0=隐藏 1=显示',
  `module_status` int(1) DEFAULT NULL COMMENT '模块状态 0=无效 1=有效',
  `module_icon` varchar(20) DEFAULT NULL COMMENT '模块图标',
  `module_val` varchar(50) DEFAULT NULL COMMENT '模块值(用于权限控制)',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=309 COMMENT='系统模块信息表';

-- 构造表 sys_module_node
CREATE TABLE IF NOT EXISTS `sys_module_node` (
  `node_id` char(32) NOT NULL COMMENT '节点ID',
  `node_module` char(32) DEFAULT NULL COMMENT '节点所属模块',
  `node_name` varchar(50) DEFAULT NULL COMMENT '节点名称',
  `node_url` varchar(100) DEFAULT NULL COMMENT '节点url',
  `node_val` varchar(50) DEFAULT NULL COMMENT '节点值(用于权限控制)',
  `node_order` int(5) DEFAULT NULL COMMENT '节点序号',
  `node_desc` varchar(200) DEFAULT NULL COMMENT '节点描述',
  `node_i18n_code` varchar(255) DEFAULT NULL COMMENT '国际化',
  PRIMARY KEY (`node_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=396 COMMENT='系统功能节点表';

-- 构造表 sys_org
CREATE TABLE IF NOT EXISTS `sys_org` (
  `id` char(32) NOT NULL COMMENT '唯一标识',
  `pid` char(32) DEFAULT NULL COMMENT '上级组织机构标识',
  `name` varchar(200) DEFAULT NULL COMMENT '名称',
  `description` varchar(200) DEFAULT NULL COMMENT '描述',
  `remark` varchar(200) DEFAULT NULL COMMENT '备注',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_show` char(1) NOT NULL DEFAULT '1' COMMENT '1 显示 0 不显示',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统组织机构基本信息表';

-- 构造表 sys_org_role
CREATE TABLE IF NOT EXISTS `sys_org_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `role_id` char(32) DEFAULT NULL COMMENT '角色ID',
  `org_id` char(32) DEFAULT NULL COMMENT '机构ID',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=4096 COMMENT='系统角色机构关联表';

-- 构造表 sys_org_user
CREATE TABLE IF NOT EXISTS `sys_org_user` (
  `id` char(32) NOT NULL COMMENT '唯一标识',
  `org_id` char(32) DEFAULT NULL COMMENT '组织机构标识',
  `user_id` char(32) DEFAULT NULL COMMENT '用户标识',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1820 COMMENT='系统用户所属组织机构关联表';

-- 构造表 sys_role
CREATE TABLE IF NOT EXISTS `sys_role` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `role_name` varchar(50) DEFAULT NULL COMMENT '角色名称',
  `role_remark` varchar(200) DEFAULT NULL COMMENT '角色备注',
  `role_desc` varchar(200) DEFAULT NULL COMMENT '角色描述',
  `role_status` int(1) DEFAULT NULL COMMENT '角色状态 0=无效 1=有效',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=4096 COMMENT='系统角色信息表';

-- 构造表 sys_role_user
CREATE TABLE IF NOT EXISTS `sys_role_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `role_id` int(11) DEFAULT NULL COMMENT '角色ID',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=2048 COMMENT='系统角色与用户关联表';

-- 构造表 sys_user
CREATE TABLE IF NOT EXISTS `sys_user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_name` varchar(50) DEFAULT NULL COMMENT '用户名',
  `user_account` varchar(50) DEFAULT NULL COMMENT '账号',
  `user_pwd` varchar(50) DEFAULT NULL COMMENT '密码',
  `user_phone` varchar(11) DEFAULT NULL COMMENT '手机号',
  `user_remark` varchar(200) DEFAULT NULL COMMENT '备注',
  `user_desc` varchar(500) DEFAULT NULL COMMENT '描述',
  `user_status` int(1) DEFAULT NULL COMMENT '状态 0=无效 1=有效',
  `user_admin` int(1) DEFAULT NULL COMMENT '0 普通用户 1 内置超级管理员',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=4096 COMMENT='系统用户基本信息表';

-- 构造表 t_ad
CREATE TABLE IF NOT EXISTS `t_ad` (
  `Id` int(8) NOT NULL AUTO_INCREMENT,
  `ParkId` int(8) NOT NULL DEFAULT '0' COMMENT '停车场编号',
  `ComputerId` varchar(20) NOT NULL DEFAULT '' COMMENT '查询机IP(若配置为127.0.0.1,则所有查询机可用;若不是配置为127.0.0.1,则只有对应查询机可用)',
  `AdType` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0:查询机下面广告 1:找车页面广告',
  `PlayType` int(8) NOT NULL DEFAULT '1' COMMENT '播放位置(1:找车 2:户外屏 3:其他)',
  `VideoUrl` varchar(1000) NOT NULL DEFAULT '' COMMENT '视频资源路径',
  `ImagePlayTime` int(8) NOT NULL DEFAULT '0' COMMENT '播放时间',
  `ImagePlayStyle` int(8) NOT NULL DEFAULT '0' COMMENT '播放样式',
  `ImagesUrl` varchar(1000) NOT NULL DEFAULT '' COMMENT '图片资源路径',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='广告主表';

-- 构造表 t_adsub
CREATE TABLE IF NOT EXISTS `t_adsub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ObjectId` int(8) NOT NULL DEFAULT '1' COMMENT '1:广告1 2:广告2',
  `FormId` int(11) NOT NULL DEFAULT '0' COMMENT '主表ID',
  `FilePath` varchar(500) NOT NULL DEFAULT '' COMMENT '文件路径',
  `Remark` varchar(255) NOT NULL DEFAULT '' COMMENT '描述',
  `FileType` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0:图片 1：视频',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='广告子表';

-- 构造表 t_area_device
CREATE TABLE IF NOT EXISTS `t_area_device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deviceaddr` int(11) DEFAULT '0' COMMENT '相机地址',
  `areaid` int(11) DEFAULT '0' COMMENT '区域ID',
  `type` int(11) DEFAULT '0' COMMENT '0:进 1:出',
  `outareaid` varchar(255) DEFAULT NULL COMMENT '标识该相机是否作为其他区域的出口相机使用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='区域设备信息表';

-- 构造表 t_businfo
CREATE TABLE IF NOT EXISTS `t_businfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `busid` varchar(32) NOT NULL COMMENT '全局车位编号（逻辑编号）',
  `lockDtuId` varchar(32) NOT NULL COMMENT '车位锁DTU设备id',
  `lockPos` varchar(32) NOT NULL COMMENT '车位锁DTU下车位编号',
  `autoLock` int(11) NOT NULL DEFAULT '15' COMMENT '自动上锁时间(秒)',
  `lockStatus` int(11) NOT NULL DEFAULT '0' COMMENT '车位锁状态，0未上锁；1上锁；2故障',
  `detectDtuId` varchar(32) NOT NULL COMMENT '探测器dtuID',
  `detectPos` varchar(32) NOT NULL COMMENT '探测器在dtu下编号',
  `detectStatus` int(11) NOT NULL DEFAULT '0' COMMENT '探测器状态，0无车；1有车；2故障',
  `updateTime` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `busid` (`busid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='车位与车位锁关系表';

-- 构造表 t_display_config
CREATE TABLE IF NOT EXISTS `t_display_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lot_id` int(11) DEFAULT '0' COMMENT '楼层id',
  `title_top` double(255,0) DEFAULT '0' COMMENT '标题上边距',
  `title_left` double DEFAULT '0' COMMENT '标题左边距',
  `title_font_size` double DEFAULT '0' COMMENT '标题字体大小',
  `title_color` varchar(255) DEFAULT '#fff' COMMENT '标题颜色',
  `title_text` varchar(255) DEFAULT '' COMMENT '标题内容',
  `led_font_size` double DEFAULT '0' COMMENT 'led屏字体大小',
  `led_width` double DEFAULT '0' COMMENT 'led屏宽度',
  `led_height` double DEFAULT '0' COMMENT 'led屏高度',
  `led_common_color` varchar(255) DEFAULT '#00ffff' COMMENT 'led屏剩余数颜色',
  `led_full_color` varchar(255) DEFAULT '#ff1100' COMMENT 'led屏满位颜色',
  `ico_width` double DEFAULT '0' COMMENT '图标宽度',
  `ico_height` double DEFAULT '0' COMMENT '图标高度',
  `ico_woman_img` varchar(255) DEFAULT '' COMMENT '空闲女图标',
  `ico_woman_actimg` varchar(255) DEFAULT '' COMMENT '占用女图标',
  `ico_man_img` varchar(255) DEFAULT '' COMMENT '空闲男图标',
  `ico_man_actimg` varchar(255) DEFAULT '' COMMENT '占用男图标',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='LCD显示屏配置项';

-- 构造表 t_events
CREATE TABLE IF NOT EXISTS `t_events` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `evtType` int(11) NOT NULL DEFAULT '0' COMMENT '类型(0出车事件,1抬杆,2计算费用,3重新抓拍,\r\n4手动抓拍图片返回数据,5停止拍照,6恢复拍照,\r\n7设置ETC配置,\r\n8获取ETC配置\r\n9LED显示剩余车位,\r\n11入口弹窗，需人工确认才进\r\n12手动关闸,13:发送可定制屏指令(致远4S),\r\n14:出入口是否启用\r\n16：找车系统LED屏指令\r\n20：通知入口要重新抓拍(出口时判断是否剩余车位小于0)\r\n21：设置DSP控制还是服务器控制\r\n22：强制抬杆\r\n23：强制抬杆后恢复到落杆状态\r\n24：一个地址可发任意行数的任意内容\r\n27：强制落闸\r\n28：恢复（原来是抬杆就是抬杆，原来是落闸就落闸）',
  `imgName` varchar(50) NOT NULL DEFAULT '0' COMMENT '图片名称',
  `dspIp` varchar(32) NOT NULL DEFAULT '0',
  `evtTime` varchar(32) NOT NULL DEFAULT '0' COMMENT '当前事件的时间',
  `inAddr` varchar(32) NOT NULL DEFAULT '0',
  `inTime` varchar(32) NOT NULL DEFAULT '0',
  `outAddr` varchar(32) NOT NULL DEFAULT '0',
  `outTime` varchar(32) NOT NULL DEFAULT '0',
  `money` int(11) NOT NULL DEFAULT '0',
  `carNo` varchar(32) NOT NULL DEFAULT '0' COMMENT 'ETC卡号',
  `carplateNum` varchar(2000) DEFAULT NULL,
  `carplateType` int(1) unsigned NOT NULL DEFAULT '0' COMMENT '车牌类型 （见系统类型表)',
  `carplateProty1` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '实际天数，余额等信息',
  `carplateProty2` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '0将到期  1已到期',
  `enchargeFlag` int(1) unsigned NOT NULL DEFAULT '0' COMMENT '0不收费  1 收费',
  `serialType` int(1) unsigned NOT NULL DEFAULT '0' COMMENT '0无卡，1有卡 , 255未知',
  `serialNo` varchar(500) NOT NULL DEFAULT '0' COMMENT '出车流水号',
  `inImgName` varchar(50) DEFAULT '',
  `CarColor` varchar(45) NOT NULL DEFAULT '' COMMENT '车身颜色',
  `CarBrand` varchar(45) NOT NULL DEFAULT '' COMMENT '车品牌',
  `RecogEnable` int(8) NOT NULL DEFAULT '0' COMMENT '识别可信度',
  `CarplateColor` varchar(45) NOT NULL DEFAULT '' COMMENT '车牌颜色',
  `CameraId` int(11) NOT NULL DEFAULT '0' COMMENT '照相机ID',
  `remark` varchar(50) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MEMORY DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=9089;

-- 构造表 t_faceinfo
CREATE TABLE IF NOT EXISTS `t_faceinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plateNo` varchar(50) DEFAULT '' COMMENT '车牌号码',
  `faceInfo` text,
  `createTime` datetime DEFAULT NULL,
  `isTemp` int(11) DEFAULT '0' COMMENT '是否临时数据',
  `faceId` varchar(50) DEFAULT '' COMMENT '人脸信息唯一值',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 构造表 t_fcs_seller
CREATE TABLE IF NOT EXISTS `t_fcs_seller` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT '商家ID',
  `seller_name` varchar(50) DEFAULT '' COMMENT '商家名称',
  `seller_code` varchar(50) DEFAULT '' COMMENT '商家编号',
  `pos_x` int(4) DEFAULT '0' COMMENT '坐标X',
  `pos_y` int(4) DEFAULT '0' COMMENT '坐标Y',
  `floor_id` int(8) DEFAULT '0' COMMENT '所属楼层ID',
  `is_delete` int(1) DEFAULT '0' COMMENT '0未删除、1已删除',
  `create_time` datetime DEFAULT NULL COMMENT '添加时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商家信息表';

-- 构造表 t_findcar_events
CREATE TABLE IF NOT EXISTS `t_findcar_events` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `evtType` int(11) NOT NULL DEFAULT '0' COMMENT '类型(0出车事件,1抬杆,2计算费用,3重新抓拍,',
  `imgName` varchar(255) NOT NULL DEFAULT '0' COMMENT '图片名称',
  `dspIp` varchar(32) NOT NULL DEFAULT '0',
  `evtTime` varchar(32) NOT NULL DEFAULT '0' COMMENT '当前事件的时间',
  `inAddr` varchar(32) NOT NULL DEFAULT '0',
  `inTime` varchar(32) NOT NULL DEFAULT '0',
  `outAddr` varchar(32) NOT NULL DEFAULT '0',
  `outTime` varchar(32) NOT NULL DEFAULT '0',
  `money` int(11) NOT NULL DEFAULT '0',
  `carNo` varchar(32) NOT NULL DEFAULT '0' COMMENT 'ETC卡号',
  `carplateNum` varchar(45) NOT NULL DEFAULT '0' COMMENT '车牌',
  `carplateType` int(1) unsigned NOT NULL DEFAULT '0' COMMENT '车牌类型 （见系统类型表)',
  `carplateProty1` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '实际天数，余额等信息',
  `carplateProty2` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '0将到期  1已到期',
  `enchargeFlag` int(1) unsigned NOT NULL DEFAULT '0' COMMENT '0不收费  1 收费',
  `serialType` int(1) unsigned NOT NULL DEFAULT '0' COMMENT '0无卡，1有卡 , 255未知',
  `serialNo` varchar(45) NOT NULL DEFAULT '0' COMMENT '出车流水号',
  `inImgName` varchar(50) DEFAULT '',
  `CarColor` varchar(45) NOT NULL DEFAULT '' COMMENT '车身颜色',
  `CarBrand` varchar(45) NOT NULL DEFAULT '' COMMENT '车品牌',
  `RecogEnable` int(8) NOT NULL DEFAULT '0' COMMENT '识别可信度',
  `CarplateColor` varchar(45) NOT NULL DEFAULT '' COMMENT '车牌颜色',
  `CameraId` int(11) NOT NULL DEFAULT '0' COMMENT '照相机ID',
  `remark` varchar(50) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MEMORY DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=2473;

-- 构造表 t_findcar_upload
CREATE TABLE IF NOT EXISTS `t_findcar_upload` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(20) NOT NULL DEFAULT '' COMMENT '类型标识',
  `uploadTime` datetime DEFAULT NULL COMMENT '上次上报时间',
  `remark` varchar(256) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 构造表 t_ibeacon
CREATE TABLE IF NOT EXISTS `t_ibeacon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lotCode` int(11) NOT NULL DEFAULT '0' COMMENT '车场编号',
  `UUID` varchar(255) NOT NULL DEFAULT '',
  `Major` varchar(255) NOT NULL DEFAULT '',
  `Minor` varchar(255) NOT NULL DEFAULT '',
  `Addr` int(11) NOT NULL DEFAULT '0',
  `PosX` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '蓝牙点X坐标',
  `PosY` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '蓝牙点Y坐标',
  `Mid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '楼层ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_t_ibeacon` (`UUID`,`Major`,`Minor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='蓝牙信息表';

-- 构造表 t_illegal_report
CREATE TABLE IF NOT EXISTS `t_illegal_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `carPlateNum` varchar(50) DEFAULT '' COMMENT '车牌号码',
  `parkTime` datetime DEFAULT NULL COMMENT '停放时间',
  `busNumber` varchar(50) DEFAULT '' COMMENT '车位地址',
  `illegalPlate` varchar(50) DEFAULT '' COMMENT '违停车牌',
  `imgName` varchar(100) DEFAULT '' COMMENT '图片',
  `isAlarm` int(11) NOT NULL DEFAULT '0' COMMENT '是否弹窗过',
  `remark` varchar(512) DEFAULT '' COMMENT '备注',
  `createTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 构造表 t_illegal_spaces
CREATE TABLE IF NOT EXISTS `t_illegal_spaces` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `carPlateNum` varchar(50) DEFAULT '' COMMENT '车牌号码',
  `busNumber` varchar(50) DEFAULT '' COMMENT '车位地址',
  `owner` varchar(100) DEFAULT '' COMMENT '业主',
  `scheme` int(11) DEFAULT '0' COMMENT '违停告警方案',
  `ledIp` varchar(50) DEFAULT '' COMMENT 'LED屏',
  `remark` varchar(512) DEFAULT '' COMMENT '备注',
  `operator` varchar(100) DEFAULT '' COMMENT 'username',
  `createTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 构造表 t_infobus_getinfobus_tmp
CREATE TABLE IF NOT EXISTS `t_infobus_getinfobus_tmp` (
  `id` int(11) NOT NULL DEFAULT '0',
  `BusNumber` varchar(40) DEFAULT '0' COMMENT '车位编号',
  `Addr` int(11) DEFAULT '0' COMMENT '车位地址',
  `state` int(11) DEFAULT '0' COMMENT '0:无车；1有车；2故障',
  `LeaveTime` varchar(40) DEFAULT NULL COMMENT '出场时间',
  `ComeTime` varchar(40) DEFAULT NULL COMMENT '入场时间',
  `CarPlateNum` varchar(50) DEFAULT NULL COMMENT '车牌号码',
  `ImgName` varchar(50) DEFAULT NULL COMMENT '图片名称',
  `AreaID` int(11) DEFAULT '0' COMMENT '区域ID',
  `PreLeaveTime` varchar(40) DEFAULT NULL,
  `PreComeTime` varchar(40) DEFAULT NULL,
  `PreCarplateNum` varchar(50) DEFAULT NULL,
  `CarType` int(11) DEFAULT '0' COMMENT '车位类型',
  `CarplateDigital` varchar(45) DEFAULT NULL,
  `Mid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '地图ID',
  `Trun` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '车位摆向',
  `PosX` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '车位X坐标',
  `PosY` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '车位Y坐标',
  `PSPlaceNum` varchar(30) NOT NULL DEFAULT '' COMMENT '车位编号',
  `PSPlaceName` varchar(30) NOT NULL DEFAULT '' COMMENT '车位名称',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0 未删除,1 已删除',
  `flag` int(1) NOT NULL DEFAULT '0'
) ENGINE=MEMORY DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1422;

-- 构造表 t_keypoint
CREATE TABLE IF NOT EXISTS `t_keypoint` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '路口编号ID',
  `pointType` int(3) NOT NULL DEFAULT '0' COMMENT '类别,1:十字路口;2:查车机;3:车位;4:电梯口',
  `pointName` varchar(50) DEFAULT NULL COMMENT '关键点名称(可放车位ID及编号)',
  `locateX` int(5) NOT NULL DEFAULT '0' COMMENT 'X坐标',
  `locateY` int(5) NOT NULL DEFAULT '0' COMMENT 'Y坐标',
  `lotid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '地图ID',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0未上传；1上传中；2上传成功；3回写成功)',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0 未删除,1 已删除',
  `floorpoint` varchar(255) DEFAULT '' COMMENT '关联的其他楼层电梯口(跨层寻车指定具体电梯口使用)',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='关键点信息表(寻车路线画线用)';

-- 构造表 t_keypointlinks
CREATE TABLE IF NOT EXISTS `t_keypointlinks` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `pointType1` int(1) NOT NULL DEFAULT '0' COMMENT '类别,1:十字路口;2:查车机;3:车位;4:电梯口',
  `pointId1` int(11) NOT NULL COMMENT '第一关键点ID',
  `pointType2` int(1) NOT NULL DEFAULT '0' COMMENT '类别,1:十字路口;2:查车机;3:车位;4:电梯口',
  `pointId2` int(11) NOT NULL COMMENT '第二关键点ID',
  `direction` int(4) NOT NULL DEFAULT '0' COMMENT '关系方向(0:未定义;1:第一关键点到第二关键点单向;2:第二关键点到第一关键点单向;3：第一关键点与第二关键点双向;)',
  `distance` int(11) NOT NULL DEFAULT '0' COMMENT '两点之间的距离',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0未上传；1上传中；2上传成功；3回写成功)',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0:未删除 1:已删除',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='关键点关联表';

-- 构造表 t_led_events
CREATE TABLE IF NOT EXISTS `t_led_events` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `evtType` int(11) NOT NULL DEFAULT '0' COMMENT '类型(0出车事件,1抬杆,2计算费用,3重新抓拍,\r\n4手动抓拍图片返回数据,5停止拍照,6恢复拍照,\r\n7设置ETC配置,\r\n8获取ETC配置\r\n9LED显示剩余车位,\r\n11入口弹窗，需人工确认才进\r\n12手动关闸,13:发送可定制屏指令(致远4S),\r\n14:出入口是否启用\r\n16：找车系统LED屏指令\r\n20：通知入口要重新抓拍(出口时判断是否剩余车位小于0)',
  `imgName` varchar(50) NOT NULL DEFAULT '0' COMMENT '图片名称',
  `dspIp` varchar(32) NOT NULL DEFAULT '0',
  `evtTime` varchar(32) NOT NULL DEFAULT '0' COMMENT '当前事件的时间',
  `inAddr` varchar(32) NOT NULL DEFAULT '0',
  `inTime` varchar(32) NOT NULL DEFAULT '0',
  `outAddr` varchar(32) NOT NULL DEFAULT '0',
  `outTime` varchar(32) NOT NULL DEFAULT '0',
  `money` int(11) NOT NULL DEFAULT '0',
  `carNo` varchar(32) NOT NULL DEFAULT '0' COMMENT 'ETC卡号',
  `carplateNum` varchar(45) NOT NULL DEFAULT '0' COMMENT '车牌',
  `carplateType` int(1) unsigned NOT NULL DEFAULT '0' COMMENT '车牌类型 （见系统类型表)',
  `carplateProty1` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '实际天数，余额等信息',
  `carplateProty2` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '0将到期  1已到期',
  `enchargeFlag` int(1) unsigned NOT NULL DEFAULT '0' COMMENT '0不收费  1 收费',
  `serialType` int(1) unsigned NOT NULL DEFAULT '0' COMMENT '0无卡，1有卡 , 255未知',
  `serialNo` varchar(45) NOT NULL DEFAULT '0' COMMENT '出车流水号',
  `inImgName` varchar(50) DEFAULT '',
  `CarColor` varchar(45) NOT NULL DEFAULT '' COMMENT '车身颜色',
  `CarBrand` varchar(45) NOT NULL DEFAULT '' COMMENT '车品牌',
  `RecogEnable` int(8) NOT NULL DEFAULT '0' COMMENT '识别可信度',
  `CarplateColor` varchar(45) NOT NULL DEFAULT '' COMMENT '车牌颜色',
  `CameraId` int(11) NOT NULL DEFAULT '0' COMMENT '照相机ID',
  `remark` varchar(50) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MEMORY DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1857;

-- 构造表 t_lock_control
CREATE TABLE IF NOT EXISTS `t_lock_control` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `busid` varchar(32) NOT NULL COMMENT '车位编号',
  `action` int(11) NOT NULL COMMENT '0关锁；1开锁',
  `updateTime` datetime NOT NULL COMMENT '记录插入时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='车位锁状态';

-- 构造表 t_lotcarforfee
CREATE TABLE IF NOT EXISTS `t_lotcarforfee` (
  `carNo` varchar(32) NOT NULL,
  `parkTime` datetime NOT NULL,
  `lastUpdate` datetime NOT NULL,
  `imgname` varchar(100) NOT NULL,
  PRIMARY KEY (`carNo`),
  KEY `idx_lotCarForFee_Update` (`lastUpdate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 构造表 t_lotcarforfind
CREATE TABLE IF NOT EXISTS `t_lotcarforfind` (
  `carNo` varchar(32) NOT NULL,
  `carAddr` int(11) NOT NULL COMMENT '车位ID',
  `parkTime` datetime NOT NULL COMMENT '车入场时间',
  `lastUpdate` datetime NOT NULL,
  `carNumber` varchar(8) DEFAULT '',
  `imgName` varchar(50) DEFAULT '',
  `carType` int(2) DEFAULT '0',
  `CarPlateASI` varchar(30) DEFAULT NULL COMMENT '纯数字字母车牌',
  KEY `idx_lotcarforfind_carAddr` (`carAddr`),
  KEY `idx_lotcarforfind_carNoCarAddr` (`carNo`,`carAddr`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 构造表 t_lotcarforfind_area
CREATE TABLE IF NOT EXISTS `t_lotcarforfind_area` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `carNo` varchar(32) NOT NULL,
  `carAddr` int(11) NOT NULL COMMENT '车位ID',
  `parkTime` datetime NOT NULL COMMENT '车入场时间',
  `lastUpdate` datetime NOT NULL,
  `carNumber` varchar(8) DEFAULT '',
  `imgname` varchar(255) DEFAULT NULL COMMENT '车辆照片',
  `CarPlateASI` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `IX_t_lotcarforfind_area_carAddr` (`carAddr`),
  KEY `UK_t_lotcarforfind_area_imgname` (`imgname`),
  KEY `UK_t_lotcarforfind_carNoCarAddr` (`carAddr`,`carNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 构造表 t_parkinglot
CREATE TABLE IF NOT EXISTS `t_parkinglot` (
  `lotId` int(3) NOT NULL AUTO_INCREMENT COMMENT '停车场ID',
  `lotName` varchar(100) NOT NULL COMMENT '停车场名称',
  `bgImgFile` varchar(200) DEFAULT NULL COMMENT '停车场的背景图',
  `areaCount` int(5) NOT NULL DEFAULT '1' COMMENT '本停车场区域数',
  `tollCount` int(11) NOT NULL DEFAULT '0' COMMENT '岗亭数',
  `placeCount` int(5) NOT NULL DEFAULT '0' COMMENT '本停车场停车位数',
  `zoomRate` tinyint(2) NOT NULL DEFAULT '1' COMMENT '放大率',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0未上传；1上传中；2上传成功；3回写成功)',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0 未删除,1 已删除',
  `address` varchar(200) DEFAULT '' COMMENT '车场地址',
  `totalSpace` varchar(200) DEFAULT '' COMMENT '总车位数',
  `tel` varchar(200) DEFAULT '' COMMENT '电话',
  `secret` varchar(200) DEFAULT '' COMMENT '密钥',
  PRIMARY KEY (`lotId`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=48 COMMENT='车场信息表';

-- 构造表 t_power_events
CREATE TABLE IF NOT EXISTS `t_power_events` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `evtType` int(11) NOT NULL DEFAULT '0' COMMENT '类型(0出车事件,1抬杆,2计算费用,3重新抓拍,\r\n4手动抓拍图片返回数据,5停止拍照,6恢复拍照,\r\n7设置ETC配置,\r\n8获取ETC配置\r\n9LED显示剩余车位,\r\n11入口弹窗，需人工确认才进\r\n12手动关闸,13:发送可定制屏指令(致远4S),\r\n14:出入口是否启用\r\n16：找车系统LED屏指令\r\n20：通知入口要重新抓拍(出口时判断是否剩余车位小于0)',
  `imgName` varchar(50) NOT NULL DEFAULT '0' COMMENT '图片名称',
  `dspIp` varchar(32) NOT NULL DEFAULT '0',
  `evtTime` varchar(32) NOT NULL DEFAULT '0' COMMENT '当前事件的时间',
  `inAddr` varchar(32) NOT NULL DEFAULT '0',
  `inTime` varchar(32) NOT NULL DEFAULT '0',
  `outAddr` varchar(32) NOT NULL DEFAULT '0',
  `outTime` varchar(32) NOT NULL DEFAULT '0',
  `money` int(11) NOT NULL DEFAULT '0',
  `carNo` varchar(32) NOT NULL DEFAULT '0' COMMENT 'ETC卡号',
  `carplateNum` varchar(45) NOT NULL DEFAULT '0' COMMENT '车牌',
  `carplateType` int(1) unsigned NOT NULL DEFAULT '0' COMMENT '车牌类型 （见系统类型表)',
  `carplateProty1` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '实际天数，余额等信息',
  `carplateProty2` int(3) unsigned NOT NULL DEFAULT '0' COMMENT '0将到期  1已到期',
  `enchargeFlag` int(1) unsigned NOT NULL DEFAULT '0' COMMENT '0不收费  1 收费',
  `serialType` int(1) unsigned NOT NULL DEFAULT '0' COMMENT '0无卡，1有卡 , 255未知',
  `serialNo` varchar(45) NOT NULL DEFAULT '0' COMMENT '出车流水号',
  `inImgName` varchar(50) DEFAULT '',
  `CarColor` varchar(45) NOT NULL DEFAULT '' COMMENT '车身颜色',
  `CarBrand` varchar(45) NOT NULL DEFAULT '' COMMENT '车品牌',
  `RecogEnable` int(8) NOT NULL DEFAULT '0' COMMENT '识别可信度',
  `CarplateColor` varchar(45) NOT NULL DEFAULT '' COMMENT '车牌颜色',
  `CameraId` int(11) NOT NULL DEFAULT '0' COMMENT '照相机ID',
  `remark` varchar(50) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `idx_events_dspIp` (`dspIp`),
  KEY `idx_events_evtType` (`evtType`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- 构造表 t_service_config
CREATE TABLE IF NOT EXISTS `t_service_config` (
  `id` int(11) NOT NULL,
  `is_separate` tinyint(1) DEFAULT '0' COMMENT '是否寻车收费服务器是分开的(0:否 1:是)',
  `is_sync_parking_data` tinyint(1) DEFAULT '0' COMMENT '是否需要同步寻车系统车位数据及状态数据(0:否 1:是)',
  `is_sync_lock_instruction` tinyint(1) DEFAULT '0' COMMENT '是否需要同步车位锁关锁指令(0:否 1:是)',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统服务配置';

-- 构造表 t_toll_ip
CREATE TABLE IF NOT EXISTS `t_toll_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(20) NOT NULL DEFAULT '' COMMENT '岗亭Ip',
  `createTime` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(256) DEFAULT '' COMMENT '创建者',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 构造表 temp_log_parkcount
CREATE TABLE IF NOT EXISTS `temp_log_parkcount` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT '自动增长',
  `AreaId` int(11) NOT NULL DEFAULT '0' COMMENT '区域ID',
  `AreaName` varchar(50) NOT NULL DEFAULT '' COMMENT '区域名称',
  `ParkDate` datetime DEFAULT NULL COMMENT '停车日期',
  `ParkHour` int(11) NOT NULL DEFAULT '0' COMMENT '停车小时',
  `ParkCount` int(11) NOT NULL DEFAULT '0' COMMENT '占用数',
  `FlowIn` int(11) NOT NULL DEFAULT '0' COMMENT '入车数',
  `FlowOut` int(11) NOT NULL DEFAULT '0' COMMENT '出车数',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0未上传；1上传中；2上传成功；3回写成功)',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0 未删除,1 已删除',
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='车流量统计表';

-- 构造表 user
CREATE TABLE IF NOT EXISTS `user` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `LoginName` varchar(45) NOT NULL COMMENT '登陆账号',
  `Pwd` varchar(45) NOT NULL COMMENT '登陆密码',
  `URight` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '用户权限(0:普通用户 1:管理员)',
  `lastlogintime` varchar(40) DEFAULT NULL COMMENT '最后登陆时间',
  `UserType` int(11) DEFAULT '0' COMMENT '用户类型(0:后台账户 1:找车机账户)',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=8192;

-- ===============全量更新所有表字段===============
-- 更新表 areapointled 所有字段和索引
CALL add_element_unless_exists('column', 'areapointled', 'Lid', 'ALTER TABLE areapointled ADD COLUMN `Lid` int(11) DEFAULT "0" COMMENT "屏ID";');
CALL add_element_unless_exists('column', 'areapointled', 'Aid', 'ALTER TABLE areapointled ADD COLUMN `Aid` int(11) DEFAULT "0" COMMENT "区域ID" AFTER Lid;');

-- 更新表 buspointled 所有字段和索引
CALL add_element_unless_exists('column', 'buspointled', 'PAddr', 'ALTER TABLE buspointled ADD COLUMN `PAddr` int(11) DEFAULT NULL COMMENT "车位地址";');
CALL add_element_unless_exists('column', 'buspointled', 'LAddr', 'ALTER TABLE buspointled ADD COLUMN `LAddr` int(11) DEFAULT NULL COMMENT "屏地址" AFTER PAddr;');
CALL add_element_unless_exists('column', 'buspointled', 'pid', 'ALTER TABLE buspointled ADD COLUMN `pid` int(11) DEFAULT "0" COMMENT "车位ID" AFTER LAddr;');
CALL add_element_unless_exists('column', 'buspointled', 'lid', 'ALTER TABLE buspointled ADD COLUMN `lid` int(11) DEFAULT "0" COMMENT "屏ID" AFTER pid;');

-- 更新表 buspointrecorder 所有字段和索引
CALL add_element_unless_exists('column', 'buspointrecorder', 'Paddr', 'ALTER TABLE buspointrecorder ADD COLUMN `Paddr` int(11) DEFAULT "0" COMMENT "车位地址";');
CALL add_element_unless_exists('column', 'buspointrecorder', 'Rid', 'ALTER TABLE buspointrecorder ADD COLUMN `Rid` int(11) DEFAULT "0" COMMENT "刻录机ID" AFTER Paddr;');
CALL add_element_unless_exists('column', 'buspointrecorder', 'Rport', 'ALTER TABLE buspointrecorder ADD COLUMN `Rport` int(11) DEFAULT "0" COMMENT "刻录机_哪一路" AFTER Rid;');

-- 更新表 carcolor 所有字段和索引
CALL add_element_unless_exists('column', 'carcolor', 'LedOne', 'ALTER TABLE carcolor ADD COLUMN `LedOne` int(10) unsigned DEFAULT "0" COMMENT "灯一颜色(已停用)";');
CALL add_element_unless_exists('column', 'carcolor', 'LedTwo', 'ALTER TABLE carcolor ADD COLUMN `LedTwo` int(10) unsigned DEFAULT "0" COMMENT "灯二颜色(已停用)" AFTER LedOne;');
CALL add_element_unless_exists('column', 'carcolor', 'ACar', 'ALTER TABLE carcolor ADD COLUMN `ACar` int(10) unsigned DEFAULT "0" COMMENT "有车时灯颜色(0当前颜色不变；1红；2绿；3蓝；4橙；5黄；6青；7紫；8白；10不亮)" AFTER LedTwo;');
CALL add_element_unless_exists('column', 'carcolor', 'NoCar', 'ALTER TABLE carcolor ADD COLUMN `NoCar` int(10) unsigned DEFAULT "0" COMMENT "无车时灯颜色(0当前颜色不变；1红；2绿；3蓝；4橙；5黄；6青；7紫；8白；10不亮)" AFTER ACar;');
CALL add_element_unless_exists('column', 'carcolor', 'CarType', 'ALTER TABLE carcolor ADD COLUMN `CarType` int(10) unsigned DEFAULT "0" COMMENT "车位类型标识 0:Ordinary 1:Monthly2:Disabled" AFTER NoCar;');
CALL add_element_unless_exists('column', 'carcolor', 'TypeNamect', 'ALTER TABLE carcolor ADD COLUMN `TypeNamect` varchar(45) DEFAULT "" COMMENT "类型名称(中文)" AFTER CarType;');
CALL add_element_unless_exists('column', 'carcolor', 'TypeNameen', 'ALTER TABLE carcolor ADD COLUMN `TypeNameen` varchar(45) DEFAULT "" COMMENT "类型名称(英文)" AFTER TypeNamect;');
CALL add_element_unless_exists('column', 'carcolor', 'IfCount', 'ALTER TABLE carcolor ADD COLUMN `IfCount` int(11) DEFAULT "0" COMMENT "是否参与屏计数 0:不统计 1:统计" AFTER TypeNameen;');

-- 更新表 carfindencrypt 所有字段和索引
CALL add_element_unless_exists('column', 'carfindencrypt', 'CarNum', 'ALTER TABLE carfindencrypt ADD COLUMN `CarNum` varchar(10) NOT NULL DEFAULT "" COMMENT "车牌号码";');
CALL add_element_unless_exists('column', 'carfindencrypt', 'password', 'ALTER TABLE carfindencrypt ADD COLUMN `password` varchar(10) NOT NULL DEFAULT "" COMMENT "查询密码" AFTER CarNum;');
CALL add_element_unless_exists('column', 'carfindencrypt', 'ValidityFromDate', 'ALTER TABLE carfindencrypt ADD COLUMN `ValidityFromDate` datetime DEFAULT NULL COMMENT "有效日期从" AFTER password;');
CALL add_element_unless_exists('column', 'carfindencrypt', 'ValidityToDate', 'ALTER TABLE carfindencrypt ADD COLUMN `ValidityToDate` datetime DEFAULT NULL COMMENT "有效日期至" AFTER ValidityFromDate;');
CALL add_element_unless_exists('column', 'carfindencrypt', 'CreateTime', 'ALTER TABLE carfindencrypt ADD COLUMN `CreateTime` datetime DEFAULT NULL COMMENT "创建时间" AFTER ValidityToDate;');
CALL add_element_unless_exists('index', 'carfindencrypt', 'idx_carfindencrypt_CarNum', 'ALTER TABLE carfindencrypt ADD INDEX idx_carfindencrypt_CarNum (CarNum) USING BTREE');

-- 更新表 columns_priv 所有字段和索引
CALL add_element_unless_exists('column', 'columns_priv', 'Db', 'ALTER TABLE columns_priv ADD COLUMN `Db` char(64) COLLATE utf8_bin NOT NULL DEFAULT "";');
CALL add_element_unless_exists('column', 'columns_priv', 'User', 'ALTER TABLE columns_priv ADD COLUMN `User` char(16) COLLATE utf8_bin NOT NULL DEFAULT "" AFTER Db;');
CALL add_element_unless_exists('column', 'columns_priv', 'Table_name', 'ALTER TABLE columns_priv ADD COLUMN `Table_name` char(64) COLLATE utf8_bin NOT NULL DEFAULT "" AFTER User;');
CALL add_element_unless_exists('column', 'columns_priv', 'Column_name', 'ALTER TABLE columns_priv ADD COLUMN `Column_name` char(64) COLLATE utf8_bin NOT NULL DEFAULT "" AFTER Table_name;');

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
  `BusNumber` varchar(40) DEFAULT '0' COMMENT '车位编号',
  `Addr` int(11) DEFAULT '0' COMMENT '车位地址',
  `state` int(11) DEFAULT '0' COMMENT '0:无车；1有车；2故障',
  `LeaveTime` varchar(40) DEFAULT NULL COMMENT '出场时间',
  `ComeTime` varchar(40) DEFAULT NULL COMMENT '入场时间',
  `carplatenum` varchar(50) DEFAULT NULL COMMENT '车牌号码',
  `lastCarPlateNum` varchar(50) DEFAULT '' COMMENT '上一次入车车牌',
  `ImgName` varchar(50) DEFAULT NULL COMMENT '图片名称',
  `lastImgName` varchar(50) DEFAULT '' COMMENT '上一次入车的车辆图片名称',
  `AreaID` int(11) DEFAULT '0' COMMENT '区域ID',
  `Flag` int(10) unsigned NOT NULL DEFAULT '0',
  `PreLeaveTime` varchar(40) DEFAULT NULL,
  `PreComeTime` varchar(40) DEFAULT NULL,
  `PreCarplateNum` varchar(50) DEFAULT NULL,
  `CarType` int(11) DEFAULT '0' COMMENT '车位类型',
  `ifchange` int(11) DEFAULT '0',
  `ifsend` int(11) DEFAULT '0',
  `CarplateDigital` varchar(45) DEFAULT NULL,
  `Mid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '地图ID',
  `Trun` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '车位摆向',
  `PosX` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '车位X坐标',
  `PosY` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '车位Y坐标',
  `IfSetRoute` varchar(255) DEFAULT '0' COMMENT '1-预设路线 0-自动路线',
  `PSPlaceNum` varchar(30) NOT NULL DEFAULT '' COMMENT '车位编号',
  `PSPlaceName` varchar(30) NOT NULL DEFAULT '' COMMENT '车位名称',
  `WDCloudFlag` int(4) NOT NULL DEFAULT '0' COMMENT '万达云上传标志：0未上传；1已上传',
  `WDCloudDate` datetime DEFAULT NULL COMMENT '云异动时间',
  `parktype` int(1) DEFAULT '0' COMMENT '0普通车位，1产权车位',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0未上传；1上传中；2上传成功；3回写成功)',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0 未删除,1 已删除',
  `LightType` int(11) DEFAULT '0' COMMENT '灯方案_灯指令',
  `LightSend` int(11) DEFAULT '0' COMMENT '是否发送灯指令 0:否 1:是',
  `LightFree` int(11) DEFAULT '0' COMMENT '0当前颜色不变;1红;2绿;3蓝;4橙;5黄;6青;7紫;8白;11红闪;12绿闪;13蓝闪;14橙闪;15黄闪;16青闪;17紫闪;18白闪;10 不亮灯',
  `LightOcc` int(11) DEFAULT '0' COMMENT '0当前颜色不变;1红;2绿;3蓝;4橙;5黄;6青;7紫;8白;11红闪;12绿闪;13蓝闪;14橙闪;15黄闪;16青闪;17紫闪;18白闪;10 不亮灯',
  `LightErr` int(11) DEFAULT '0' COMMENT '0当前颜色不变;1红;2绿;3蓝;4橙;5黄;6青;7紫;8白;11红闪;12绿闪;13蓝闪;14橙闪;15黄闪;16青闪;17紫闪;18白闪;',
  `CarPlateASI` varchar(30) DEFAULT NULL COMMENT '纯数字字母车牌',
  `ClientUpdateTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `IDX_BusNo_CarNo` (`BusNumber`,`carplatenum`),
  KEY `Idx_infobus_Addr_AreaId` (`Addr`,`AreaID`),
  KEY `IX_infobus` (`Addr`,`state`),
  KEY `IX_infobus_Addr` (`Addr`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='车位信息表';

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=16384 COMMENT='找车机常用参数表';

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
  `Mapname` varchar(30) NOT NULL DEFAULT '' COMMENT '中文地图名称',
  `MapName2` varchar(30) DEFAULT '' COMMENT '英文地图名称',
  `MapName3` varchar(30) DEFAULT '' COMMENT '其他地图名称',
  `Mapfile` varchar(60) NOT NULL DEFAULT '' COMMENT '地图文件',
  `Big` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '车位放大率(新版寻车系统网页已停用)',
  `FloorPoint` varchar(50) NOT NULL DEFAULT '' COMMENT '(已停用)',
  `MapDeclare` varchar(50) NOT NULL DEFAULT '' COMMENT '(已停用)',
  `SpaceL` int(8) NOT NULL DEFAULT '0' COMMENT '车位长',
  `SpaceW` int(8) NOT NULL DEFAULT '0' COMMENT '车位宽',
  `orderNo` tinyint(4) NOT NULL DEFAULT '0' COMMENT '排序字段',
  `CliDate` datetime DEFAULT NULL COMMENT '上传日期',
  `CliFlag` int(8) NOT NULL DEFAULT '0' COMMENT '上传标志(0:未上传 1:上传中 2:上传成功 3:回写成功)',
  `total` int(11) DEFAULT '0' COMMENT '楼层总车位数',
  `Type` varchar(255) DEFAULT NULL COMMENT '楼层类型(1:带车位楼层 2:带商家楼层)',
  `MapCode` varchar(50) DEFAULT '' COMMENT '楼层编码',
  `IsDelete` int(1) NOT NULL DEFAULT '0' COMMENT '0:未删除 1:已删除',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='车场楼层信息表';

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=2048 COMMENT='系统常用参数配置表';

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=655 COMMENT='登录日志';

-- 构造表 log_operate
CREATE TABLE IF NOT EXISTS `log_operate` (
  `ope_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '操作ID',
  `ope_user_id` varchar(11) DEFAULT NULL COMMENT '操作用户',
  `ope_time` datetime DEFAULT NULL COMMENT '操作时间',
  `ope_ip` varchar(50) DEFAULT NULL COMMENT '操作ip',
  `ope_action` int(1) DEFAULT NULL COMMENT '操作行为 (1=新增 2=删除 3=修改)',
  `ope_content` longtext COMMENT '操作内容',
  PRIMARY KEY (`ope_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=3510 COMMENT='操作日志';

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=16384;

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
) ENGINE=InnoDB AUTO_INCREMENT=1825 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=137 COMMENT='系统授权';

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
) ENGINE=InnoDB AUTO_INCREMENT=790 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=192 COMMENT='国际化消息表';

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=321 COMMENT='系统模块信息表';

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=413 COMMENT='系统功能节点表';

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=16384 COMMENT='系统组织机构基本信息表';

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=4096 COMMENT='系统用户所属组织机构关联表';

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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=4096 COMMENT='系统角色与用户关联表';

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=3276 COMMENT='系统用户基本信息表';

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
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
) ENGINE=MEMORY DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1857;

-- 构造表 t_findcar_upload
CREATE TABLE IF NOT EXISTS `t_findcar_upload` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(20) NOT NULL DEFAULT '' COMMENT '类型标识',
  `uploadTime` datetime DEFAULT NULL COMMENT '上次上报时间',
  `remark` varchar(256) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=16384 COMMENT='系统服务配置';

-- 构造表 t_toll_ip
CREATE TABLE IF NOT EXISTS `t_toll_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(20) NOT NULL DEFAULT '' COMMENT '岗亭Ip',
  `createTime` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(256) DEFAULT '' COMMENT '创建者',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
) ENGINE=MyISAM AUTO_INCREMENT=88 DEFAULT CHARSET=utf8 COMMENT='车流量统计表';

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
CALL add_element_unless_exists('column', 'areapointled', 'ID', 'ALTER TABLE areapointled ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'areapointled', 'Lid', 'ALTER TABLE areapointled ADD COLUMN `Lid` int(11) NULL DEFAULT 0 AFTER `ID`;');
CALL add_element_unless_exists('column', 'areapointled', 'Aid', 'ALTER TABLE areapointled ADD COLUMN `Aid` int(11) NULL DEFAULT 0 AFTER `Lid`;');
CALL add_element_unless_exists('index', 'areapointled', 'PRIMARY', 'ALTER TABLE areapointled ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 buspointled 所有字段和索引
CALL add_element_unless_exists('column', 'buspointled', 'ID', 'ALTER TABLE buspointled ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'buspointled', 'PAddr', 'ALTER TABLE buspointled ADD COLUMN `PAddr` int(11) NULL AFTER `ID`;');
CALL add_element_unless_exists('column', 'buspointled', 'LAddr', 'ALTER TABLE buspointled ADD COLUMN `LAddr` int(11) NULL AFTER `PAddr`;');
CALL add_element_unless_exists('column', 'buspointled', 'pid', 'ALTER TABLE buspointled ADD COLUMN `pid` int(11) NULL DEFAULT 0 AFTER `LAddr`;');
CALL add_element_unless_exists('column', 'buspointled', 'lid', 'ALTER TABLE buspointled ADD COLUMN `lid` int(11) NULL DEFAULT 0 AFTER `pid`;');
CALL add_element_unless_exists('index', 'buspointled', 'PRIMARY', 'ALTER TABLE buspointled ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 buspointrecorder 所有字段和索引
CALL add_element_unless_exists('column', 'buspointrecorder', 'ID', 'ALTER TABLE buspointrecorder ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'buspointrecorder', 'Paddr', 'ALTER TABLE buspointrecorder ADD COLUMN `Paddr` int(11) NULL DEFAULT 0 AFTER `ID`;');
CALL add_element_unless_exists('column', 'buspointrecorder', 'Rid', 'ALTER TABLE buspointrecorder ADD COLUMN `Rid` int(11) NULL DEFAULT 0 AFTER `Paddr`;');
CALL add_element_unless_exists('column', 'buspointrecorder', 'Rport', 'ALTER TABLE buspointrecorder ADD COLUMN `Rport` int(11) NULL DEFAULT 0 AFTER `Rid`;');
CALL add_element_unless_exists('index', 'buspointrecorder', 'PRIMARY', 'ALTER TABLE buspointrecorder ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 carcolor 所有字段和索引
CALL add_element_unless_exists('column', 'carcolor', 'ID', 'ALTER TABLE carcolor ADD COLUMN `ID` int(10) unsigned NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'carcolor', 'LedOne', 'ALTER TABLE carcolor ADD COLUMN `LedOne` int(10) unsigned NULL DEFAULT 0 AFTER `ID`;');
CALL add_element_unless_exists('column', 'carcolor', 'LedTwo', 'ALTER TABLE carcolor ADD COLUMN `LedTwo` int(10) unsigned NULL DEFAULT 0 AFTER `LedOne`;');
CALL add_element_unless_exists('column', 'carcolor', 'ACar', 'ALTER TABLE carcolor ADD COLUMN `ACar` int(10) unsigned NULL DEFAULT 0 AFTER `LedTwo`;');
CALL add_element_unless_exists('column', 'carcolor', 'NoCar', 'ALTER TABLE carcolor ADD COLUMN `NoCar` int(10) unsigned NULL DEFAULT 0 AFTER `ACar`;');
CALL add_element_unless_exists('column', 'carcolor', 'CarType', 'ALTER TABLE carcolor ADD COLUMN `CarType` int(10) unsigned NULL DEFAULT 0 AFTER `NoCar`;');
CALL add_element_unless_exists('column', 'carcolor', 'TypeNamect', 'ALTER TABLE carcolor ADD COLUMN `TypeNamect` varchar(45) NULL DEFAULT AFTER `CarType`;');
CALL add_element_unless_exists('column', 'carcolor', 'TypeNameen', 'ALTER TABLE carcolor ADD COLUMN `TypeNameen` varchar(45) NULL DEFAULT AFTER `TypeNamect`;');
CALL add_element_unless_exists('column', 'carcolor', 'IfCount', 'ALTER TABLE carcolor ADD COLUMN `IfCount` int(11) NULL DEFAULT 0 AFTER `TypeNameen`;');
CALL add_element_unless_exists('index', 'carcolor', 'PRIMARY', 'ALTER TABLE carcolor ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 carfindencrypt 所有字段和索引
CALL add_element_unless_exists('column', 'carfindencrypt', 'id', 'ALTER TABLE carfindencrypt ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'carfindencrypt', 'CarNum', 'ALTER TABLE carfindencrypt ADD COLUMN `CarNum` varchar(10) NOT NULL DEFAULT AFTER `id`;');
CALL add_element_unless_exists('column', 'carfindencrypt', 'password', 'ALTER TABLE carfindencrypt ADD COLUMN `password` varchar(10) NOT NULL DEFAULT AFTER `CarNum`;');
CALL add_element_unless_exists('column', 'carfindencrypt', 'ValidityFromDate', 'ALTER TABLE carfindencrypt ADD COLUMN `ValidityFromDate` datetime NULL AFTER `password`;');
CALL add_element_unless_exists('column', 'carfindencrypt', 'ValidityToDate', 'ALTER TABLE carfindencrypt ADD COLUMN `ValidityToDate` datetime NULL AFTER `ValidityFromDate`;');
CALL add_element_unless_exists('column', 'carfindencrypt', 'CreateTime', 'ALTER TABLE carfindencrypt ADD COLUMN `CreateTime` datetime NULL AFTER `ValidityToDate`;');
CALL add_element_unless_exists('index', 'carfindencrypt', 'PRIMARY', 'ALTER TABLE carfindencrypt ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');
CALL add_element_unless_exists('index', 'carfindencrypt', 'idx_carfindencrypt_CarNum', 'ALTER TABLE carfindencrypt ADD INDEX INDEX `idx_carfindencrypt_CarNum` (`CarNum`) USING BTREE;');

-- 更新表 columns_priv 所有字段和索引
CALL add_element_unless_exists('column', 'columns_priv', 'Host', 'ALTER TABLE columns_priv ADD COLUMN `Host` char(60) NOT NULL DEFAULT;');
CALL add_element_unless_exists('column', 'columns_priv', 'Db', 'ALTER TABLE columns_priv ADD COLUMN `Db` char(64) NOT NULL DEFAULT AFTER `Host`;');
CALL add_element_unless_exists('column', 'columns_priv', 'User', 'ALTER TABLE columns_priv ADD COLUMN `User` char(16) NOT NULL DEFAULT AFTER `Db`;');
CALL add_element_unless_exists('column', 'columns_priv', 'Table_name', 'ALTER TABLE columns_priv ADD COLUMN `Table_name` char(64) NOT NULL DEFAULT AFTER `User`;');
CALL add_element_unless_exists('column', 'columns_priv', 'Column_name', 'ALTER TABLE columns_priv ADD COLUMN `Column_name` char(64) NOT NULL DEFAULT AFTER `Table_name`;');
CALL add_element_unless_exists('column', 'columns_priv', 'Timestamp', 'ALTER TABLE columns_priv ADD COLUMN `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP AFTER `Column_name`;');
CALL add_element_unless_exists('column', 'columns_priv', 'Column_priv', 'ALTER TABLE columns_priv ADD COLUMN `Column_priv` set(\'Select\',\'Insert\',\'Update\',\'References\') NOT NULL AFTER `Timestamp`;');
CALL add_element_unless_exists('index', 'columns_priv', 'PRIMARY', 'ALTER TABLE columns_priv ADD UNIQUE INDEX `PRIMARY` (`Host`) USING BTREE;');
CALL add_element_unless_exists('index', 'columns_priv', 'PRIMARY', 'ALTER TABLE columns_priv ADD UNIQUE INDEX `PRIMARY` (`Db`) USING BTREE;');
CALL add_element_unless_exists('index', 'columns_priv', 'PRIMARY', 'ALTER TABLE columns_priv ADD UNIQUE INDEX `PRIMARY` (`User`) USING BTREE;');
CALL add_element_unless_exists('index', 'columns_priv', 'PRIMARY', 'ALTER TABLE columns_priv ADD UNIQUE INDEX `PRIMARY` (`Table_name`) USING BTREE;');
CALL add_element_unless_exists('index', 'columns_priv', 'PRIMARY', 'ALTER TABLE columns_priv ADD UNIQUE INDEX `PRIMARY` (`Column_name`) USING BTREE;');

-- 更新表 controlset 所有字段和索引
CALL add_element_unless_exists('column', 'controlset', 'ID', 'ALTER TABLE controlset ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'controlset', 'LNumber', 'ALTER TABLE controlset ADD COLUMN `LNumber` varchar(50) NULL DEFAULT AFTER `ID`;');
CALL add_element_unless_exists('column', 'controlset', 'Location', 'ALTER TABLE controlset ADD COLUMN `Location` varchar(50) NULL DEFAULT 0 AFTER `LNumber`;');
CALL add_element_unless_exists('column', 'controlset', 'Direction', 'ALTER TABLE controlset ADD COLUMN `Direction` varchar(50) NULL DEFAULT 0 AFTER `Location`;');
CALL add_element_unless_exists('column', 'controlset', 'Color', 'ALTER TABLE controlset ADD COLUMN `Color` varchar(50) NULL DEFAULT 3 AFTER `Direction`;');
CALL add_element_unless_exists('column', 'controlset', 'BusType', 'ALTER TABLE controlset ADD COLUMN `BusType` varchar(50) NULL DEFAULT 1 AFTER `Color`;');
CALL add_element_unless_exists('index', 'controlset', 'PRIMARY', 'ALTER TABLE controlset ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 cy2 所有字段和索引
CALL add_element_unless_exists('column', 'cy2', 'ID', 'ALTER TABLE cy2 ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'cy2', 'CIP', 'ALTER TABLE cy2 ADD COLUMN `CIP` varchar(50) NOT NULL AFTER `ID`;');
CALL add_element_unless_exists('column', 'cy2', 'OtherMid', 'ALTER TABLE cy2 ADD COLUMN `OtherMid` int(11) unsigned NOT NULL AFTER `CIP`;');
CALL add_element_unless_exists('column', 'cy2', 'FloorPoint', 'ALTER TABLE cy2 ADD COLUMN `FloorPoint` varchar(50) NOT NULL AFTER `OtherMid`;');
CALL add_element_unless_exists('column', 'cy2', 'fstate', 'ALTER TABLE cy2 ADD COLUMN `fstate` int(11) unsigned NOT NULL DEFAULT 1 AFTER `FloorPoint`;');
CALL add_element_unless_exists('column', 'cy2', 'otherselfmac', 'ALTER TABLE cy2 ADD COLUMN `otherselfmac` int(10) NOT NULL DEFAULT 0 AFTER `fstate`;');
CALL add_element_unless_exists('column', 'cy2', 'DirType', 'ALTER TABLE cy2 ADD COLUMN `DirType` int(1) NOT NULL DEFAULT 0 AFTER `otherselfmac`;');
CALL add_element_unless_exists('column', 'cy2', 'CliFlag', 'ALTER TABLE cy2 ADD COLUMN `CliFlag` int(8) NOT NULL DEFAULT 0 AFTER `DirType`;');
CALL add_element_unless_exists('column', 'cy2', 'CliDate', 'ALTER TABLE cy2 ADD COLUMN `CliDate` datetime NULL AFTER `CliFlag`;');
CALL add_element_unless_exists('column', 'cy2', 'IsDelete', 'ALTER TABLE cy2 ADD COLUMN `IsDelete` int(1) NOT NULL DEFAULT 0 AFTER `CliDate`;');
CALL add_element_unless_exists('index', 'cy2', 'PRIMARY', 'ALTER TABLE cy2 ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 cy_cx_a 所有字段和索引
CALL add_element_unless_exists('column', 'cy_cx_a', 'ID', 'ALTER TABLE cy_cx_a ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'CName', 'ALTER TABLE cy_cx_a ADD COLUMN `CName` varchar(50) NOT NULL DEFAULT AFTER `ID`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'CIP', 'ALTER TABLE cy_cx_a ADD COLUMN `CIP` varchar(50) NOT NULL DEFAULT AFTER `CName`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'MID', 'ALTER TABLE cy_cx_a ADD COLUMN `MID` int(11) NOT NULL DEFAULT 0 AFTER `CIP`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'lukou', 'ALTER TABLE cy_cx_a ADD COLUMN `lukou` int(11) NOT NULL DEFAULT 0 AFTER `MID`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'mapfile', 'ALTER TABLE cy_cx_a ADD COLUMN `mapfile` varchar(45) NOT NULL DEFAULT AFTER `lukou`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'angle', 'ALTER TABLE cy_cx_a ADD COLUMN `angle` int(11) NOT NULL DEFAULT 0 AFTER `mapfile`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'Direction', 'ALTER TABLE cy_cx_a ADD COLUMN `Direction` int(6) NOT NULL DEFAULT 45 AFTER `angle`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'PosX', 'ALTER TABLE cy_cx_a ADD COLUMN `PosX` int(11) NOT NULL DEFAULT 0 AFTER `Direction`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'PosY', 'ALTER TABLE cy_cx_a ADD COLUMN `PosY` int(11) NOT NULL DEFAULT 0 AFTER `PosX`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'AreaId', 'ALTER TABLE cy_cx_a ADD COLUMN `AreaId` int(11) NOT NULL DEFAULT 0 AFTER `PosY`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'CliFlag', 'ALTER TABLE cy_cx_a ADD COLUMN `CliFlag` int(8) NOT NULL DEFAULT 0 AFTER `AreaId`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'CliDate', 'ALTER TABLE cy_cx_a ADD COLUMN `CliDate` datetime NULL AFTER `CliFlag`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'IsDelete', 'ALTER TABLE cy_cx_a ADD COLUMN `IsDelete` int(1) NOT NULL DEFAULT 0 AFTER `CliDate`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'route_ip', 'ALTER TABLE cy_cx_a ADD COLUMN `route_ip` varchar(50) NULL DEFAULT AFTER `IsDelete`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'up_point', 'ALTER TABLE cy_cx_a ADD COLUMN `up_point` varchar(50) NULL DEFAULT AFTER `route_ip`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'down_point', 'ALTER TABLE cy_cx_a ADD COLUMN `down_point` varchar(50) NULL DEFAULT AFTER `up_point`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'left_point', 'ALTER TABLE cy_cx_a ADD COLUMN `left_point` varchar(50) NULL DEFAULT AFTER `down_point`;');
CALL add_element_unless_exists('column', 'cy_cx_a', 'right_point', 'ALTER TABLE cy_cx_a ADD COLUMN `right_point` varchar(50) NULL DEFAULT AFTER `left_point`;');
CALL add_element_unless_exists('index', 'cy_cx_a', 'PRIMARY', 'ALTER TABLE cy_cx_a ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 dspinfolog 所有字段和索引
CALL add_element_unless_exists('column', 'dspinfolog', 'ID', 'ALTER TABLE dspinfolog ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'dspinfolog', 'CarplateNum', 'ALTER TABLE dspinfolog ADD COLUMN `CarplateNum` varchar(50) NULL DEFAULT AFTER `ID`;');
CALL add_element_unless_exists('column', 'dspinfolog', 'CarAddr', 'ALTER TABLE dspinfolog ADD COLUMN `CarAddr` int(11) NULL DEFAULT 0 AFTER `CarplateNum`;');
CALL add_element_unless_exists('column', 'dspinfolog', 'ImgName', 'ALTER TABLE dspinfolog ADD COLUMN `ImgName` varchar(100) NULL DEFAULT AFTER `CarAddr`;');
CALL add_element_unless_exists('column', 'dspinfolog', 'PdataTime', 'ALTER TABLE dspinfolog ADD COLUMN `PdataTime` varchar(40) NULL AFTER `ImgName`;');
CALL add_element_unless_exists('index', 'dspinfolog', 'PRIMARY', 'ALTER TABLE dspinfolog ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');
CALL add_element_unless_exists('index', 'dspinfolog', 'IDX_dspinfolog', 'ALTER TABLE dspinfolog ADD INDEX INDEX `IDX_dspinfolog` (`CarAddr`) USING BTREE;');
CALL add_element_unless_exists('index', 'dspinfolog', 'IDX_dspinfolog', 'ALTER TABLE dspinfolog ADD INDEX INDEX `IDX_dspinfolog` (`PdataTime`) USING BTREE;');
CALL add_element_unless_exists('index', 'dspinfolog', 'IDX_dspinfolog_PdataTime', 'ALTER TABLE dspinfolog ADD INDEX INDEX `IDX_dspinfolog_PdataTime` (`PdataTime`) USING BTREE;');

-- 更新表 infoarea 所有字段和索引
CALL add_element_unless_exists('column', 'infoarea', 'ID', 'ALTER TABLE infoarea ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'infoarea', 'AreaName', 'ALTER TABLE infoarea ADD COLUMN `AreaName` varchar(30) NOT NULL DEFAULT AFTER `ID`;');
CALL add_element_unless_exists('column', 'infoarea', 'AreaName2', 'ALTER TABLE infoarea ADD COLUMN `AreaName2` varchar(30) NOT NULL DEFAULT AFTER `AreaName`;');
CALL add_element_unless_exists('column', 'infoarea', 'MapId', 'ALTER TABLE infoarea ADD COLUMN `MapId` int(11) NULL DEFAULT 0 AFTER `AreaName2`;');
CALL add_element_unless_exists('column', 'infoarea', 'MapName', 'ALTER TABLE infoarea ADD COLUMN `MapName` varchar(30) NULL DEFAULT AFTER `MapId`;');
CALL add_element_unless_exists('column', 'infoarea', 'CliDate', 'ALTER TABLE infoarea ADD COLUMN `CliDate` datetime NULL AFTER `MapName`;');
CALL add_element_unless_exists('column', 'infoarea', 'CliFlag', 'ALTER TABLE infoarea ADD COLUMN `CliFlag` int(8) NOT NULL DEFAULT 0 AFTER `CliDate`;');
CALL add_element_unless_exists('column', 'infoarea', 'IsDelete', 'ALTER TABLE infoarea ADD COLUMN `IsDelete` int(1) NOT NULL DEFAULT 0 AFTER `CliFlag`;');
CALL add_element_unless_exists('column', 'infoarea', 'PosX', 'ALTER TABLE infoarea ADD COLUMN `PosX` int(11) NULL DEFAULT 0 AFTER `IsDelete`;');
CALL add_element_unless_exists('column', 'infoarea', 'PosY', 'ALTER TABLE infoarea ADD COLUMN `PosY` int(11) NULL DEFAULT 0 AFTER `PosX`;');
CALL add_element_unless_exists('column', 'infoarea', 'TotalNum', 'ALTER TABLE infoarea ADD COLUMN `TotalNum` int(11) NULL DEFAULT 0 AFTER `PosY`;');
CALL add_element_unless_exists('column', 'infoarea', 'FreeNum', 'ALTER TABLE infoarea ADD COLUMN `FreeNum` int(11) NULL DEFAULT 0 AFTER `TotalNum`;');
CALL add_element_unless_exists('column', 'infoarea', 'AreaType', 'ALTER TABLE infoarea ADD COLUMN `AreaType` int(11) NULL DEFAULT 0 AFTER `FreeNum`;');
CALL add_element_unless_exists('column', 'infoarea', 'LimitNum', 'ALTER TABLE infoarea ADD COLUMN `LimitNum` int(11) NULL DEFAULT 0 AFTER `AreaType`;');
CALL add_element_unless_exists('column', 'infoarea', 'AreaName3', 'ALTER TABLE infoarea ADD COLUMN `AreaName3` varchar(30) NULL DEFAULT AFTER `LimitNum`;');
CALL add_element_unless_exists('column', 'infoarea', 'ClientUpdateTime', 'ALTER TABLE infoarea ADD COLUMN `ClientUpdateTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP AFTER `AreaName3`;');
CALL add_element_unless_exists('index', 'infoarea', 'PRIMARY', 'ALTER TABLE infoarea ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 infobus 所有字段和索引
CALL add_element_unless_exists('column', 'infobus', 'ID', 'ALTER TABLE infobus ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'infobus', 'BusNumber', 'ALTER TABLE infobus ADD COLUMN `BusNumber` varchar(40) NULL DEFAULT 0 AFTER `ID`;');
CALL add_element_unless_exists('column', 'infobus', 'Addr', 'ALTER TABLE infobus ADD COLUMN `Addr` int(11) NULL DEFAULT 0 AFTER `BusNumber`;');
CALL add_element_unless_exists('column', 'infobus', 'state', 'ALTER TABLE infobus ADD COLUMN `state` int(11) NULL DEFAULT 0 AFTER `Addr`;');
CALL add_element_unless_exists('column', 'infobus', 'LeaveTime', 'ALTER TABLE infobus ADD COLUMN `LeaveTime` varchar(40) NULL AFTER `state`;');
CALL add_element_unless_exists('column', 'infobus', 'ComeTime', 'ALTER TABLE infobus ADD COLUMN `ComeTime` varchar(40) NULL AFTER `LeaveTime`;');
CALL add_element_unless_exists('column', 'infobus', 'carplatenum', 'ALTER TABLE infobus ADD COLUMN `carplatenum` varchar(50) NULL AFTER `ComeTime`;');
CALL add_element_unless_exists('column', 'infobus', 'lastCarPlateNum', 'ALTER TABLE infobus ADD COLUMN `lastCarPlateNum` varchar(50) NULL DEFAULT AFTER `carplatenum`;');
CALL add_element_unless_exists('column', 'infobus', 'ImgName', 'ALTER TABLE infobus ADD COLUMN `ImgName` varchar(50) NULL AFTER `lastCarPlateNum`;');
CALL add_element_unless_exists('column', 'infobus', 'lastImgName', 'ALTER TABLE infobus ADD COLUMN `lastImgName` varchar(50) NULL DEFAULT AFTER `ImgName`;');
CALL add_element_unless_exists('column', 'infobus', 'AreaID', 'ALTER TABLE infobus ADD COLUMN `AreaID` int(11) NULL DEFAULT 0 AFTER `lastImgName`;');
CALL add_element_unless_exists('column', 'infobus', 'Flag', 'ALTER TABLE infobus ADD COLUMN `Flag` int(10) unsigned NOT NULL DEFAULT 0 AFTER `AreaID`;');
CALL add_element_unless_exists('column', 'infobus', 'PreLeaveTime', 'ALTER TABLE infobus ADD COLUMN `PreLeaveTime` varchar(40) NULL AFTER `Flag`;');
CALL add_element_unless_exists('column', 'infobus', 'PreComeTime', 'ALTER TABLE infobus ADD COLUMN `PreComeTime` varchar(40) NULL AFTER `PreLeaveTime`;');
CALL add_element_unless_exists('column', 'infobus', 'PreCarplateNum', 'ALTER TABLE infobus ADD COLUMN `PreCarplateNum` varchar(50) NULL AFTER `PreComeTime`;');
CALL add_element_unless_exists('column', 'infobus', 'CarType', 'ALTER TABLE infobus ADD COLUMN `CarType` int(11) NULL DEFAULT 0 AFTER `PreCarplateNum`;');
CALL add_element_unless_exists('column', 'infobus', 'ifchange', 'ALTER TABLE infobus ADD COLUMN `ifchange` int(11) NULL DEFAULT 0 AFTER `CarType`;');
CALL add_element_unless_exists('column', 'infobus', 'ifsend', 'ALTER TABLE infobus ADD COLUMN `ifsend` int(11) NULL DEFAULT 0 AFTER `ifchange`;');
CALL add_element_unless_exists('column', 'infobus', 'CarplateDigital', 'ALTER TABLE infobus ADD COLUMN `CarplateDigital` varchar(45) NULL AFTER `ifsend`;');
CALL add_element_unless_exists('column', 'infobus', 'Mid', 'ALTER TABLE infobus ADD COLUMN `Mid` int(10) unsigned NOT NULL DEFAULT 0 AFTER `CarplateDigital`;');
CALL add_element_unless_exists('column', 'infobus', 'Trun', 'ALTER TABLE infobus ADD COLUMN `Trun` int(10) unsigned NOT NULL DEFAULT 0 AFTER `Mid`;');
CALL add_element_unless_exists('column', 'infobus', 'PosX', 'ALTER TABLE infobus ADD COLUMN `PosX` int(10) unsigned NOT NULL DEFAULT 0 AFTER `Trun`;');
CALL add_element_unless_exists('column', 'infobus', 'PosY', 'ALTER TABLE infobus ADD COLUMN `PosY` int(10) unsigned NOT NULL DEFAULT 0 AFTER `PosX`;');
CALL add_element_unless_exists('column', 'infobus', 'IfSetRoute', 'ALTER TABLE infobus ADD COLUMN `IfSetRoute` varchar(255) NULL DEFAULT 0 AFTER `PosY`;');
CALL add_element_unless_exists('column', 'infobus', 'PSPlaceNum', 'ALTER TABLE infobus ADD COLUMN `PSPlaceNum` varchar(30) NOT NULL DEFAULT AFTER `IfSetRoute`;');
CALL add_element_unless_exists('column', 'infobus', 'PSPlaceName', 'ALTER TABLE infobus ADD COLUMN `PSPlaceName` varchar(30) NOT NULL DEFAULT AFTER `PSPlaceNum`;');
CALL add_element_unless_exists('column', 'infobus', 'WDCloudFlag', 'ALTER TABLE infobus ADD COLUMN `WDCloudFlag` int(4) NOT NULL DEFAULT 0 AFTER `PSPlaceName`;');
CALL add_element_unless_exists('column', 'infobus', 'WDCloudDate', 'ALTER TABLE infobus ADD COLUMN `WDCloudDate` datetime NULL AFTER `WDCloudFlag`;');
CALL add_element_unless_exists('column', 'infobus', 'parktype', 'ALTER TABLE infobus ADD COLUMN `parktype` int(1) NULL DEFAULT 0 AFTER `WDCloudDate`;');
CALL add_element_unless_exists('column', 'infobus', 'CliDate', 'ALTER TABLE infobus ADD COLUMN `CliDate` datetime NULL AFTER `parktype`;');
CALL add_element_unless_exists('column', 'infobus', 'CliFlag', 'ALTER TABLE infobus ADD COLUMN `CliFlag` int(8) NOT NULL DEFAULT 0 AFTER `CliDate`;');
CALL add_element_unless_exists('column', 'infobus', 'IsDelete', 'ALTER TABLE infobus ADD COLUMN `IsDelete` int(1) NOT NULL DEFAULT 0 AFTER `CliFlag`;');
CALL add_element_unless_exists('column', 'infobus', 'LightType', 'ALTER TABLE infobus ADD COLUMN `LightType` int(11) NULL DEFAULT 0 AFTER `IsDelete`;');
CALL add_element_unless_exists('column', 'infobus', 'LightSend', 'ALTER TABLE infobus ADD COLUMN `LightSend` int(11) NULL DEFAULT 0 AFTER `LightType`;');
CALL add_element_unless_exists('column', 'infobus', 'LightFree', 'ALTER TABLE infobus ADD COLUMN `LightFree` int(11) NULL DEFAULT 0 AFTER `LightSend`;');
CALL add_element_unless_exists('column', 'infobus', 'LightOcc', 'ALTER TABLE infobus ADD COLUMN `LightOcc` int(11) NULL DEFAULT 0 AFTER `LightFree`;');
CALL add_element_unless_exists('column', 'infobus', 'LightErr', 'ALTER TABLE infobus ADD COLUMN `LightErr` int(11) NULL DEFAULT 0 AFTER `LightOcc`;');
CALL add_element_unless_exists('column', 'infobus', 'CarPlateASI', 'ALTER TABLE infobus ADD COLUMN `CarPlateASI` varchar(30) NULL AFTER `LightErr`;');
CALL add_element_unless_exists('column', 'infobus', 'ClientUpdateTime', 'ALTER TABLE infobus ADD COLUMN `ClientUpdateTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP AFTER `CarPlateASI`;');
CALL add_element_unless_exists('index', 'infobus', 'PRIMARY', 'ALTER TABLE infobus ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');
CALL add_element_unless_exists('index', 'infobus', 'IDX_BusNo_CarNo', 'ALTER TABLE infobus ADD INDEX INDEX `IDX_BusNo_CarNo` (`BusNumber`) USING BTREE;');
CALL add_element_unless_exists('index', 'infobus', 'IDX_BusNo_CarNo', 'ALTER TABLE infobus ADD INDEX INDEX `IDX_BusNo_CarNo` (`carplatenum`) USING BTREE;');
CALL add_element_unless_exists('index', 'infobus', 'Idx_infobus_Addr_AreaId', 'ALTER TABLE infobus ADD INDEX INDEX `Idx_infobus_Addr_AreaId` (`Addr`) USING BTREE;');
CALL add_element_unless_exists('index', 'infobus', 'Idx_infobus_Addr_AreaId', 'ALTER TABLE infobus ADD INDEX INDEX `Idx_infobus_Addr_AreaId` (`AreaID`) USING BTREE;');
CALL add_element_unless_exists('index', 'infobus', 'IX_infobus', 'ALTER TABLE infobus ADD INDEX INDEX `IX_infobus` (`Addr`) USING BTREE;');
CALL add_element_unless_exists('index', 'infobus', 'IX_infobus', 'ALTER TABLE infobus ADD INDEX INDEX `IX_infobus` (`state`) USING BTREE;');
CALL add_element_unless_exists('index', 'infobus', 'IX_infobus_Addr', 'ALTER TABLE infobus ADD INDEX INDEX `IX_infobus_Addr` (`Addr`) USING BTREE;');

-- 更新表 infoconfig 所有字段和索引
CALL add_element_unless_exists('column', 'infoconfig', 'id', 'ALTER TABLE infoconfig ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'infoconfig', 'inquireWays', 'ALTER TABLE infoconfig ADD COLUMN `inquireWays` varchar(200) NULL AFTER `id`;');
CALL add_element_unless_exists('column', 'infoconfig', 'openAlreadyTime', 'ALTER TABLE infoconfig ADD COLUMN `openAlreadyTime` tinyint(1) NULL AFTER `inquireWays`;');
CALL add_element_unless_exists('column', 'infoconfig', 'chargePort', 'ALTER TABLE infoconfig ADD COLUMN `chargePort` int(11) NULL DEFAULT 8080 AFTER `openAlreadyTime`;');
CALL add_element_unless_exists('column', 'infoconfig', 'openParingTime', 'ALTER TABLE infoconfig ADD COLUMN `openParingTime` tinyint(1) NULL AFTER `chargePort`;');
CALL add_element_unless_exists('column', 'infoconfig', 'openBusiness', 'ALTER TABLE infoconfig ADD COLUMN `openBusiness` tinyint(1) NULL AFTER `openParingTime`;');
CALL add_element_unless_exists('column', 'infoconfig', 'openCarPwd', 'ALTER TABLE infoconfig ADD COLUMN `openCarPwd` tinyint(1) NULL AFTER `openBusiness`;');
CALL add_element_unless_exists('column', 'infoconfig', 'cloudPort', 'ALTER TABLE infoconfig ADD COLUMN `cloudPort` int(11) NULL DEFAULT 8099 AFTER `openCarPwd`;');
CALL add_element_unless_exists('column', 'infoconfig', 'plugInCard', 'ALTER TABLE infoconfig ADD COLUMN `plugInCard` tinyint(1) NULL DEFAULT 0 AFTER `cloudPort`;');
CALL add_element_unless_exists('column', 'infoconfig', 'swipingCard', 'ALTER TABLE infoconfig ADD COLUMN `swipingCard` tinyint(1) NULL DEFAULT 0 AFTER `plugInCard`;');
CALL add_element_unless_exists('column', 'infoconfig', 'snapCard', 'ALTER TABLE infoconfig ADD COLUMN `snapCard` tinyint(1) NULL DEFAULT 0 AFTER `swipingCard`;');
CALL add_element_unless_exists('column', 'infoconfig', 'aliPay', 'ALTER TABLE infoconfig ADD COLUMN `aliPay` tinyint(1) NULL DEFAULT 0 AFTER `snapCard`;');
CALL add_element_unless_exists('column', 'infoconfig', 'weiXin', 'ALTER TABLE infoconfig ADD COLUMN `weiXin` tinyint(1) NULL DEFAULT 0 AFTER `aliPay`;');
CALL add_element_unless_exists('column', 'infoconfig', 'cloudChargeServiceAdd', 'ALTER TABLE infoconfig ADD COLUMN `cloudChargeServiceAdd` varchar(50) NULL DEFAULT AFTER `weiXin`;');
CALL add_element_unless_exists('column', 'infoconfig', 'chargeServiceAdd', 'ALTER TABLE infoconfig ADD COLUMN `chargeServiceAdd` varchar(50) NULL DEFAULT AFTER `cloudChargeServiceAdd`;');
CALL add_element_unless_exists('column', 'infoconfig', 'recordCount', 'ALTER TABLE infoconfig ADD COLUMN `recordCount` int(11) NULL DEFAULT 25 AFTER `chargeServiceAdd`;');
CALL add_element_unless_exists('column', 'infoconfig', 'routeType', 'ALTER TABLE infoconfig ADD COLUMN `routeType` tinyint(1) NULL DEFAULT 1 AFTER `recordCount`;');
CALL add_element_unless_exists('column', 'infoconfig', 'phoneServiceAdd', 'ALTER TABLE infoconfig ADD COLUMN `phoneServiceAdd` varchar(50) NULL DEFAULT AFTER `routeType`;');
CALL add_element_unless_exists('column', 'infoconfig', 'ifSubSeller', 'ALTER TABLE infoconfig ADD COLUMN `ifSubSeller` tinyint(4) NULL AFTER `phoneServiceAdd`;');
CALL add_element_unless_exists('column', 'infoconfig', 'plateMaxNum', 'ALTER TABLE infoconfig ADD COLUMN `plateMaxNum` int(11) NULL DEFAULT 5 AFTER `ifSubSeller`;');
CALL add_element_unless_exists('column', 'infoconfig', 'parkMaxNum', 'ALTER TABLE infoconfig ADD COLUMN `parkMaxNum` int(11) NULL DEFAULT 5 AFTER `plateMaxNum`;');
CALL add_element_unless_exists('column', 'infoconfig', 'isOpenPrint', 'ALTER TABLE infoconfig ADD COLUMN `isOpenPrint` tinyint(4) NULL AFTER `parkMaxNum`;');
CALL add_element_unless_exists('column', 'infoconfig', 'isOpenPickUp', 'ALTER TABLE infoconfig ADD COLUMN `isOpenPickUp` tinyint(4) NULL AFTER `isOpenPrint`;');
CALL add_element_unless_exists('column', 'infoconfig', 'languageSupport', 'ALTER TABLE infoconfig ADD COLUMN `languageSupport` int(11) NULL DEFAULT 0 AFTER `isOpenPickUp`;');
CALL add_element_unless_exists('column', 'infoconfig', 'foreginLanguage', 'ALTER TABLE infoconfig ADD COLUMN `foreginLanguage` varchar(30) NULL DEFAULT AFTER `languageSupport`;');
CALL add_element_unless_exists('column', 'infoconfig', 'isOpenQrcode', 'ALTER TABLE infoconfig ADD COLUMN `isOpenQrcode` tinyint(1) NULL DEFAULT 0 AFTER `foreginLanguage`;');
CALL add_element_unless_exists('index', 'infoconfig', 'PRIMARY', 'ALTER TABLE infoconfig ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 infofloor 所有字段和索引
CALL add_element_unless_exists('column', 'infofloor', 'id', 'ALTER TABLE infofloor ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'infofloor', 'curmid', 'ALTER TABLE infofloor ADD COLUMN `curmid` int(11) NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 'infofloor', 'othermid', 'ALTER TABLE infofloor ADD COLUMN `othermid` int(11) NULL DEFAULT 0 AFTER `curmid`;');
CALL add_element_unless_exists('column', 'infofloor', 'imgsrc', 'ALTER TABLE infofloor ADD COLUMN `imgsrc` varchar(255) NULL AFTER `othermid`;');
CALL add_element_unless_exists('column', 'infofloor', 'ftype', 'ALTER TABLE infofloor ADD COLUMN `ftype` int(11) NULL DEFAULT 0 AFTER `imgsrc`;');
CALL add_element_unless_exists('column', 'infofloor', 'pointid', 'ALTER TABLE infofloor ADD COLUMN `pointid` int(11) NULL DEFAULT 0 AFTER `ftype`;');
CALL add_element_unless_exists('index', 'infofloor', 'PRIMARY', 'ALTER TABLE infofloor ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 infohint 所有字段和索引
CALL add_element_unless_exists('column', 'infohint', 'ID', 'ALTER TABLE infohint ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'infohint', 'FindOption', 'ALTER TABLE infohint ADD COLUMN `FindOption` int(11) NULL DEFAULT 0 AFTER `ID`;');
CALL add_element_unless_exists('column', 'infohint', 'SubOption', 'ALTER TABLE infohint ADD COLUMN `SubOption` int(11) NULL DEFAULT 0 AFTER `FindOption`;');
CALL add_element_unless_exists('column', 'infohint', 'Memo', 'ALTER TABLE infohint ADD COLUMN `Memo` varchar(255) NULL DEFAULT AFTER `SubOption`;');
CALL add_element_unless_exists('column', 'infohint', 'cnWarnInfo', 'ALTER TABLE infohint ADD COLUMN `cnWarnInfo` varchar(255) NULL DEFAULT AFTER `Memo`;');
CALL add_element_unless_exists('column', 'infohint', 'enWarnInfo', 'ALTER TABLE infohint ADD COLUMN `enWarnInfo` varchar(255) NULL DEFAULT AFTER `cnWarnInfo`;');
CALL add_element_unless_exists('column', 'infohint', 'otherWarnInfo', 'ALTER TABLE infohint ADD COLUMN `otherWarnInfo` varchar(255) NULL DEFAULT AFTER `enWarnInfo`;');
CALL add_element_unless_exists('index', 'infohint', 'PRIMARY', 'ALTER TABLE infohint ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 infoled 所有字段和索引
CALL add_element_unless_exists('column', 'infoled', 'ID', 'ALTER TABLE infoled ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'infoled', 'Addr', 'ALTER TABLE infoled ADD COLUMN `Addr` int(11) NULL DEFAULT 0 AFTER `ID`;');
CALL add_element_unless_exists('column', 'infoled', 'LMemo', 'ALTER TABLE infoled ADD COLUMN `LMemo` varchar(255) NULL DEFAULT AFTER `Addr`;');
CALL add_element_unless_exists('column', 'infoled', 'LType', 'ALTER TABLE infoled ADD COLUMN `LType` varchar(2) NULL AFTER `LMemo`;');
CALL add_element_unless_exists('column', 'infoled', 'ShowNum', 'ALTER TABLE infoled ADD COLUMN `ShowNum` smallint(6) NULL AFTER `LType`;');
CALL add_element_unless_exists('column', 'infoled', 'ShowType', 'ALTER TABLE infoled ADD COLUMN `ShowType` int(11) NULL DEFAULT 0 AFTER `ShowNum`;');
CALL add_element_unless_exists('column', 'infoled', 'State', 'ALTER TABLE infoled ADD COLUMN `State` int(11) NULL DEFAULT 0 AFTER `ShowType`;');
CALL add_element_unless_exists('column', 'infoled', 'EmptyBus', 'ALTER TABLE infoled ADD COLUMN `EmptyBus` int(11) NULL DEFAULT 0 AFTER `State`;');
CALL add_element_unless_exists('column', 'infoled', 'last_update', 'ALTER TABLE infoled ADD COLUMN `last_update` datetime NULL AFTER `EmptyBus`;');
CALL add_element_unless_exists('column', 'infoled', 'ifclosed', 'ALTER TABLE infoled ADD COLUMN `ifclosed` int(11) NULL DEFAULT 0 AFTER `last_update`;');
CALL add_element_unless_exists('column', 'infoled', 'ifsend', 'ALTER TABLE infoled ADD COLUMN `ifsend` int(11) unsigned NULL DEFAULT 0 AFTER `ifclosed`;');
CALL add_element_unless_exists('column', 'infoled', 'ledsz', 'ALTER TABLE infoled ADD COLUMN `ledsz` int(11) unsigned NOT NULL DEFAULT 0 AFTER `ifsend`;');
CALL add_element_unless_exists('column', 'infoled', 'allbusaddr', 'ALTER TABLE infoled ADD COLUMN `allbusaddr` int(11) unsigned NOT NULL DEFAULT 0 AFTER `ledsz`;');
CALL add_element_unless_exists('column', 'infoled', 'lotid', 'ALTER TABLE infoled ADD COLUMN `lotid` int(11) NOT NULL DEFAULT 0 AFTER `allbusaddr`;');
CALL add_element_unless_exists('column', 'infoled', 'posx', 'ALTER TABLE infoled ADD COLUMN `posx` int(11) NULL DEFAULT 0 AFTER `lotid`;');
CALL add_element_unless_exists('column', 'infoled', 'posy', 'ALTER TABLE infoled ADD COLUMN `posy` int(11) NULL DEFAULT 0 AFTER `posx`;');
CALL add_element_unless_exists('column', 'infoled', 'checknum', 'ALTER TABLE infoled ADD COLUMN `checknum` int(11) NULL DEFAULT 0 AFTER `posy`;');
CALL add_element_unless_exists('column', 'infoled', 'ledtype', 'ALTER TABLE infoled ADD COLUMN `ledtype` int(11) NULL DEFAULT 0 AFTER `checknum`;');
CALL add_element_unless_exists('column', 'infoled', 'criticalval', 'ALTER TABLE infoled ADD COLUMN `criticalval` int(11) NULL DEFAULT 0 AFTER `ledtype`;');
CALL add_element_unless_exists('column', 'infoled', 'levaddr', 'ALTER TABLE infoled ADD COLUMN `levaddr` int(11) NULL DEFAULT 0 AFTER `criticalval`;');
CALL add_element_unless_exists('column', 'infoled', 'inoutledip', 'ALTER TABLE infoled ADD COLUMN `inoutledip` varchar(255) NULL DEFAULT AFTER `levaddr`;');
CALL add_element_unless_exists('column', 'infoled', 'ledkind', 'ALTER TABLE infoled ADD COLUMN `ledkind` int(2) NULL DEFAULT 0 AFTER `inoutledip`;');
CALL add_element_unless_exists('index', 'infoled', 'PRIMARY', 'ALTER TABLE infoled ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 infoledlev 所有字段和索引
CALL add_element_unless_exists('column', 'infoledlev', 'ID', 'ALTER TABLE infoledlev ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'infoledlev', 'Addr', 'ALTER TABLE infoledlev ADD COLUMN `Addr` int(11) NULL DEFAULT 0 AFTER `ID`;');
CALL add_element_unless_exists('column', 'infoledlev', 'LMemo', 'ALTER TABLE infoledlev ADD COLUMN `LMemo` varchar(255) NULL DEFAULT AFTER `Addr`;');
CALL add_element_unless_exists('column', 'infoledlev', 'LType', 'ALTER TABLE infoledlev ADD COLUMN `LType` varchar(2) NULL AFTER `LMemo`;');
CALL add_element_unless_exists('column', 'infoledlev', 'ShowNum', 'ALTER TABLE infoledlev ADD COLUMN `ShowNum` smallint(6) NULL AFTER `LType`;');
CALL add_element_unless_exists('column', 'infoledlev', 'ShowType', 'ALTER TABLE infoledlev ADD COLUMN `ShowType` int(11) NULL DEFAULT 0 AFTER `ShowNum`;');
CALL add_element_unless_exists('column', 'infoledlev', 'State', 'ALTER TABLE infoledlev ADD COLUMN `State` int(11) NULL DEFAULT 0 AFTER `ShowType`;');
CALL add_element_unless_exists('column', 'infoledlev', 'EmptyBus', 'ALTER TABLE infoledlev ADD COLUMN `EmptyBus` int(11) NULL DEFAULT 0 AFTER `State`;');
CALL add_element_unless_exists('column', 'infoledlev', 'last_update', 'ALTER TABLE infoledlev ADD COLUMN `last_update` datetime NULL AFTER `EmptyBus`;');
CALL add_element_unless_exists('column', 'infoledlev', 'ifclosed', 'ALTER TABLE infoledlev ADD COLUMN `ifclosed` int(11) NULL DEFAULT 0 AFTER `last_update`;');
CALL add_element_unless_exists('column', 'infoledlev', 'ifsend', 'ALTER TABLE infoledlev ADD COLUMN `ifsend` int(11) unsigned NULL DEFAULT 0 AFTER `ifclosed`;');
CALL add_element_unless_exists('column', 'infoledlev', 'ledsz', 'ALTER TABLE infoledlev ADD COLUMN `ledsz` int(11) unsigned NOT NULL DEFAULT 0 AFTER `ifsend`;');
CALL add_element_unless_exists('column', 'infoledlev', 'allbusaddr', 'ALTER TABLE infoledlev ADD COLUMN `allbusaddr` int(11) unsigned NOT NULL DEFAULT 0 AFTER `ledsz`;');
CALL add_element_unless_exists('column', 'infoledlev', 'lotid', 'ALTER TABLE infoledlev ADD COLUMN `lotid` int(11) NOT NULL DEFAULT 0 AFTER `allbusaddr`;');
CALL add_element_unless_exists('column', 'infoledlev', 'posx', 'ALTER TABLE infoledlev ADD COLUMN `posx` int(11) NULL DEFAULT 0 AFTER `lotid`;');
CALL add_element_unless_exists('column', 'infoledlev', 'posy', 'ALTER TABLE infoledlev ADD COLUMN `posy` int(11) NULL DEFAULT 0 AFTER `posx`;');
CALL add_element_unless_exists('column', 'infoledlev', 'checknum', 'ALTER TABLE infoledlev ADD COLUMN `checknum` int(11) NULL DEFAULT 0 AFTER `posy`;');
CALL add_element_unless_exists('column', 'infoledlev', 'ledtype', 'ALTER TABLE infoledlev ADD COLUMN `ledtype` int(11) NULL DEFAULT 3 AFTER `checknum`;');
CALL add_element_unless_exists('column', 'infoledlev', 'criticalval', 'ALTER TABLE infoledlev ADD COLUMN `criticalval` int(11) NULL DEFAULT 0 AFTER `ledtype`;');
CALL add_element_unless_exists('index', 'infoledlev', 'PRIMARY', 'ALTER TABLE infoledlev ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 infomap 所有字段和索引
CALL add_element_unless_exists('column', 'infomap', 'ID', 'ALTER TABLE infomap ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'infomap', 'Mapname', 'ALTER TABLE infomap ADD COLUMN `Mapname` varchar(30) NOT NULL DEFAULT AFTER `ID`;');
CALL add_element_unless_exists('column', 'infomap', 'MapName2', 'ALTER TABLE infomap ADD COLUMN `MapName2` varchar(30) NULL DEFAULT AFTER `Mapname`;');
CALL add_element_unless_exists('column', 'infomap', 'MapName3', 'ALTER TABLE infomap ADD COLUMN `MapName3` varchar(30) NULL DEFAULT AFTER `MapName2`;');
CALL add_element_unless_exists('column', 'infomap', 'Mapfile', 'ALTER TABLE infomap ADD COLUMN `Mapfile` varchar(60) NOT NULL DEFAULT AFTER `MapName3`;');
CALL add_element_unless_exists('column', 'infomap', 'Big', 'ALTER TABLE infomap ADD COLUMN `Big` int(11) unsigned NOT NULL DEFAULT 0 AFTER `Mapfile`;');
CALL add_element_unless_exists('column', 'infomap', 'FloorPoint', 'ALTER TABLE infomap ADD COLUMN `FloorPoint` varchar(50) NOT NULL DEFAULT AFTER `Big`;');
CALL add_element_unless_exists('column', 'infomap', 'MapDeclare', 'ALTER TABLE infomap ADD COLUMN `MapDeclare` varchar(50) NOT NULL DEFAULT AFTER `FloorPoint`;');
CALL add_element_unless_exists('column', 'infomap', 'SpaceL', 'ALTER TABLE infomap ADD COLUMN `SpaceL` int(8) NOT NULL DEFAULT 0 AFTER `MapDeclare`;');
CALL add_element_unless_exists('column', 'infomap', 'SpaceW', 'ALTER TABLE infomap ADD COLUMN `SpaceW` int(8) NOT NULL DEFAULT 0 AFTER `SpaceL`;');
CALL add_element_unless_exists('column', 'infomap', 'orderNo', 'ALTER TABLE infomap ADD COLUMN `orderNo` tinyint(4) NOT NULL DEFAULT 0 AFTER `SpaceW`;');
CALL add_element_unless_exists('column', 'infomap', 'CliDate', 'ALTER TABLE infomap ADD COLUMN `CliDate` datetime NULL AFTER `orderNo`;');
CALL add_element_unless_exists('column', 'infomap', 'CliFlag', 'ALTER TABLE infomap ADD COLUMN `CliFlag` int(8) NOT NULL DEFAULT 0 AFTER `CliDate`;');
CALL add_element_unless_exists('column', 'infomap', 'total', 'ALTER TABLE infomap ADD COLUMN `total` int(11) NULL DEFAULT 0 AFTER `CliFlag`;');
CALL add_element_unless_exists('column', 'infomap', 'Type', 'ALTER TABLE infomap ADD COLUMN `Type` varchar(255) NULL AFTER `total`;');
CALL add_element_unless_exists('column', 'infomap', 'MapCode', 'ALTER TABLE infomap ADD COLUMN `MapCode` varchar(50) NULL DEFAULT AFTER `Type`;');
CALL add_element_unless_exists('column', 'infomap', 'IsDelete', 'ALTER TABLE infomap ADD COLUMN `IsDelete` int(1) NOT NULL DEFAULT 0 AFTER `MapCode`;');
CALL add_element_unless_exists('index', 'infomap', 'PRIMARY', 'ALTER TABLE infomap ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 infonode 所有字段和索引
CALL add_element_unless_exists('column', 'infonode', 'ID', 'ALTER TABLE infonode ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'infonode', 'Addr', 'ALTER TABLE infonode ADD COLUMN `Addr` int(11) NULL DEFAULT 0 AFTER `ID`;');
CALL add_element_unless_exists('column', 'infonode', 'BusNum', 'ALTER TABLE infonode ADD COLUMN `BusNum` int(11) NULL DEFAULT 0 AFTER `Addr`;');
CALL add_element_unless_exists('column', 'infonode', 'NMemo', 'ALTER TABLE infonode ADD COLUMN `NMemo` mediumtext NULL AFTER `BusNum`;');
CALL add_element_unless_exists('column', 'infonode', 'State', 'ALTER TABLE infonode ADD COLUMN `State` int(11) NULL DEFAULT 0 AFTER `NMemo`;');
CALL add_element_unless_exists('column', 'infonode', 'LastRecData', 'ALTER TABLE infonode ADD COLUMN `LastRecData` varchar(30) NULL AFTER `State`;');
CALL add_element_unless_exists('column', 'infonode', 'LastRecTime', 'ALTER TABLE infonode ADD COLUMN `LastRecTime` varchar(40) NULL AFTER `LastRecData`;');
CALL add_element_unless_exists('column', 'infonode', 'PowerIp', 'ALTER TABLE infonode ADD COLUMN `PowerIp` varchar(255) NULL AFTER `LastRecTime`;');
CALL add_element_unless_exists('column', 'infonode', 'PowerSend', 'ALTER TABLE infonode ADD COLUMN `PowerSend` varchar(255) NULL AFTER `PowerIp`;');
CALL add_element_unless_exists('column', 'infonode', 'PowerSendTime', 'ALTER TABLE infonode ADD COLUMN `PowerSendTime` datetime NULL AFTER `PowerSend`;');
CALL add_element_unless_exists('column', 'infonode', 'DeviceType', 'ALTER TABLE infonode ADD COLUMN `DeviceType` int(11) NULL DEFAULT 0 AFTER `PowerSendTime`;');
CALL add_element_unless_exists('index', 'infonode', 'PRIMARY', 'ALTER TABLE infonode ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 infopic 所有字段和索引
CALL add_element_unless_exists('column', 'infopic', 'id', 'ALTER TABLE infopic ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'infopic', 'imgsrc', 'ALTER TABLE infopic ADD COLUMN `imgsrc` varchar(255) NULL DEFAULT AFTER `id`;');
CALL add_element_unless_exists('column', 'infopic', 'imgname', 'ALTER TABLE infopic ADD COLUMN `imgname` varchar(255) NULL AFTER `imgsrc`;');
CALL add_element_unless_exists('index', 'infopic', 'PRIMARY', 'ALTER TABLE infopic ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 inforecorder 所有字段和索引
CALL add_element_unless_exists('column', 'inforecorder', 'id', 'ALTER TABLE inforecorder ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'inforecorder', 'ip', 'ALTER TABLE inforecorder ADD COLUMN `ip` varchar(255) NULL AFTER `id`;');
CALL add_element_unless_exists('column', 'inforecorder', 'Memo', 'ALTER TABLE inforecorder ADD COLUMN `Memo` varchar(255) NULL AFTER `ip`;');
CALL add_element_unless_exists('column', 'inforecorder', 'loginname', 'ALTER TABLE inforecorder ADD COLUMN `loginname` varchar(255) NULL AFTER `Memo`;');
CALL add_element_unless_exists('column', 'inforecorder', 'loginpwd', 'ALTER TABLE inforecorder ADD COLUMN `loginpwd` varchar(255) NULL AFTER `loginname`;');
CALL add_element_unless_exists('column', 'inforecorder', 'port', 'ALTER TABLE inforecorder ADD COLUMN `port` int(11) NULL DEFAULT 0 AFTER `loginpwd`;');
CALL add_element_unless_exists('index', 'inforecorder', 'PRIMARY', 'ALTER TABLE inforecorder ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 infoserlog 所有字段和索引
CALL add_element_unless_exists('column', 'infoserlog', 'id', 'ALTER TABLE infoserlog ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'infoserlog', 'usetime', 'ALTER TABLE infoserlog ADD COLUMN `usetime` datetime NULL AFTER `id`;');
CALL add_element_unless_exists('column', 'infoserlog', 'usetype', 'ALTER TABLE infoserlog ADD COLUMN `usetype` int(11) NULL DEFAULT 0 AFTER `usetime`;');
CALL add_element_unless_exists('column', 'infoserlog', 'useval', 'ALTER TABLE infoserlog ADD COLUMN `useval` varchar(255) NULL AFTER `usetype`;');
CALL add_element_unless_exists('column', 'infoserlog', 'cip', 'ALTER TABLE infoserlog ADD COLUMN `cip` varchar(255) NULL DEFAULT AFTER `useval`;');
CALL add_element_unless_exists('index', 'infoserlog', 'PRIMARY', 'ALTER TABLE infoserlog ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 infosystem 所有字段和索引
CALL add_element_unless_exists('column', 'infosystem', 'id', 'ALTER TABLE infosystem ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'infosystem', 'type', 'ALTER TABLE infosystem ADD COLUMN `type` int(11) NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 'infosystem', 'memo', 'ALTER TABLE infosystem ADD COLUMN `memo` varchar(255) NULL DEFAULT AFTER `type`;');
CALL add_element_unless_exists('column', 'infosystem', 'value', 'ALTER TABLE infosystem ADD COLUMN `value` varchar(255) NULL DEFAULT AFTER `memo`;');
CALL add_element_unless_exists('index', 'infosystem', 'PRIMARY', 'ALTER TABLE infosystem ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 log_carinout 所有字段和索引
CALL add_element_unless_exists('column', 'log_carinout', 'ID', 'ALTER TABLE log_carinout ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'log_carinout', 'ParkDate', 'ALTER TABLE log_carinout ADD COLUMN `ParkDate` date NULL AFTER `ID`;');
CALL add_element_unless_exists('column', 'log_carinout', 'ParkHour', 'ALTER TABLE log_carinout ADD COLUMN `ParkHour` int(11) NOT NULL DEFAULT 0 AFTER `ParkDate`;');
CALL add_element_unless_exists('column', 'log_carinout', 'FlowIn', 'ALTER TABLE log_carinout ADD COLUMN `FlowIn` int(11) NOT NULL DEFAULT 0 AFTER `ParkHour`;');
CALL add_element_unless_exists('column', 'log_carinout', 'FlowOut', 'ALTER TABLE log_carinout ADD COLUMN `FlowOut` int(11) NOT NULL DEFAULT 0 AFTER `FlowIn`;');
CALL add_element_unless_exists('column', 'log_carinout', 'FlowIn1', 'ALTER TABLE log_carinout ADD COLUMN `FlowIn1` int(11) NOT NULL DEFAULT 0 AFTER `FlowOut`;');
CALL add_element_unless_exists('column', 'log_carinout', 'FlowOut1', 'ALTER TABLE log_carinout ADD COLUMN `FlowOut1` int(11) NOT NULL DEFAULT 0 AFTER `FlowIn1`;');
CALL add_element_unless_exists('column', 'log_carinout', 'FlowIn2', 'ALTER TABLE log_carinout ADD COLUMN `FlowIn2` int(11) NOT NULL DEFAULT 0 AFTER `FlowOut1`;');
CALL add_element_unless_exists('column', 'log_carinout', 'FlowOut2', 'ALTER TABLE log_carinout ADD COLUMN `FlowOut2` int(11) NOT NULL DEFAULT 0 AFTER `FlowIn2`;');
CALL add_element_unless_exists('column', 'log_carinout', 'FlowIn3', 'ALTER TABLE log_carinout ADD COLUMN `FlowIn3` int(11) NOT NULL DEFAULT 0 AFTER `FlowOut2`;');
CALL add_element_unless_exists('column', 'log_carinout', 'FlowOut3', 'ALTER TABLE log_carinout ADD COLUMN `FlowOut3` int(11) NOT NULL DEFAULT 0 AFTER `FlowIn3`;');
CALL add_element_unless_exists('index', 'log_carinout', 'PRIMARY', 'ALTER TABLE log_carinout ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 log_hourcount 所有字段和索引
CALL add_element_unless_exists('column', 'log_hourcount', 'ID', 'ALTER TABLE log_hourcount ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'log_hourcount', 'StaticDate', 'ALTER TABLE log_hourcount ADD COLUMN `StaticDate` date NULL AFTER `ID`;');
CALL add_element_unless_exists('column', 'log_hourcount', 'StaticHour', 'ALTER TABLE log_hourcount ADD COLUMN `StaticHour` int(11) NULL AFTER `StaticDate`;');
CALL add_element_unless_exists('column', 'log_hourcount', 'ParkLong', 'ALTER TABLE log_hourcount ADD COLUMN `ParkLong` double NULL AFTER `StaticHour`;');
CALL add_element_unless_exists('column', 'log_hourcount', 'ParkLong1', 'ALTER TABLE log_hourcount ADD COLUMN `ParkLong1` double NULL AFTER `ParkLong`;');
CALL add_element_unless_exists('column', 'log_hourcount', 'ParkLong2', 'ALTER TABLE log_hourcount ADD COLUMN `ParkLong2` double NULL AFTER `ParkLong1`;');
CALL add_element_unless_exists('column', 'log_hourcount', 'ParkLong3', 'ALTER TABLE log_hourcount ADD COLUMN `ParkLong3` double NULL AFTER `ParkLong2`;');
CALL add_element_unless_exists('column', 'log_hourcount', 'ParkCount', 'ALTER TABLE log_hourcount ADD COLUMN `ParkCount` int(11) NULL DEFAULT 0 AFTER `ParkLong3`;');
CALL add_element_unless_exists('column', 'log_hourcount', 'ParkCount1', 'ALTER TABLE log_hourcount ADD COLUMN `ParkCount1` int(11) NULL DEFAULT 0 AFTER `ParkCount`;');
CALL add_element_unless_exists('column', 'log_hourcount', 'ParkCount2', 'ALTER TABLE log_hourcount ADD COLUMN `ParkCount2` int(11) NULL DEFAULT 0 AFTER `ParkCount1`;');
CALL add_element_unless_exists('column', 'log_hourcount', 'ParkCount3', 'ALTER TABLE log_hourcount ADD COLUMN `ParkCount3` int(11) NULL DEFAULT 0 AFTER `ParkCount2`;');
CALL add_element_unless_exists('index', 'log_hourcount', 'PRIMARY', 'ALTER TABLE log_hourcount ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 log_login 所有字段和索引
CALL add_element_unless_exists('column', 'log_login', 'login_id', 'ALTER TABLE log_login ADD COLUMN `login_id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'log_login', 'login_account', 'ALTER TABLE log_login ADD COLUMN `login_account` varchar(50) NULL AFTER `login_id`;');
CALL add_element_unless_exists('column', 'log_login', 'login_time', 'ALTER TABLE log_login ADD COLUMN `login_time` datetime NULL AFTER `login_account`;');
CALL add_element_unless_exists('column', 'log_login', 'login_desc', 'ALTER TABLE log_login ADD COLUMN `login_desc` varchar(200) NULL AFTER `login_time`;');
CALL add_element_unless_exists('column', 'log_login', 'login_ip', 'ALTER TABLE log_login ADD COLUMN `login_ip` varchar(50) NULL AFTER `login_desc`;');
CALL add_element_unless_exists('index', 'log_login', 'PRIMARY', 'ALTER TABLE log_login ADD UNIQUE INDEX `PRIMARY` (`login_id`) USING BTREE;');

-- 更新表 log_operate 所有字段和索引
CALL add_element_unless_exists('column', 'log_operate', 'ope_id', 'ALTER TABLE log_operate ADD COLUMN `ope_id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'log_operate', 'ope_user_id', 'ALTER TABLE log_operate ADD COLUMN `ope_user_id` varchar(11) NULL AFTER `ope_id`;');
CALL add_element_unless_exists('column', 'log_operate', 'ope_time', 'ALTER TABLE log_operate ADD COLUMN `ope_time` datetime NULL AFTER `ope_user_id`;');
CALL add_element_unless_exists('column', 'log_operate', 'ope_ip', 'ALTER TABLE log_operate ADD COLUMN `ope_ip` varchar(50) NULL AFTER `ope_time`;');
CALL add_element_unless_exists('column', 'log_operate', 'ope_action', 'ALTER TABLE log_operate ADD COLUMN `ope_action` int(1) NULL AFTER `ope_ip`;');
CALL add_element_unless_exists('column', 'log_operate', 'ope_content', 'ALTER TABLE log_operate ADD COLUMN `ope_content` longtext NULL AFTER `ope_action`;');
CALL add_element_unless_exists('index', 'log_operate', 'PRIMARY', 'ALTER TABLE log_operate ADD UNIQUE INDEX `PRIMARY` (`ope_id`) USING BTREE;');

-- 更新表 log_parkcount 所有字段和索引
CALL add_element_unless_exists('column', 'log_parkcount', 'ID', 'ALTER TABLE log_parkcount ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'log_parkcount', 'AreaId', 'ALTER TABLE log_parkcount ADD COLUMN `AreaId` int(11) NOT NULL DEFAULT 0 AFTER `ID`;');
CALL add_element_unless_exists('column', 'log_parkcount', 'AreaName', 'ALTER TABLE log_parkcount ADD COLUMN `AreaName` varchar(50) NOT NULL DEFAULT AFTER `AreaId`;');
CALL add_element_unless_exists('column', 'log_parkcount', 'ParkDate', 'ALTER TABLE log_parkcount ADD COLUMN `ParkDate` datetime NULL AFTER `AreaName`;');
CALL add_element_unless_exists('column', 'log_parkcount', 'ParkHour', 'ALTER TABLE log_parkcount ADD COLUMN `ParkHour` int(11) NOT NULL DEFAULT 0 AFTER `ParkDate`;');
CALL add_element_unless_exists('column', 'log_parkcount', 'ParkCount', 'ALTER TABLE log_parkcount ADD COLUMN `ParkCount` int(11) NOT NULL DEFAULT 0 AFTER `ParkHour`;');
CALL add_element_unless_exists('column', 'log_parkcount', 'FlowIn', 'ALTER TABLE log_parkcount ADD COLUMN `FlowIn` int(11) NOT NULL DEFAULT 0 AFTER `ParkCount`;');
CALL add_element_unless_exists('column', 'log_parkcount', 'FlowOut', 'ALTER TABLE log_parkcount ADD COLUMN `FlowOut` int(11) NOT NULL DEFAULT 0 AFTER `FlowIn`;');
CALL add_element_unless_exists('column', 'log_parkcount', 'CliDate', 'ALTER TABLE log_parkcount ADD COLUMN `CliDate` datetime NULL AFTER `FlowOut`;');
CALL add_element_unless_exists('column', 'log_parkcount', 'CliFlag', 'ALTER TABLE log_parkcount ADD COLUMN `CliFlag` int(8) NOT NULL DEFAULT 0 AFTER `CliDate`;');
CALL add_element_unless_exists('column', 'log_parkcount', 'IsDelete', 'ALTER TABLE log_parkcount ADD COLUMN `IsDelete` int(1) NOT NULL DEFAULT 0 AFTER `CliFlag`;');
CALL add_element_unless_exists('index', 'log_parkcount', 'PRIMARY', 'ALTER TABLE log_parkcount ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');
CALL add_element_unless_exists('index', 'log_parkcount', 'UK_log_parkcount', 'ALTER TABLE log_parkcount ADD UNIQUE INDEX `UK_log_parkcount` (`AreaId`) USING BTREE;');
CALL add_element_unless_exists('index', 'log_parkcount', 'UK_log_parkcount', 'ALTER TABLE log_parkcount ADD UNIQUE INDEX `UK_log_parkcount` (`ParkDate`) USING BTREE;');
CALL add_element_unless_exists('index', 'log_parkcount', 'UK_log_parkcount', 'ALTER TABLE log_parkcount ADD UNIQUE INDEX `UK_log_parkcount` (`ParkHour`) USING BTREE;');

-- 更新表 log_parkinglotlog 所有字段和索引
CALL add_element_unless_exists('column', 'log_parkinglotlog', 'id', 'ALTER TABLE log_parkinglotlog ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'log_parkinglotlog', 'CarplateNum', 'ALTER TABLE log_parkinglotlog ADD COLUMN `CarplateNum` varchar(20) NOT NULL DEFAULT AFTER `id`;');
CALL add_element_unless_exists('column', 'log_parkinglotlog', 'CarAddr', 'ALTER TABLE log_parkinglotlog ADD COLUMN `CarAddr` int(11) NOT NULL DEFAULT 0 AFTER `CarplateNum`;');
CALL add_element_unless_exists('column', 'log_parkinglotlog', 'ImgName', 'ALTER TABLE log_parkinglotlog ADD COLUMN `ImgName` varchar(255) NOT NULL DEFAULT AFTER `CarAddr`;');
CALL add_element_unless_exists('column', 'log_parkinglotlog', 'InTime', 'ALTER TABLE log_parkinglotlog ADD COLUMN `InTime` datetime NULL AFTER `ImgName`;');
CALL add_element_unless_exists('column', 'log_parkinglotlog', 'OutTime', 'ALTER TABLE log_parkinglotlog ADD COLUMN `OutTime` datetime NULL AFTER `InTime`;');
CALL add_element_unless_exists('column', 'log_parkinglotlog', 'longTime', 'ALTER TABLE log_parkinglotlog ADD COLUMN `longTime` int(11) NOT NULL DEFAULT 0 AFTER `OutTime`;');
CALL add_element_unless_exists('column', 'log_parkinglotlog', 'AreaId', 'ALTER TABLE log_parkinglotlog ADD COLUMN `AreaId` int(11) NOT NULL DEFAULT 0 AFTER `longTime`;');
CALL add_element_unless_exists('column', 'log_parkinglotlog', 'CliDate', 'ALTER TABLE log_parkinglotlog ADD COLUMN `CliDate` datetime NULL AFTER `AreaId`;');
CALL add_element_unless_exists('column', 'log_parkinglotlog', 'CliFlag', 'ALTER TABLE log_parkinglotlog ADD COLUMN `CliFlag` int(8) NOT NULL DEFAULT 0 AFTER `CliDate`;');
CALL add_element_unless_exists('column', 'log_parkinglotlog', 'IsDelete', 'ALTER TABLE log_parkinglotlog ADD COLUMN `IsDelete` int(1) NOT NULL DEFAULT 0 AFTER `CliFlag`;');
CALL add_element_unless_exists('index', 'log_parkinglotlog', 'PRIMARY', 'ALTER TABLE log_parkinglotlog ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');
CALL add_element_unless_exists('index', 'log_parkinglotlog', 'IDX_log_parkinglotlog_OutTime', 'ALTER TABLE log_parkinglotlog ADD INDEX INDEX `IDX_log_parkinglotlog_OutTime` (`OutTime`) USING BTREE;');
CALL add_element_unless_exists('index', 'log_parkinglotlog', 'IX_log_parkinglotlog_InTime', 'ALTER TABLE log_parkinglotlog ADD INDEX INDEX `IX_log_parkinglotlog_InTime` (`InTime`) USING BTREE;');

-- 更新表 log_temp 所有字段和索引
CALL add_element_unless_exists('column', 'log_temp', 'ID', 'ALTER TABLE log_temp ADD COLUMN `ID` int(11) NULL DEFAULT 0;');
CALL add_element_unless_exists('column', 'log_temp', 'temp', 'ALTER TABLE log_temp ADD COLUMN `temp` int(11) NULL DEFAULT 0 AFTER `ID`;');

-- 更新表 parklampgroup 所有字段和索引
CALL add_element_unless_exists('column', 'parklampgroup', 'id', 'ALTER TABLE parklampgroup ADD COLUMN `id` int(10) unsigned NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'parklampgroup', 'groupname', 'ALTER TABLE parklampgroup ADD COLUMN `groupname` varchar(45) NOT NULL DEFAULT AFTER `id`;');
CALL add_element_unless_exists('column', 'parklampgroup', 'lampId', 'ALTER TABLE parklampgroup ADD COLUMN `lampId` varchar(4096) NULL DEFAULT 0 AFTER `groupname`;');
CALL add_element_unless_exists('column', 'parklampgroup', 'parkId', 'ALTER TABLE parklampgroup ADD COLUMN `parkId` varchar(4096) NULL DEFAULT 0 AFTER `lampId`;');
CALL add_element_unless_exists('column', 'parklampgroup', 'empty', 'ALTER TABLE parklampgroup ADD COLUMN `empty` int(10) unsigned NULL DEFAULT 0 AFTER `parkId`;');
CALL add_element_unless_exists('column', 'parklampgroup', 'state', 'ALTER TABLE parklampgroup ADD COLUMN `state` int(10) unsigned NULL DEFAULT 0 AFTER `empty`;');
CALL add_element_unless_exists('column', 'parklampgroup', 'lastULTime', 'ALTER TABLE parklampgroup ADD COLUMN `lastULTime` datetime NULL DEFAULT 2013-01-01 00:00:00 AFTER `state`;');
CALL add_element_unless_exists('column', 'parklampgroup', 'lotid', 'ALTER TABLE parklampgroup ADD COLUMN `lotid` int(11) NULL DEFAULT 0 AFTER `lastULTime`;');
CALL add_element_unless_exists('column', 'parklampgroup', 'lotname', 'ALTER TABLE parklampgroup ADD COLUMN `lotname` varchar(50) NULL DEFAULT AFTER `lotid`;');
CALL add_element_unless_exists('column', 'parklampgroup', 'total', 'ALTER TABLE parklampgroup ADD COLUMN `total` int(11) NULL DEFAULT 0 AFTER `lotname`;');
CALL add_element_unless_exists('index', 'parklampgroup', 'PRIMARY', 'ALTER TABLE parklampgroup ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 parkmsglog 所有字段和索引
CALL add_element_unless_exists('column', 'parkmsglog', 'id', 'ALTER TABLE parkmsglog ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'parkmsglog', 'areaid', 'ALTER TABLE parkmsglog ADD COLUMN `areaid` int(11) NULL AFTER `id`;');
CALL add_element_unless_exists('column', 'parkmsglog', 'busnumber', 'ALTER TABLE parkmsglog ADD COLUMN `busnumber` varchar(255) NULL DEFAULT AFTER `areaid`;');
CALL add_element_unless_exists('column', 'parkmsglog', 'plate', 'ALTER TABLE parkmsglog ADD COLUMN `plate` varchar(255) NULL DEFAULT AFTER `busnumber`;');
CALL add_element_unless_exists('column', 'parkmsglog', 'cometime', 'ALTER TABLE parkmsglog ADD COLUMN `cometime` datetime NULL AFTER `plate`;');
CALL add_element_unless_exists('column', 'parkmsglog', 'parklong', 'ALTER TABLE parkmsglog ADD COLUMN `parklong` int(11) NULL DEFAULT 0 AFTER `cometime`;');
CALL add_element_unless_exists('column', 'parkmsglog', 'imgname', 'ALTER TABLE parkmsglog ADD COLUMN `imgname` varchar(255) NULL DEFAULT AFTER `parklong`;');
CALL add_element_unless_exists('column', 'parkmsglog', 'toltype', 'ALTER TABLE parkmsglog ADD COLUMN `toltype` int(11) NULL DEFAULT 1 AFTER `imgname`;');
CALL add_element_unless_exists('column', 'parkmsglog', 'statictime', 'ALTER TABLE parkmsglog ADD COLUMN `statictime` datetime NULL AFTER `toltype`;');
CALL add_element_unless_exists('index', 'parkmsglog', 'PRIMARY', 'ALTER TABLE parkmsglog ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');
CALL add_element_unless_exists('index', 'parkmsglog', 'IDX_parkmsglog_statictime', 'ALTER TABLE parkmsglog ADD INDEX INDEX `IDX_parkmsglog_statictime` (`statictime`) USING BTREE;');

-- 更新表 parkwarnlog 所有字段和索引
CALL add_element_unless_exists('column', 'parkwarnlog', 'id', 'ALTER TABLE parkwarnlog ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'parkwarnlog', 'areaid', 'ALTER TABLE parkwarnlog ADD COLUMN `areaid` int(11) NULL AFTER `id`;');
CALL add_element_unless_exists('column', 'parkwarnlog', 'busnumber', 'ALTER TABLE parkwarnlog ADD COLUMN `busnumber` varchar(255) NULL AFTER `areaid`;');
CALL add_element_unless_exists('column', 'parkwarnlog', 'plate', 'ALTER TABLE parkwarnlog ADD COLUMN `plate` varchar(255) NULL AFTER `busnumber`;');
CALL add_element_unless_exists('column', 'parkwarnlog', 'cometime', 'ALTER TABLE parkwarnlog ADD COLUMN `cometime` datetime NULL AFTER `plate`;');
CALL add_element_unless_exists('column', 'parkwarnlog', 'parklong', 'ALTER TABLE parkwarnlog ADD COLUMN `parklong` int(11) NULL DEFAULT 0 AFTER `cometime`;');
CALL add_element_unless_exists('column', 'parkwarnlog', 'imgname', 'ALTER TABLE parkwarnlog ADD COLUMN `imgname` varchar(255) NULL AFTER `parklong`;');
CALL add_element_unless_exists('column', 'parkwarnlog', 'toltype', 'ALTER TABLE parkwarnlog ADD COLUMN `toltype` int(11) NULL DEFAULT 0 AFTER `imgname`;');
CALL add_element_unless_exists('column', 'parkwarnlog', 'statictime', 'ALTER TABLE parkwarnlog ADD COLUMN `statictime` datetime NULL AFTER `toltype`;');
CALL add_element_unless_exists('index', 'parkwarnlog', 'PRIMARY', 'ALTER TABLE parkwarnlog ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');
CALL add_element_unless_exists('index', 'parkwarnlog', 'IDX_parkwarnlog_statictime', 'ALTER TABLE parkwarnlog ADD INDEX INDEX `IDX_parkwarnlog_statictime` (`statictime`) USING BTREE;');

-- 更新表 sys_assign 所有字段和索引
CALL add_element_unless_exists('column', 'sys_assign', 'assign_id', 'ALTER TABLE sys_assign ADD COLUMN `assign_id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'sys_assign', 'assign_rela_id', 'ALTER TABLE sys_assign ADD COLUMN `assign_rela_id` char(32) NULL AFTER `assign_id`;');
CALL add_element_unless_exists('column', 'sys_assign', 'assign_role', 'ALTER TABLE sys_assign ADD COLUMN `assign_role` int(11) NULL AFTER `assign_rela_id`;');
CALL add_element_unless_exists('column', 'sys_assign', 'assign_type', 'ALTER TABLE sys_assign ADD COLUMN `assign_type` int(1) NULL AFTER `assign_role`;');
CALL add_element_unless_exists('column', 'sys_assign', 'create_time', 'ALTER TABLE sys_assign ADD COLUMN `create_time` datetime NULL AFTER `assign_type`;');
CALL add_element_unless_exists('index', 'sys_assign', 'PRIMARY', 'ALTER TABLE sys_assign ADD UNIQUE INDEX `PRIMARY` (`assign_id`) USING BTREE;');

-- 更新表 sys_i18n_message 所有字段和索引
CALL add_element_unless_exists('column', 'sys_i18n_message', 'ID', 'ALTER TABLE sys_i18n_message ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'sys_i18n_message', 'CODE', 'ALTER TABLE sys_i18n_message ADD COLUMN `CODE` varchar(100) NULL AFTER `ID`;');
CALL add_element_unless_exists('column', 'sys_i18n_message', 'DESCRIPTION', 'ALTER TABLE sys_i18n_message ADD COLUMN `DESCRIPTION` varchar(500) NULL AFTER `CODE`;');
CALL add_element_unless_exists('column', 'sys_i18n_message', 'MODULE', 'ALTER TABLE sys_i18n_message ADD COLUMN `MODULE` varchar(100) NULL AFTER `DESCRIPTION`;');
CALL add_element_unless_exists('column', 'sys_i18n_message', 'ZH_CN', 'ALTER TABLE sys_i18n_message ADD COLUMN `ZH_CN` varchar(500) NULL AFTER `MODULE`;');
CALL add_element_unless_exists('column', 'sys_i18n_message', 'ZH_HK', 'ALTER TABLE sys_i18n_message ADD COLUMN `ZH_HK` varchar(500) NULL AFTER `ZH_CN`;');
CALL add_element_unless_exists('column', 'sys_i18n_message', 'ZH_TW', 'ALTER TABLE sys_i18n_message ADD COLUMN `ZH_TW` varchar(500) NULL AFTER `ZH_HK`;');
CALL add_element_unless_exists('column', 'sys_i18n_message', 'EN_US', 'ALTER TABLE sys_i18n_message ADD COLUMN `EN_US` varchar(500) NULL AFTER `ZH_TW`;');
CALL add_element_unless_exists('column', 'sys_i18n_message', 'QT_LAN', 'ALTER TABLE sys_i18n_message ADD COLUMN `QT_LAN` varchar(500) NULL AFTER `EN_US`;');
CALL add_element_unless_exists('column', 'sys_i18n_message', 'CREATE_TIME', 'ALTER TABLE sys_i18n_message ADD COLUMN `CREATE_TIME` datetime NULL AFTER `QT_LAN`;');
CALL add_element_unless_exists('column', 'sys_i18n_message', 'UPDATE_TIME', 'ALTER TABLE sys_i18n_message ADD COLUMN `UPDATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP AFTER `CREATE_TIME`;');
CALL add_element_unless_exists('index', 'sys_i18n_message', 'PRIMARY', 'ALTER TABLE sys_i18n_message ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');
CALL add_element_unless_exists('index', 'sys_i18n_message', 'UK_sys_i18n_message_CODE', 'ALTER TABLE sys_i18n_message ADD UNIQUE INDEX `UK_sys_i18n_message_CODE` (`CODE`) USING BTREE;');

-- 更新表 sys_module 所有字段和索引
CALL add_element_unless_exists('column', 'sys_module', 'module_id', 'ALTER TABLE sys_module ADD COLUMN `module_id` char(32) NOT NULL;');
CALL add_element_unless_exists('column', 'sys_module', 'module_pid', 'ALTER TABLE sys_module ADD COLUMN `module_pid` char(32) NULL AFTER `module_id`;');
CALL add_element_unless_exists('column', 'sys_module', 'module_name', 'ALTER TABLE sys_module ADD COLUMN `module_name` varchar(50) NULL AFTER `module_pid`;');
CALL add_element_unless_exists('column', 'sys_module', 'module_url', 'ALTER TABLE sys_module ADD COLUMN `module_url` varchar(200) NULL AFTER `module_name`;');
CALL add_element_unless_exists('column', 'sys_module', 'module_desc', 'ALTER TABLE sys_module ADD COLUMN `module_desc` varchar(200) NULL AFTER `module_url`;');
CALL add_element_unless_exists('column', 'sys_module', 'module_order', 'ALTER TABLE sys_module ADD COLUMN `module_order` int(5) NULL AFTER `module_desc`;');
CALL add_element_unless_exists('column', 'sys_module', 'module_show', 'ALTER TABLE sys_module ADD COLUMN `module_show` int(1) NULL AFTER `module_order`;');
CALL add_element_unless_exists('column', 'sys_module', 'module_status', 'ALTER TABLE sys_module ADD COLUMN `module_status` int(1) NULL AFTER `module_show`;');
CALL add_element_unless_exists('column', 'sys_module', 'module_icon', 'ALTER TABLE sys_module ADD COLUMN `module_icon` varchar(20) NULL AFTER `module_status`;');
CALL add_element_unless_exists('column', 'sys_module', 'module_val', 'ALTER TABLE sys_module ADD COLUMN `module_val` varchar(50) NULL AFTER `module_icon`;');
CALL add_element_unless_exists('column', 'sys_module', 'create_time', 'ALTER TABLE sys_module ADD COLUMN `create_time` datetime NULL AFTER `module_val`;');
CALL add_element_unless_exists('column', 'sys_module', 'update_time', 'ALTER TABLE sys_module ADD COLUMN `update_time` datetime NULL AFTER `create_time`;');
CALL add_element_unless_exists('index', 'sys_module', 'PRIMARY', 'ALTER TABLE sys_module ADD UNIQUE INDEX `PRIMARY` (`module_id`) USING BTREE;');

-- 更新表 sys_module_node 所有字段和索引
CALL add_element_unless_exists('column', 'sys_module_node', 'node_id', 'ALTER TABLE sys_module_node ADD COLUMN `node_id` char(32) NOT NULL;');
CALL add_element_unless_exists('column', 'sys_module_node', 'node_module', 'ALTER TABLE sys_module_node ADD COLUMN `node_module` char(32) NULL AFTER `node_id`;');
CALL add_element_unless_exists('column', 'sys_module_node', 'node_name', 'ALTER TABLE sys_module_node ADD COLUMN `node_name` varchar(50) NULL AFTER `node_module`;');
CALL add_element_unless_exists('column', 'sys_module_node', 'node_url', 'ALTER TABLE sys_module_node ADD COLUMN `node_url` varchar(100) NULL AFTER `node_name`;');
CALL add_element_unless_exists('column', 'sys_module_node', 'node_val', 'ALTER TABLE sys_module_node ADD COLUMN `node_val` varchar(50) NULL AFTER `node_url`;');
CALL add_element_unless_exists('column', 'sys_module_node', 'node_order', 'ALTER TABLE sys_module_node ADD COLUMN `node_order` int(5) NULL AFTER `node_val`;');
CALL add_element_unless_exists('column', 'sys_module_node', 'node_desc', 'ALTER TABLE sys_module_node ADD COLUMN `node_desc` varchar(200) NULL AFTER `node_order`;');
CALL add_element_unless_exists('column', 'sys_module_node', 'node_i18n_code', 'ALTER TABLE sys_module_node ADD COLUMN `node_i18n_code` varchar(255) NULL AFTER `node_desc`;');
CALL add_element_unless_exists('index', 'sys_module_node', 'PRIMARY', 'ALTER TABLE sys_module_node ADD UNIQUE INDEX `PRIMARY` (`node_id`) USING BTREE;');

-- 更新表 sys_org 所有字段和索引
CALL add_element_unless_exists('column', 'sys_org', 'id', 'ALTER TABLE sys_org ADD COLUMN `id` char(32) NOT NULL;');
CALL add_element_unless_exists('column', 'sys_org', 'pid', 'ALTER TABLE sys_org ADD COLUMN `pid` char(32) NULL AFTER `id`;');
CALL add_element_unless_exists('column', 'sys_org', 'name', 'ALTER TABLE sys_org ADD COLUMN `name` varchar(200) NULL AFTER `pid`;');
CALL add_element_unless_exists('column', 'sys_org', 'description', 'ALTER TABLE sys_org ADD COLUMN `description` varchar(200) NULL AFTER `name`;');
CALL add_element_unless_exists('column', 'sys_org', 'remark', 'ALTER TABLE sys_org ADD COLUMN `remark` varchar(200) NULL AFTER `description`;');
CALL add_element_unless_exists('column', 'sys_org', 'create_time', 'ALTER TABLE sys_org ADD COLUMN `create_time` datetime NULL AFTER `remark`;');
CALL add_element_unless_exists('column', 'sys_org', 'update_time', 'ALTER TABLE sys_org ADD COLUMN `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP AFTER `create_time`;');
CALL add_element_unless_exists('column', 'sys_org', 'is_show', 'ALTER TABLE sys_org ADD COLUMN `is_show` char(1) NOT NULL DEFAULT 1 AFTER `update_time`;');
CALL add_element_unless_exists('index', 'sys_org', 'PRIMARY', 'ALTER TABLE sys_org ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 sys_org_role 所有字段和索引
CALL add_element_unless_exists('column', 'sys_org_role', 'id', 'ALTER TABLE sys_org_role ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'sys_org_role', 'role_id', 'ALTER TABLE sys_org_role ADD COLUMN `role_id` char(32) NULL AFTER `id`;');
CALL add_element_unless_exists('column', 'sys_org_role', 'org_id', 'ALTER TABLE sys_org_role ADD COLUMN `org_id` char(32) NULL AFTER `role_id`;');
CALL add_element_unless_exists('column', 'sys_org_role', 'create_time', 'ALTER TABLE sys_org_role ADD COLUMN `create_time` datetime NULL AFTER `org_id`;');
CALL add_element_unless_exists('index', 'sys_org_role', 'PRIMARY', 'ALTER TABLE sys_org_role ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 sys_org_user 所有字段和索引
CALL add_element_unless_exists('column', 'sys_org_user', 'id', 'ALTER TABLE sys_org_user ADD COLUMN `id` char(32) NOT NULL;');
CALL add_element_unless_exists('column', 'sys_org_user', 'org_id', 'ALTER TABLE sys_org_user ADD COLUMN `org_id` char(32) NULL AFTER `id`;');
CALL add_element_unless_exists('column', 'sys_org_user', 'user_id', 'ALTER TABLE sys_org_user ADD COLUMN `user_id` char(32) NULL AFTER `org_id`;');
CALL add_element_unless_exists('column', 'sys_org_user', 'create_time', 'ALTER TABLE sys_org_user ADD COLUMN `create_time` datetime NULL AFTER `user_id`;');
CALL add_element_unless_exists('column', 'sys_org_user', 'update_time', 'ALTER TABLE sys_org_user ADD COLUMN `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP AFTER `create_time`;');
CALL add_element_unless_exists('index', 'sys_org_user', 'PRIMARY', 'ALTER TABLE sys_org_user ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 sys_role 所有字段和索引
CALL add_element_unless_exists('column', 'sys_role', 'role_id', 'ALTER TABLE sys_role ADD COLUMN `role_id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'sys_role', 'role_name', 'ALTER TABLE sys_role ADD COLUMN `role_name` varchar(50) NULL AFTER `role_id`;');
CALL add_element_unless_exists('column', 'sys_role', 'role_remark', 'ALTER TABLE sys_role ADD COLUMN `role_remark` varchar(200) NULL AFTER `role_name`;');
CALL add_element_unless_exists('column', 'sys_role', 'role_desc', 'ALTER TABLE sys_role ADD COLUMN `role_desc` varchar(200) NULL AFTER `role_remark`;');
CALL add_element_unless_exists('column', 'sys_role', 'role_status', 'ALTER TABLE sys_role ADD COLUMN `role_status` int(1) NULL AFTER `role_desc`;');
CALL add_element_unless_exists('column', 'sys_role', 'create_time', 'ALTER TABLE sys_role ADD COLUMN `create_time` datetime NULL AFTER `role_status`;');
CALL add_element_unless_exists('column', 'sys_role', 'update_time', 'ALTER TABLE sys_role ADD COLUMN `update_time` datetime NULL AFTER `create_time`;');
CALL add_element_unless_exists('index', 'sys_role', 'PRIMARY', 'ALTER TABLE sys_role ADD UNIQUE INDEX `PRIMARY` (`role_id`) USING BTREE;');

-- 更新表 sys_role_user 所有字段和索引
CALL add_element_unless_exists('column', 'sys_role_user', 'id', 'ALTER TABLE sys_role_user ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'sys_role_user', 'role_id', 'ALTER TABLE sys_role_user ADD COLUMN `role_id` int(11) NULL AFTER `id`;');
CALL add_element_unless_exists('column', 'sys_role_user', 'user_id', 'ALTER TABLE sys_role_user ADD COLUMN `user_id` int(11) NULL AFTER `role_id`;');
CALL add_element_unless_exists('column', 'sys_role_user', 'create_time', 'ALTER TABLE sys_role_user ADD COLUMN `create_time` datetime NULL AFTER `user_id`;');
CALL add_element_unless_exists('index', 'sys_role_user', 'PRIMARY', 'ALTER TABLE sys_role_user ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 sys_user 所有字段和索引
CALL add_element_unless_exists('column', 'sys_user', 'user_id', 'ALTER TABLE sys_user ADD COLUMN `user_id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'sys_user', 'user_name', 'ALTER TABLE sys_user ADD COLUMN `user_name` varchar(50) NULL AFTER `user_id`;');
CALL add_element_unless_exists('column', 'sys_user', 'user_account', 'ALTER TABLE sys_user ADD COLUMN `user_account` varchar(50) NULL AFTER `user_name`;');
CALL add_element_unless_exists('column', 'sys_user', 'user_pwd', 'ALTER TABLE sys_user ADD COLUMN `user_pwd` varchar(50) NULL AFTER `user_account`;');
CALL add_element_unless_exists('column', 'sys_user', 'user_phone', 'ALTER TABLE sys_user ADD COLUMN `user_phone` varchar(11) NULL AFTER `user_pwd`;');
CALL add_element_unless_exists('column', 'sys_user', 'user_remark', 'ALTER TABLE sys_user ADD COLUMN `user_remark` varchar(200) NULL AFTER `user_phone`;');
CALL add_element_unless_exists('column', 'sys_user', 'user_desc', 'ALTER TABLE sys_user ADD COLUMN `user_desc` varchar(500) NULL AFTER `user_remark`;');
CALL add_element_unless_exists('column', 'sys_user', 'user_status', 'ALTER TABLE sys_user ADD COLUMN `user_status` int(1) NULL AFTER `user_desc`;');
CALL add_element_unless_exists('column', 'sys_user', 'user_admin', 'ALTER TABLE sys_user ADD COLUMN `user_admin` int(1) NULL AFTER `user_status`;');
CALL add_element_unless_exists('column', 'sys_user', 'create_time', 'ALTER TABLE sys_user ADD COLUMN `create_time` datetime NULL AFTER `user_admin`;');
CALL add_element_unless_exists('column', 'sys_user', 'update_time', 'ALTER TABLE sys_user ADD COLUMN `update_time` datetime NULL AFTER `create_time`;');
CALL add_element_unless_exists('index', 'sys_user', 'PRIMARY', 'ALTER TABLE sys_user ADD UNIQUE INDEX `PRIMARY` (`user_id`) USING BTREE;');

-- 更新表 t_ad 所有字段和索引
CALL add_element_unless_exists('column', 't_ad', 'Id', 'ALTER TABLE t_ad ADD COLUMN `Id` int(8) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_ad', 'ParkId', 'ALTER TABLE t_ad ADD COLUMN `ParkId` int(8) NOT NULL DEFAULT 0 AFTER `Id`;');
CALL add_element_unless_exists('column', 't_ad', 'ComputerId', 'ALTER TABLE t_ad ADD COLUMN `ComputerId` varchar(20) NOT NULL DEFAULT AFTER `ParkId`;');
CALL add_element_unless_exists('column', 't_ad', 'AdType', 'ALTER TABLE t_ad ADD COLUMN `AdType` tinyint(4) NOT NULL DEFAULT 0 AFTER `ComputerId`;');
CALL add_element_unless_exists('column', 't_ad', 'PlayType', 'ALTER TABLE t_ad ADD COLUMN `PlayType` int(8) NOT NULL DEFAULT 1 AFTER `AdType`;');
CALL add_element_unless_exists('column', 't_ad', 'VideoUrl', 'ALTER TABLE t_ad ADD COLUMN `VideoUrl` varchar(1000) NOT NULL DEFAULT AFTER `PlayType`;');
CALL add_element_unless_exists('column', 't_ad', 'ImagePlayTime', 'ALTER TABLE t_ad ADD COLUMN `ImagePlayTime` int(8) NOT NULL DEFAULT 0 AFTER `VideoUrl`;');
CALL add_element_unless_exists('column', 't_ad', 'ImagePlayStyle', 'ALTER TABLE t_ad ADD COLUMN `ImagePlayStyle` int(8) NOT NULL DEFAULT 0 AFTER `ImagePlayTime`;');
CALL add_element_unless_exists('column', 't_ad', 'ImagesUrl', 'ALTER TABLE t_ad ADD COLUMN `ImagesUrl` varchar(1000) NOT NULL DEFAULT AFTER `ImagePlayStyle`;');
CALL add_element_unless_exists('index', 't_ad', 'PRIMARY', 'ALTER TABLE t_ad ADD UNIQUE INDEX `PRIMARY` (`Id`) USING BTREE;');

-- 更新表 t_adsub 所有字段和索引
CALL add_element_unless_exists('column', 't_adsub', 'id', 'ALTER TABLE t_adsub ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_adsub', 'ObjectId', 'ALTER TABLE t_adsub ADD COLUMN `ObjectId` int(8) NOT NULL DEFAULT 1 AFTER `id`;');
CALL add_element_unless_exists('column', 't_adsub', 'FormId', 'ALTER TABLE t_adsub ADD COLUMN `FormId` int(11) NOT NULL DEFAULT 0 AFTER `ObjectId`;');
CALL add_element_unless_exists('column', 't_adsub', 'FilePath', 'ALTER TABLE t_adsub ADD COLUMN `FilePath` varchar(500) NOT NULL DEFAULT AFTER `FormId`;');
CALL add_element_unless_exists('column', 't_adsub', 'Remark', 'ALTER TABLE t_adsub ADD COLUMN `Remark` varchar(255) NOT NULL DEFAULT AFTER `FilePath`;');
CALL add_element_unless_exists('column', 't_adsub', 'FileType', 'ALTER TABLE t_adsub ADD COLUMN `FileType` tinyint(4) NOT NULL DEFAULT 0 AFTER `Remark`;');
CALL add_element_unless_exists('index', 't_adsub', 'PRIMARY', 'ALTER TABLE t_adsub ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_area_device 所有字段和索引
CALL add_element_unless_exists('column', 't_area_device', 'id', 'ALTER TABLE t_area_device ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_area_device', 'deviceaddr', 'ALTER TABLE t_area_device ADD COLUMN `deviceaddr` int(11) NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 't_area_device', 'areaid', 'ALTER TABLE t_area_device ADD COLUMN `areaid` int(11) NULL DEFAULT 0 AFTER `deviceaddr`;');
CALL add_element_unless_exists('column', 't_area_device', 'type', 'ALTER TABLE t_area_device ADD COLUMN `type` int(11) NULL DEFAULT 0 AFTER `areaid`;');
CALL add_element_unless_exists('column', 't_area_device', 'outareaid', 'ALTER TABLE t_area_device ADD COLUMN `outareaid` varchar(255) NULL AFTER `type`;');
CALL add_element_unless_exists('index', 't_area_device', 'PRIMARY', 'ALTER TABLE t_area_device ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_businfo 所有字段和索引
CALL add_element_unless_exists('column', 't_businfo', 'id', 'ALTER TABLE t_businfo ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_businfo', 'busid', 'ALTER TABLE t_businfo ADD COLUMN `busid` varchar(32) NOT NULL AFTER `id`;');
CALL add_element_unless_exists('column', 't_businfo', 'lockDtuId', 'ALTER TABLE t_businfo ADD COLUMN `lockDtuId` varchar(32) NOT NULL AFTER `busid`;');
CALL add_element_unless_exists('column', 't_businfo', 'lockPos', 'ALTER TABLE t_businfo ADD COLUMN `lockPos` varchar(32) NOT NULL AFTER `lockDtuId`;');
CALL add_element_unless_exists('column', 't_businfo', 'autoLock', 'ALTER TABLE t_businfo ADD COLUMN `autoLock` int(11) NOT NULL DEFAULT 15 AFTER `lockPos`;');
CALL add_element_unless_exists('column', 't_businfo', 'lockStatus', 'ALTER TABLE t_businfo ADD COLUMN `lockStatus` int(11) NOT NULL DEFAULT 0 AFTER `autoLock`;');
CALL add_element_unless_exists('column', 't_businfo', 'detectDtuId', 'ALTER TABLE t_businfo ADD COLUMN `detectDtuId` varchar(32) NOT NULL AFTER `lockStatus`;');
CALL add_element_unless_exists('column', 't_businfo', 'detectPos', 'ALTER TABLE t_businfo ADD COLUMN `detectPos` varchar(32) NOT NULL AFTER `detectDtuId`;');
CALL add_element_unless_exists('column', 't_businfo', 'detectStatus', 'ALTER TABLE t_businfo ADD COLUMN `detectStatus` int(11) NOT NULL DEFAULT 0 AFTER `detectPos`;');
CALL add_element_unless_exists('column', 't_businfo', 'updateTime', 'ALTER TABLE t_businfo ADD COLUMN `updateTime` datetime NULL AFTER `detectStatus`;');
CALL add_element_unless_exists('index', 't_businfo', 'PRIMARY', 'ALTER TABLE t_businfo ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');
CALL add_element_unless_exists('index', 't_businfo', 'busid', 'ALTER TABLE t_businfo ADD UNIQUE INDEX `busid` (`busid`) USING BTREE;');

-- 更新表 t_display_config 所有字段和索引
CALL add_element_unless_exists('column', 't_display_config', 'id', 'ALTER TABLE t_display_config ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_display_config', 'lot_id', 'ALTER TABLE t_display_config ADD COLUMN `lot_id` int(11) NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 't_display_config', 'title_top', 'ALTER TABLE t_display_config ADD COLUMN `title_top` double(255,0) NULL DEFAULT 0 AFTER `lot_id`;');
CALL add_element_unless_exists('column', 't_display_config', 'title_left', 'ALTER TABLE t_display_config ADD COLUMN `title_left` double NULL DEFAULT 0 AFTER `title_top`;');
CALL add_element_unless_exists('column', 't_display_config', 'title_font_size', 'ALTER TABLE t_display_config ADD COLUMN `title_font_size` double NULL DEFAULT 0 AFTER `title_left`;');
CALL add_element_unless_exists('column', 't_display_config', 'title_color', 'ALTER TABLE t_display_config ADD COLUMN `title_color` varchar(255) NULL DEFAULT #fff AFTER `title_font_size`;');
CALL add_element_unless_exists('column', 't_display_config', 'title_text', 'ALTER TABLE t_display_config ADD COLUMN `title_text` varchar(255) NULL DEFAULT AFTER `title_color`;');
CALL add_element_unless_exists('column', 't_display_config', 'led_font_size', 'ALTER TABLE t_display_config ADD COLUMN `led_font_size` double NULL DEFAULT 0 AFTER `title_text`;');
CALL add_element_unless_exists('column', 't_display_config', 'led_width', 'ALTER TABLE t_display_config ADD COLUMN `led_width` double NULL DEFAULT 0 AFTER `led_font_size`;');
CALL add_element_unless_exists('column', 't_display_config', 'led_height', 'ALTER TABLE t_display_config ADD COLUMN `led_height` double NULL DEFAULT 0 AFTER `led_width`;');
CALL add_element_unless_exists('column', 't_display_config', 'led_common_color', 'ALTER TABLE t_display_config ADD COLUMN `led_common_color` varchar(255) NULL DEFAULT #00ffff AFTER `led_height`;');
CALL add_element_unless_exists('column', 't_display_config', 'led_full_color', 'ALTER TABLE t_display_config ADD COLUMN `led_full_color` varchar(255) NULL DEFAULT #ff1100 AFTER `led_common_color`;');
CALL add_element_unless_exists('column', 't_display_config', 'ico_width', 'ALTER TABLE t_display_config ADD COLUMN `ico_width` double NULL DEFAULT 0 AFTER `led_full_color`;');
CALL add_element_unless_exists('column', 't_display_config', 'ico_height', 'ALTER TABLE t_display_config ADD COLUMN `ico_height` double NULL DEFAULT 0 AFTER `ico_width`;');
CALL add_element_unless_exists('column', 't_display_config', 'ico_woman_img', 'ALTER TABLE t_display_config ADD COLUMN `ico_woman_img` varchar(255) NULL DEFAULT AFTER `ico_height`;');
CALL add_element_unless_exists('column', 't_display_config', 'ico_woman_actimg', 'ALTER TABLE t_display_config ADD COLUMN `ico_woman_actimg` varchar(255) NULL DEFAULT AFTER `ico_woman_img`;');
CALL add_element_unless_exists('column', 't_display_config', 'ico_man_img', 'ALTER TABLE t_display_config ADD COLUMN `ico_man_img` varchar(255) NULL DEFAULT AFTER `ico_woman_actimg`;');
CALL add_element_unless_exists('column', 't_display_config', 'ico_man_actimg', 'ALTER TABLE t_display_config ADD COLUMN `ico_man_actimg` varchar(255) NULL DEFAULT AFTER `ico_man_img`;');
CALL add_element_unless_exists('column', 't_display_config', 'create_time', 'ALTER TABLE t_display_config ADD COLUMN `create_time` datetime NULL AFTER `ico_man_actimg`;');
CALL add_element_unless_exists('column', 't_display_config', 'update_time', 'ALTER TABLE t_display_config ADD COLUMN `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP AFTER `create_time`;');
CALL add_element_unless_exists('index', 't_display_config', 'PRIMARY', 'ALTER TABLE t_display_config ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_events 所有字段和索引
CALL add_element_unless_exists('column', 't_events', 'id', 'ALTER TABLE t_events ADD COLUMN `id` bigint(20) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_events', 'evtType', 'ALTER TABLE t_events ADD COLUMN `evtType` int(11) NOT NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 't_events', 'imgName', 'ALTER TABLE t_events ADD COLUMN `imgName` varchar(50) NOT NULL DEFAULT 0 AFTER `evtType`;');
CALL add_element_unless_exists('column', 't_events', 'dspIp', 'ALTER TABLE t_events ADD COLUMN `dspIp` varchar(32) NOT NULL DEFAULT 0 AFTER `imgName`;');
CALL add_element_unless_exists('column', 't_events', 'evtTime', 'ALTER TABLE t_events ADD COLUMN `evtTime` varchar(32) NOT NULL DEFAULT 0 AFTER `dspIp`;');
CALL add_element_unless_exists('column', 't_events', 'inAddr', 'ALTER TABLE t_events ADD COLUMN `inAddr` varchar(32) NOT NULL DEFAULT 0 AFTER `evtTime`;');
CALL add_element_unless_exists('column', 't_events', 'inTime', 'ALTER TABLE t_events ADD COLUMN `inTime` varchar(32) NOT NULL DEFAULT 0 AFTER `inAddr`;');
CALL add_element_unless_exists('column', 't_events', 'outAddr', 'ALTER TABLE t_events ADD COLUMN `outAddr` varchar(32) NOT NULL DEFAULT 0 AFTER `inTime`;');
CALL add_element_unless_exists('column', 't_events', 'outTime', 'ALTER TABLE t_events ADD COLUMN `outTime` varchar(32) NOT NULL DEFAULT 0 AFTER `outAddr`;');
CALL add_element_unless_exists('column', 't_events', 'money', 'ALTER TABLE t_events ADD COLUMN `money` int(11) NOT NULL DEFAULT 0 AFTER `outTime`;');
CALL add_element_unless_exists('column', 't_events', 'carNo', 'ALTER TABLE t_events ADD COLUMN `carNo` varchar(32) NOT NULL DEFAULT 0 AFTER `money`;');
CALL add_element_unless_exists('column', 't_events', 'carplateNum', 'ALTER TABLE t_events ADD COLUMN `carplateNum` varchar(2000) NULL AFTER `carNo`;');
CALL add_element_unless_exists('column', 't_events', 'carplateType', 'ALTER TABLE t_events ADD COLUMN `carplateType` int(1) unsigned NOT NULL DEFAULT 0 AFTER `carplateNum`;');
CALL add_element_unless_exists('column', 't_events', 'carplateProty1', 'ALTER TABLE t_events ADD COLUMN `carplateProty1` int(3) unsigned NOT NULL DEFAULT 0 AFTER `carplateType`;');
CALL add_element_unless_exists('column', 't_events', 'carplateProty2', 'ALTER TABLE t_events ADD COLUMN `carplateProty2` int(3) unsigned NOT NULL DEFAULT 0 AFTER `carplateProty1`;');
CALL add_element_unless_exists('column', 't_events', 'enchargeFlag', 'ALTER TABLE t_events ADD COLUMN `enchargeFlag` int(1) unsigned NOT NULL DEFAULT 0 AFTER `carplateProty2`;');
CALL add_element_unless_exists('column', 't_events', 'serialType', 'ALTER TABLE t_events ADD COLUMN `serialType` int(1) unsigned NOT NULL DEFAULT 0 AFTER `enchargeFlag`;');
CALL add_element_unless_exists('column', 't_events', 'serialNo', 'ALTER TABLE t_events ADD COLUMN `serialNo` varchar(500) NOT NULL DEFAULT 0 AFTER `serialType`;');
CALL add_element_unless_exists('column', 't_events', 'inImgName', 'ALTER TABLE t_events ADD COLUMN `inImgName` varchar(50) NULL DEFAULT AFTER `serialNo`;');
CALL add_element_unless_exists('column', 't_events', 'CarColor', 'ALTER TABLE t_events ADD COLUMN `CarColor` varchar(45) NOT NULL DEFAULT AFTER `inImgName`;');
CALL add_element_unless_exists('column', 't_events', 'CarBrand', 'ALTER TABLE t_events ADD COLUMN `CarBrand` varchar(45) NOT NULL DEFAULT AFTER `CarColor`;');
CALL add_element_unless_exists('column', 't_events', 'RecogEnable', 'ALTER TABLE t_events ADD COLUMN `RecogEnable` int(8) NOT NULL DEFAULT 0 AFTER `CarBrand`;');
CALL add_element_unless_exists('column', 't_events', 'CarplateColor', 'ALTER TABLE t_events ADD COLUMN `CarplateColor` varchar(45) NOT NULL DEFAULT AFTER `RecogEnable`;');
CALL add_element_unless_exists('column', 't_events', 'CameraId', 'ALTER TABLE t_events ADD COLUMN `CameraId` int(11) NOT NULL DEFAULT 0 AFTER `CarplateColor`;');
CALL add_element_unless_exists('column', 't_events', 'remark', 'ALTER TABLE t_events ADD COLUMN `remark` varchar(50) NULL DEFAULT AFTER `CameraId`;');
CALL add_element_unless_exists('index', 't_events', 'PRIMARY', 'ALTER TABLE t_events ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_faceinfo 所有字段和索引
CALL add_element_unless_exists('column', 't_faceinfo', 'id', 'ALTER TABLE t_faceinfo ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_faceinfo', 'plateNo', 'ALTER TABLE t_faceinfo ADD COLUMN `plateNo` varchar(50) NULL DEFAULT AFTER `id`;');
CALL add_element_unless_exists('column', 't_faceinfo', 'faceInfo', 'ALTER TABLE t_faceinfo ADD COLUMN `faceInfo` text NULL AFTER `plateNo`;');
CALL add_element_unless_exists('column', 't_faceinfo', 'createTime', 'ALTER TABLE t_faceinfo ADD COLUMN `createTime` datetime NULL AFTER `faceInfo`;');
CALL add_element_unless_exists('column', 't_faceinfo', 'isTemp', 'ALTER TABLE t_faceinfo ADD COLUMN `isTemp` int(11) NULL DEFAULT 0 AFTER `createTime`;');
CALL add_element_unless_exists('column', 't_faceinfo', 'faceId', 'ALTER TABLE t_faceinfo ADD COLUMN `faceId` varchar(50) NULL DEFAULT AFTER `isTemp`;');
CALL add_element_unless_exists('index', 't_faceinfo', 'PRIMARY', 'ALTER TABLE t_faceinfo ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_fcs_seller 所有字段和索引
CALL add_element_unless_exists('column', 't_fcs_seller', 'id', 'ALTER TABLE t_fcs_seller ADD COLUMN `id` int(20) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_fcs_seller', 'seller_name', 'ALTER TABLE t_fcs_seller ADD COLUMN `seller_name` varchar(50) NULL DEFAULT AFTER `id`;');
CALL add_element_unless_exists('column', 't_fcs_seller', 'seller_code', 'ALTER TABLE t_fcs_seller ADD COLUMN `seller_code` varchar(50) NULL DEFAULT AFTER `seller_name`;');
CALL add_element_unless_exists('column', 't_fcs_seller', 'pos_x', 'ALTER TABLE t_fcs_seller ADD COLUMN `pos_x` int(4) NULL DEFAULT 0 AFTER `seller_code`;');
CALL add_element_unless_exists('column', 't_fcs_seller', 'pos_y', 'ALTER TABLE t_fcs_seller ADD COLUMN `pos_y` int(4) NULL DEFAULT 0 AFTER `pos_x`;');
CALL add_element_unless_exists('column', 't_fcs_seller', 'floor_id', 'ALTER TABLE t_fcs_seller ADD COLUMN `floor_id` int(8) NULL DEFAULT 0 AFTER `pos_y`;');
CALL add_element_unless_exists('column', 't_fcs_seller', 'is_delete', 'ALTER TABLE t_fcs_seller ADD COLUMN `is_delete` int(1) NULL DEFAULT 0 AFTER `floor_id`;');
CALL add_element_unless_exists('column', 't_fcs_seller', 'create_time', 'ALTER TABLE t_fcs_seller ADD COLUMN `create_time` datetime NULL AFTER `is_delete`;');
CALL add_element_unless_exists('column', 't_fcs_seller', 'update_time', 'ALTER TABLE t_fcs_seller ADD COLUMN `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP AFTER `create_time`;');
CALL add_element_unless_exists('index', 't_fcs_seller', 'PRIMARY', 'ALTER TABLE t_fcs_seller ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_findcar_events 所有字段和索引
CALL add_element_unless_exists('column', 't_findcar_events', 'id', 'ALTER TABLE t_findcar_events ADD COLUMN `id` bigint(20) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_findcar_events', 'evtType', 'ALTER TABLE t_findcar_events ADD COLUMN `evtType` int(11) NOT NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'imgName', 'ALTER TABLE t_findcar_events ADD COLUMN `imgName` varchar(255) NOT NULL DEFAULT 0 AFTER `evtType`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'dspIp', 'ALTER TABLE t_findcar_events ADD COLUMN `dspIp` varchar(32) NOT NULL DEFAULT 0 AFTER `imgName`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'evtTime', 'ALTER TABLE t_findcar_events ADD COLUMN `evtTime` varchar(32) NOT NULL DEFAULT 0 AFTER `dspIp`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'inAddr', 'ALTER TABLE t_findcar_events ADD COLUMN `inAddr` varchar(32) NOT NULL DEFAULT 0 AFTER `evtTime`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'inTime', 'ALTER TABLE t_findcar_events ADD COLUMN `inTime` varchar(32) NOT NULL DEFAULT 0 AFTER `inAddr`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'outAddr', 'ALTER TABLE t_findcar_events ADD COLUMN `outAddr` varchar(32) NOT NULL DEFAULT 0 AFTER `inTime`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'outTime', 'ALTER TABLE t_findcar_events ADD COLUMN `outTime` varchar(32) NOT NULL DEFAULT 0 AFTER `outAddr`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'money', 'ALTER TABLE t_findcar_events ADD COLUMN `money` int(11) NOT NULL DEFAULT 0 AFTER `outTime`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'carNo', 'ALTER TABLE t_findcar_events ADD COLUMN `carNo` varchar(32) NOT NULL DEFAULT 0 AFTER `money`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'carplateNum', 'ALTER TABLE t_findcar_events ADD COLUMN `carplateNum` varchar(45) NOT NULL DEFAULT 0 AFTER `carNo`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'carplateType', 'ALTER TABLE t_findcar_events ADD COLUMN `carplateType` int(1) unsigned NOT NULL DEFAULT 0 AFTER `carplateNum`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'carplateProty1', 'ALTER TABLE t_findcar_events ADD COLUMN `carplateProty1` int(3) unsigned NOT NULL DEFAULT 0 AFTER `carplateType`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'carplateProty2', 'ALTER TABLE t_findcar_events ADD COLUMN `carplateProty2` int(3) unsigned NOT NULL DEFAULT 0 AFTER `carplateProty1`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'enchargeFlag', 'ALTER TABLE t_findcar_events ADD COLUMN `enchargeFlag` int(1) unsigned NOT NULL DEFAULT 0 AFTER `carplateProty2`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'serialType', 'ALTER TABLE t_findcar_events ADD COLUMN `serialType` int(1) unsigned NOT NULL DEFAULT 0 AFTER `enchargeFlag`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'serialNo', 'ALTER TABLE t_findcar_events ADD COLUMN `serialNo` varchar(45) NOT NULL DEFAULT 0 AFTER `serialType`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'inImgName', 'ALTER TABLE t_findcar_events ADD COLUMN `inImgName` varchar(50) NULL DEFAULT AFTER `serialNo`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'CarColor', 'ALTER TABLE t_findcar_events ADD COLUMN `CarColor` varchar(45) NOT NULL DEFAULT AFTER `inImgName`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'CarBrand', 'ALTER TABLE t_findcar_events ADD COLUMN `CarBrand` varchar(45) NOT NULL DEFAULT AFTER `CarColor`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'RecogEnable', 'ALTER TABLE t_findcar_events ADD COLUMN `RecogEnable` int(8) NOT NULL DEFAULT 0 AFTER `CarBrand`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'CarplateColor', 'ALTER TABLE t_findcar_events ADD COLUMN `CarplateColor` varchar(45) NOT NULL DEFAULT AFTER `RecogEnable`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'CameraId', 'ALTER TABLE t_findcar_events ADD COLUMN `CameraId` int(11) NOT NULL DEFAULT 0 AFTER `CarplateColor`;');
CALL add_element_unless_exists('column', 't_findcar_events', 'remark', 'ALTER TABLE t_findcar_events ADD COLUMN `remark` varchar(50) NULL DEFAULT AFTER `CameraId`;');
CALL add_element_unless_exists('index', 't_findcar_events', 'PRIMARY', 'ALTER TABLE t_findcar_events ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_findcar_upload 所有字段和索引
CALL add_element_unless_exists('column', 't_findcar_upload', 'id', 'ALTER TABLE t_findcar_upload ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_findcar_upload', 'code', 'ALTER TABLE t_findcar_upload ADD COLUMN `code` varchar(20) NOT NULL DEFAULT AFTER `id`;');
CALL add_element_unless_exists('column', 't_findcar_upload', 'uploadTime', 'ALTER TABLE t_findcar_upload ADD COLUMN `uploadTime` datetime NULL AFTER `code`;');
CALL add_element_unless_exists('column', 't_findcar_upload', 'remark', 'ALTER TABLE t_findcar_upload ADD COLUMN `remark` varchar(256) NULL DEFAULT AFTER `uploadTime`;');
CALL add_element_unless_exists('index', 't_findcar_upload', 'PRIMARY', 'ALTER TABLE t_findcar_upload ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_ibeacon 所有字段和索引
CALL add_element_unless_exists('column', 't_ibeacon', 'id', 'ALTER TABLE t_ibeacon ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_ibeacon', 'lotCode', 'ALTER TABLE t_ibeacon ADD COLUMN `lotCode` int(11) NOT NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 't_ibeacon', 'UUID', 'ALTER TABLE t_ibeacon ADD COLUMN `UUID` varchar(255) NOT NULL DEFAULT AFTER `lotCode`;');
CALL add_element_unless_exists('column', 't_ibeacon', 'Major', 'ALTER TABLE t_ibeacon ADD COLUMN `Major` varchar(255) NOT NULL DEFAULT AFTER `UUID`;');
CALL add_element_unless_exists('column', 't_ibeacon', 'Minor', 'ALTER TABLE t_ibeacon ADD COLUMN `Minor` varchar(255) NOT NULL DEFAULT AFTER `Major`;');
CALL add_element_unless_exists('column', 't_ibeacon', 'Addr', 'ALTER TABLE t_ibeacon ADD COLUMN `Addr` int(11) NOT NULL DEFAULT 0 AFTER `Minor`;');
CALL add_element_unless_exists('column', 't_ibeacon', 'PosX', 'ALTER TABLE t_ibeacon ADD COLUMN `PosX` int(10) unsigned NOT NULL DEFAULT 0 AFTER `Addr`;');
CALL add_element_unless_exists('column', 't_ibeacon', 'PosY', 'ALTER TABLE t_ibeacon ADD COLUMN `PosY` int(10) unsigned NOT NULL DEFAULT 0 AFTER `PosX`;');
CALL add_element_unless_exists('column', 't_ibeacon', 'Mid', 'ALTER TABLE t_ibeacon ADD COLUMN `Mid` int(10) unsigned NOT NULL DEFAULT 0 AFTER `PosY`;');
CALL add_element_unless_exists('index', 't_ibeacon', 'PRIMARY', 'ALTER TABLE t_ibeacon ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');
CALL add_element_unless_exists('index', 't_ibeacon', 'UK_t_ibeacon', 'ALTER TABLE t_ibeacon ADD UNIQUE INDEX `UK_t_ibeacon` (`UUID`) USING BTREE;');
CALL add_element_unless_exists('index', 't_ibeacon', 'UK_t_ibeacon', 'ALTER TABLE t_ibeacon ADD UNIQUE INDEX `UK_t_ibeacon` (`Major`) USING BTREE;');
CALL add_element_unless_exists('index', 't_ibeacon', 'UK_t_ibeacon', 'ALTER TABLE t_ibeacon ADD UNIQUE INDEX `UK_t_ibeacon` (`Minor`) USING BTREE;');

-- 更新表 t_illegal_report 所有字段和索引
CALL add_element_unless_exists('column', 't_illegal_report', 'id', 'ALTER TABLE t_illegal_report ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_illegal_report', 'carPlateNum', 'ALTER TABLE t_illegal_report ADD COLUMN `carPlateNum` varchar(50) NULL DEFAULT AFTER `id`;');
CALL add_element_unless_exists('column', 't_illegal_report', 'parkTime', 'ALTER TABLE t_illegal_report ADD COLUMN `parkTime` datetime NULL AFTER `carPlateNum`;');
CALL add_element_unless_exists('column', 't_illegal_report', 'busNumber', 'ALTER TABLE t_illegal_report ADD COLUMN `busNumber` varchar(50) NULL DEFAULT AFTER `parkTime`;');
CALL add_element_unless_exists('column', 't_illegal_report', 'illegalPlate', 'ALTER TABLE t_illegal_report ADD COLUMN `illegalPlate` varchar(50) NULL DEFAULT AFTER `busNumber`;');
CALL add_element_unless_exists('column', 't_illegal_report', 'imgName', 'ALTER TABLE t_illegal_report ADD COLUMN `imgName` varchar(100) NULL DEFAULT AFTER `illegalPlate`;');
CALL add_element_unless_exists('column', 't_illegal_report', 'isAlarm', 'ALTER TABLE t_illegal_report ADD COLUMN `isAlarm` int(11) NOT NULL DEFAULT 0 AFTER `imgName`;');
CALL add_element_unless_exists('column', 't_illegal_report', 'remark', 'ALTER TABLE t_illegal_report ADD COLUMN `remark` varchar(512) NULL DEFAULT AFTER `isAlarm`;');
CALL add_element_unless_exists('column', 't_illegal_report', 'createTime', 'ALTER TABLE t_illegal_report ADD COLUMN `createTime` datetime NULL AFTER `remark`;');
CALL add_element_unless_exists('index', 't_illegal_report', 'PRIMARY', 'ALTER TABLE t_illegal_report ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_illegal_spaces 所有字段和索引
CALL add_element_unless_exists('column', 't_illegal_spaces', 'id', 'ALTER TABLE t_illegal_spaces ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_illegal_spaces', 'carPlateNum', 'ALTER TABLE t_illegal_spaces ADD COLUMN `carPlateNum` varchar(50) NULL DEFAULT AFTER `id`;');
CALL add_element_unless_exists('column', 't_illegal_spaces', 'busNumber', 'ALTER TABLE t_illegal_spaces ADD COLUMN `busNumber` varchar(50) NULL DEFAULT AFTER `carPlateNum`;');
CALL add_element_unless_exists('column', 't_illegal_spaces', 'owner', 'ALTER TABLE t_illegal_spaces ADD COLUMN `owner` varchar(100) NULL DEFAULT AFTER `busNumber`;');
CALL add_element_unless_exists('column', 't_illegal_spaces', 'scheme', 'ALTER TABLE t_illegal_spaces ADD COLUMN `scheme` int(11) NULL DEFAULT 0 AFTER `owner`;');
CALL add_element_unless_exists('column', 't_illegal_spaces', 'ledIp', 'ALTER TABLE t_illegal_spaces ADD COLUMN `ledIp` varchar(50) NULL DEFAULT AFTER `scheme`;');
CALL add_element_unless_exists('column', 't_illegal_spaces', 'remark', 'ALTER TABLE t_illegal_spaces ADD COLUMN `remark` varchar(512) NULL DEFAULT AFTER `ledIp`;');
CALL add_element_unless_exists('column', 't_illegal_spaces', 'operator', 'ALTER TABLE t_illegal_spaces ADD COLUMN `operator` varchar(100) NULL DEFAULT AFTER `remark`;');
CALL add_element_unless_exists('column', 't_illegal_spaces', 'createTime', 'ALTER TABLE t_illegal_spaces ADD COLUMN `createTime` datetime NULL AFTER `operator`;');
CALL add_element_unless_exists('index', 't_illegal_spaces', 'PRIMARY', 'ALTER TABLE t_illegal_spaces ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_infobus_getinfobus_tmp 所有字段和索引
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'id', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `id` int(11) NOT NULL DEFAULT 0;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'BusNumber', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `BusNumber` varchar(40) NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'Addr', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `Addr` int(11) NULL DEFAULT 0 AFTER `BusNumber`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'state', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `state` int(11) NULL DEFAULT 0 AFTER `Addr`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'LeaveTime', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `LeaveTime` varchar(40) NULL AFTER `state`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'ComeTime', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `ComeTime` varchar(40) NULL AFTER `LeaveTime`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'CarPlateNum', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `CarPlateNum` varchar(50) NULL AFTER `ComeTime`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'ImgName', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `ImgName` varchar(50) NULL AFTER `CarPlateNum`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'AreaID', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `AreaID` int(11) NULL DEFAULT 0 AFTER `ImgName`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'PreLeaveTime', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `PreLeaveTime` varchar(40) NULL AFTER `AreaID`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'PreComeTime', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `PreComeTime` varchar(40) NULL AFTER `PreLeaveTime`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'PreCarplateNum', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `PreCarplateNum` varchar(50) NULL AFTER `PreComeTime`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'CarType', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `CarType` int(11) NULL DEFAULT 0 AFTER `PreCarplateNum`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'CarplateDigital', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `CarplateDigital` varchar(45) NULL AFTER `CarType`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'Mid', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `Mid` int(10) unsigned NOT NULL DEFAULT 0 AFTER `CarplateDigital`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'Trun', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `Trun` int(10) unsigned NOT NULL DEFAULT 0 AFTER `Mid`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'PosX', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `PosX` int(10) unsigned NOT NULL DEFAULT 0 AFTER `Trun`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'PosY', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `PosY` int(10) unsigned NOT NULL DEFAULT 0 AFTER `PosX`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'PSPlaceNum', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `PSPlaceNum` varchar(30) NOT NULL DEFAULT AFTER `PosY`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'PSPlaceName', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `PSPlaceName` varchar(30) NOT NULL DEFAULT AFTER `PSPlaceNum`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'IsDelete', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `IsDelete` int(1) NOT NULL DEFAULT 0 AFTER `PSPlaceName`;');
CALL add_element_unless_exists('column', 't_infobus_getinfobus_tmp', 'flag', 'ALTER TABLE t_infobus_getinfobus_tmp ADD COLUMN `flag` int(1) NOT NULL DEFAULT 0 AFTER `IsDelete`;');

-- 更新表 t_keypoint 所有字段和索引
CALL add_element_unless_exists('column', 't_keypoint', 'id', 'ALTER TABLE t_keypoint ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_keypoint', 'pointType', 'ALTER TABLE t_keypoint ADD COLUMN `pointType` int(3) NOT NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 't_keypoint', 'pointName', 'ALTER TABLE t_keypoint ADD COLUMN `pointName` varchar(50) NULL AFTER `pointType`;');
CALL add_element_unless_exists('column', 't_keypoint', 'locateX', 'ALTER TABLE t_keypoint ADD COLUMN `locateX` int(5) NOT NULL DEFAULT 0 AFTER `pointName`;');
CALL add_element_unless_exists('column', 't_keypoint', 'locateY', 'ALTER TABLE t_keypoint ADD COLUMN `locateY` int(5) NOT NULL DEFAULT 0 AFTER `locateX`;');
CALL add_element_unless_exists('column', 't_keypoint', 'lotid', 'ALTER TABLE t_keypoint ADD COLUMN `lotid` int(10) unsigned NOT NULL DEFAULT 0 AFTER `locateY`;');
CALL add_element_unless_exists('column', 't_keypoint', 'CliFlag', 'ALTER TABLE t_keypoint ADD COLUMN `CliFlag` int(8) NOT NULL DEFAULT 0 AFTER `lotid`;');
CALL add_element_unless_exists('column', 't_keypoint', 'CliDate', 'ALTER TABLE t_keypoint ADD COLUMN `CliDate` datetime NULL AFTER `CliFlag`;');
CALL add_element_unless_exists('column', 't_keypoint', 'IsDelete', 'ALTER TABLE t_keypoint ADD COLUMN `IsDelete` int(1) NOT NULL DEFAULT 0 AFTER `CliDate`;');
CALL add_element_unless_exists('column', 't_keypoint', 'floorpoint', 'ALTER TABLE t_keypoint ADD COLUMN `floorpoint` varchar(255) NULL DEFAULT AFTER `IsDelete`;');
CALL add_element_unless_exists('index', 't_keypoint', 'PRIMARY', 'ALTER TABLE t_keypoint ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_keypointlinks 所有字段和索引
CALL add_element_unless_exists('column', 't_keypointlinks', 'id', 'ALTER TABLE t_keypointlinks ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_keypointlinks', 'pointType1', 'ALTER TABLE t_keypointlinks ADD COLUMN `pointType1` int(1) NOT NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 't_keypointlinks', 'pointId1', 'ALTER TABLE t_keypointlinks ADD COLUMN `pointId1` int(11) NOT NULL AFTER `pointType1`;');
CALL add_element_unless_exists('column', 't_keypointlinks', 'pointType2', 'ALTER TABLE t_keypointlinks ADD COLUMN `pointType2` int(1) NOT NULL DEFAULT 0 AFTER `pointId1`;');
CALL add_element_unless_exists('column', 't_keypointlinks', 'pointId2', 'ALTER TABLE t_keypointlinks ADD COLUMN `pointId2` int(11) NOT NULL AFTER `pointType2`;');
CALL add_element_unless_exists('column', 't_keypointlinks', 'direction', 'ALTER TABLE t_keypointlinks ADD COLUMN `direction` int(4) NOT NULL DEFAULT 0 AFTER `pointId2`;');
CALL add_element_unless_exists('column', 't_keypointlinks', 'distance', 'ALTER TABLE t_keypointlinks ADD COLUMN `distance` int(11) NOT NULL DEFAULT 0 AFTER `direction`;');
CALL add_element_unless_exists('column', 't_keypointlinks', 'CliFlag', 'ALTER TABLE t_keypointlinks ADD COLUMN `CliFlag` int(8) NOT NULL DEFAULT 0 AFTER `distance`;');
CALL add_element_unless_exists('column', 't_keypointlinks', 'CliDate', 'ALTER TABLE t_keypointlinks ADD COLUMN `CliDate` datetime NULL AFTER `CliFlag`;');
CALL add_element_unless_exists('column', 't_keypointlinks', 'IsDelete', 'ALTER TABLE t_keypointlinks ADD COLUMN `IsDelete` int(1) NOT NULL DEFAULT 0 AFTER `CliDate`;');
CALL add_element_unless_exists('index', 't_keypointlinks', 'PRIMARY', 'ALTER TABLE t_keypointlinks ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_led_events 所有字段和索引
CALL add_element_unless_exists('column', 't_led_events', 'id', 'ALTER TABLE t_led_events ADD COLUMN `id` bigint(20) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_led_events', 'evtType', 'ALTER TABLE t_led_events ADD COLUMN `evtType` int(11) NOT NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 't_led_events', 'imgName', 'ALTER TABLE t_led_events ADD COLUMN `imgName` varchar(50) NOT NULL DEFAULT 0 AFTER `evtType`;');
CALL add_element_unless_exists('column', 't_led_events', 'dspIp', 'ALTER TABLE t_led_events ADD COLUMN `dspIp` varchar(32) NOT NULL DEFAULT 0 AFTER `imgName`;');
CALL add_element_unless_exists('column', 't_led_events', 'evtTime', 'ALTER TABLE t_led_events ADD COLUMN `evtTime` varchar(32) NOT NULL DEFAULT 0 AFTER `dspIp`;');
CALL add_element_unless_exists('column', 't_led_events', 'inAddr', 'ALTER TABLE t_led_events ADD COLUMN `inAddr` varchar(32) NOT NULL DEFAULT 0 AFTER `evtTime`;');
CALL add_element_unless_exists('column', 't_led_events', 'inTime', 'ALTER TABLE t_led_events ADD COLUMN `inTime` varchar(32) NOT NULL DEFAULT 0 AFTER `inAddr`;');
CALL add_element_unless_exists('column', 't_led_events', 'outAddr', 'ALTER TABLE t_led_events ADD COLUMN `outAddr` varchar(32) NOT NULL DEFAULT 0 AFTER `inTime`;');
CALL add_element_unless_exists('column', 't_led_events', 'outTime', 'ALTER TABLE t_led_events ADD COLUMN `outTime` varchar(32) NOT NULL DEFAULT 0 AFTER `outAddr`;');
CALL add_element_unless_exists('column', 't_led_events', 'money', 'ALTER TABLE t_led_events ADD COLUMN `money` int(11) NOT NULL DEFAULT 0 AFTER `outTime`;');
CALL add_element_unless_exists('column', 't_led_events', 'carNo', 'ALTER TABLE t_led_events ADD COLUMN `carNo` varchar(32) NOT NULL DEFAULT 0 AFTER `money`;');
CALL add_element_unless_exists('column', 't_led_events', 'carplateNum', 'ALTER TABLE t_led_events ADD COLUMN `carplateNum` varchar(45) NOT NULL DEFAULT 0 AFTER `carNo`;');
CALL add_element_unless_exists('column', 't_led_events', 'carplateType', 'ALTER TABLE t_led_events ADD COLUMN `carplateType` int(1) unsigned NOT NULL DEFAULT 0 AFTER `carplateNum`;');
CALL add_element_unless_exists('column', 't_led_events', 'carplateProty1', 'ALTER TABLE t_led_events ADD COLUMN `carplateProty1` int(3) unsigned NOT NULL DEFAULT 0 AFTER `carplateType`;');
CALL add_element_unless_exists('column', 't_led_events', 'carplateProty2', 'ALTER TABLE t_led_events ADD COLUMN `carplateProty2` int(3) unsigned NOT NULL DEFAULT 0 AFTER `carplateProty1`;');
CALL add_element_unless_exists('column', 't_led_events', 'enchargeFlag', 'ALTER TABLE t_led_events ADD COLUMN `enchargeFlag` int(1) unsigned NOT NULL DEFAULT 0 AFTER `carplateProty2`;');
CALL add_element_unless_exists('column', 't_led_events', 'serialType', 'ALTER TABLE t_led_events ADD COLUMN `serialType` int(1) unsigned NOT NULL DEFAULT 0 AFTER `enchargeFlag`;');
CALL add_element_unless_exists('column', 't_led_events', 'serialNo', 'ALTER TABLE t_led_events ADD COLUMN `serialNo` varchar(45) NOT NULL DEFAULT 0 AFTER `serialType`;');
CALL add_element_unless_exists('column', 't_led_events', 'inImgName', 'ALTER TABLE t_led_events ADD COLUMN `inImgName` varchar(50) NULL DEFAULT AFTER `serialNo`;');
CALL add_element_unless_exists('column', 't_led_events', 'CarColor', 'ALTER TABLE t_led_events ADD COLUMN `CarColor` varchar(45) NOT NULL DEFAULT AFTER `inImgName`;');
CALL add_element_unless_exists('column', 't_led_events', 'CarBrand', 'ALTER TABLE t_led_events ADD COLUMN `CarBrand` varchar(45) NOT NULL DEFAULT AFTER `CarColor`;');
CALL add_element_unless_exists('column', 't_led_events', 'RecogEnable', 'ALTER TABLE t_led_events ADD COLUMN `RecogEnable` int(8) NOT NULL DEFAULT 0 AFTER `CarBrand`;');
CALL add_element_unless_exists('column', 't_led_events', 'CarplateColor', 'ALTER TABLE t_led_events ADD COLUMN `CarplateColor` varchar(45) NOT NULL DEFAULT AFTER `RecogEnable`;');
CALL add_element_unless_exists('column', 't_led_events', 'CameraId', 'ALTER TABLE t_led_events ADD COLUMN `CameraId` int(11) NOT NULL DEFAULT 0 AFTER `CarplateColor`;');
CALL add_element_unless_exists('column', 't_led_events', 'remark', 'ALTER TABLE t_led_events ADD COLUMN `remark` varchar(50) NULL DEFAULT AFTER `CameraId`;');
CALL add_element_unless_exists('index', 't_led_events', 'PRIMARY', 'ALTER TABLE t_led_events ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_lock_control 所有字段和索引
CALL add_element_unless_exists('column', 't_lock_control', 'id', 'ALTER TABLE t_lock_control ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_lock_control', 'busid', 'ALTER TABLE t_lock_control ADD COLUMN `busid` varchar(32) NOT NULL AFTER `id`;');
CALL add_element_unless_exists('column', 't_lock_control', 'action', 'ALTER TABLE t_lock_control ADD COLUMN `action` int(11) NOT NULL AFTER `busid`;');
CALL add_element_unless_exists('column', 't_lock_control', 'updateTime', 'ALTER TABLE t_lock_control ADD COLUMN `updateTime` datetime NOT NULL AFTER `action`;');
CALL add_element_unless_exists('index', 't_lock_control', 'PRIMARY', 'ALTER TABLE t_lock_control ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_lotcarforfee 所有字段和索引
CALL add_element_unless_exists('column', 't_lotcarforfee', 'carNo', 'ALTER TABLE t_lotcarforfee ADD COLUMN `carNo` varchar(32) NOT NULL;');
CALL add_element_unless_exists('column', 't_lotcarforfee', 'parkTime', 'ALTER TABLE t_lotcarforfee ADD COLUMN `parkTime` datetime NOT NULL AFTER `carNo`;');
CALL add_element_unless_exists('column', 't_lotcarforfee', 'lastUpdate', 'ALTER TABLE t_lotcarforfee ADD COLUMN `lastUpdate` datetime NOT NULL AFTER `parkTime`;');
CALL add_element_unless_exists('column', 't_lotcarforfee', 'imgname', 'ALTER TABLE t_lotcarforfee ADD COLUMN `imgname` varchar(100) NOT NULL AFTER `lastUpdate`;');
CALL add_element_unless_exists('index', 't_lotcarforfee', 'PRIMARY', 'ALTER TABLE t_lotcarforfee ADD UNIQUE INDEX `PRIMARY` (`carNo`) USING BTREE;');
CALL add_element_unless_exists('index', 't_lotcarforfee', 'idx_lotCarForFee_Update', 'ALTER TABLE t_lotcarforfee ADD INDEX INDEX `idx_lotCarForFee_Update` (`lastUpdate`) USING BTREE;');

-- 更新表 t_lotcarforfind 所有字段和索引
CALL add_element_unless_exists('column', 't_lotcarforfind', 'carNo', 'ALTER TABLE t_lotcarforfind ADD COLUMN `carNo` varchar(32) NOT NULL;');
CALL add_element_unless_exists('column', 't_lotcarforfind', 'carAddr', 'ALTER TABLE t_lotcarforfind ADD COLUMN `carAddr` int(11) NOT NULL AFTER `carNo`;');
CALL add_element_unless_exists('column', 't_lotcarforfind', 'parkTime', 'ALTER TABLE t_lotcarforfind ADD COLUMN `parkTime` datetime NOT NULL AFTER `carAddr`;');
CALL add_element_unless_exists('column', 't_lotcarforfind', 'lastUpdate', 'ALTER TABLE t_lotcarforfind ADD COLUMN `lastUpdate` datetime NOT NULL AFTER `parkTime`;');
CALL add_element_unless_exists('column', 't_lotcarforfind', 'carNumber', 'ALTER TABLE t_lotcarforfind ADD COLUMN `carNumber` varchar(8) NULL DEFAULT AFTER `lastUpdate`;');
CALL add_element_unless_exists('column', 't_lotcarforfind', 'imgName', 'ALTER TABLE t_lotcarforfind ADD COLUMN `imgName` varchar(50) NULL DEFAULT AFTER `carNumber`;');
CALL add_element_unless_exists('column', 't_lotcarforfind', 'carType', 'ALTER TABLE t_lotcarforfind ADD COLUMN `carType` int(2) NULL DEFAULT 0 AFTER `imgName`;');
CALL add_element_unless_exists('column', 't_lotcarforfind', 'CarPlateASI', 'ALTER TABLE t_lotcarforfind ADD COLUMN `CarPlateASI` varchar(30) NULL AFTER `carType`;');
CALL add_element_unless_exists('index', 't_lotcarforfind', 'idx_lotcarforfind_carAddr', 'ALTER TABLE t_lotcarforfind ADD INDEX INDEX `idx_lotcarforfind_carAddr` (`carAddr`) USING BTREE;');
CALL add_element_unless_exists('index', 't_lotcarforfind', 'idx_lotcarforfind_carNoCarAddr', 'ALTER TABLE t_lotcarforfind ADD INDEX INDEX `idx_lotcarforfind_carNoCarAddr` (`carNo`) USING BTREE;');
CALL add_element_unless_exists('index', 't_lotcarforfind', 'idx_lotcarforfind_carNoCarAddr', 'ALTER TABLE t_lotcarforfind ADD INDEX INDEX `idx_lotcarforfind_carNoCarAddr` (`carAddr`) USING BTREE;');

-- 更新表 t_lotcarforfind_area 所有字段和索引
CALL add_element_unless_exists('column', 't_lotcarforfind_area', 'id', 'ALTER TABLE t_lotcarforfind_area ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_lotcarforfind_area', 'carNo', 'ALTER TABLE t_lotcarforfind_area ADD COLUMN `carNo` varchar(32) NOT NULL AFTER `id`;');
CALL add_element_unless_exists('column', 't_lotcarforfind_area', 'carAddr', 'ALTER TABLE t_lotcarforfind_area ADD COLUMN `carAddr` int(11) NOT NULL AFTER `carNo`;');
CALL add_element_unless_exists('column', 't_lotcarforfind_area', 'parkTime', 'ALTER TABLE t_lotcarforfind_area ADD COLUMN `parkTime` datetime NOT NULL AFTER `carAddr`;');
CALL add_element_unless_exists('column', 't_lotcarforfind_area', 'lastUpdate', 'ALTER TABLE t_lotcarforfind_area ADD COLUMN `lastUpdate` datetime NOT NULL AFTER `parkTime`;');
CALL add_element_unless_exists('column', 't_lotcarforfind_area', 'carNumber', 'ALTER TABLE t_lotcarforfind_area ADD COLUMN `carNumber` varchar(8) NULL DEFAULT AFTER `lastUpdate`;');
CALL add_element_unless_exists('column', 't_lotcarforfind_area', 'imgname', 'ALTER TABLE t_lotcarforfind_area ADD COLUMN `imgname` varchar(255) NULL AFTER `carNumber`;');
CALL add_element_unless_exists('column', 't_lotcarforfind_area', 'CarPlateASI', 'ALTER TABLE t_lotcarforfind_area ADD COLUMN `CarPlateASI` varchar(255) NULL AFTER `imgname`;');
CALL add_element_unless_exists('index', 't_lotcarforfind_area', 'PRIMARY', 'ALTER TABLE t_lotcarforfind_area ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');
CALL add_element_unless_exists('index', 't_lotcarforfind_area', 'IX_t_lotcarforfind_area_carAddr', 'ALTER TABLE t_lotcarforfind_area ADD INDEX INDEX `IX_t_lotcarforfind_area_carAddr` (`carAddr`) USING BTREE;');
CALL add_element_unless_exists('index', 't_lotcarforfind_area', 'UK_t_lotcarforfind_area_imgname', 'ALTER TABLE t_lotcarforfind_area ADD INDEX INDEX `UK_t_lotcarforfind_area_imgname` (`imgname`) USING BTREE;');
CALL add_element_unless_exists('index', 't_lotcarforfind_area', 'UK_t_lotcarforfind_carNoCarAddr', 'ALTER TABLE t_lotcarforfind_area ADD INDEX INDEX `UK_t_lotcarforfind_carNoCarAddr` (`carAddr`) USING BTREE;');
CALL add_element_unless_exists('index', 't_lotcarforfind_area', 'UK_t_lotcarforfind_carNoCarAddr', 'ALTER TABLE t_lotcarforfind_area ADD INDEX INDEX `UK_t_lotcarforfind_carNoCarAddr` (`carNo`) USING BTREE;');

-- 更新表 t_parkinglot 所有字段和索引
CALL add_element_unless_exists('column', 't_parkinglot', 'lotId', 'ALTER TABLE t_parkinglot ADD COLUMN `lotId` int(3) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_parkinglot', 'lotName', 'ALTER TABLE t_parkinglot ADD COLUMN `lotName` varchar(100) NOT NULL AFTER `lotId`;');
CALL add_element_unless_exists('column', 't_parkinglot', 'bgImgFile', 'ALTER TABLE t_parkinglot ADD COLUMN `bgImgFile` varchar(200) NULL AFTER `lotName`;');
CALL add_element_unless_exists('column', 't_parkinglot', 'areaCount', 'ALTER TABLE t_parkinglot ADD COLUMN `areaCount` int(5) NOT NULL DEFAULT 1 AFTER `bgImgFile`;');
CALL add_element_unless_exists('column', 't_parkinglot', 'tollCount', 'ALTER TABLE t_parkinglot ADD COLUMN `tollCount` int(11) NOT NULL DEFAULT 0 AFTER `areaCount`;');
CALL add_element_unless_exists('column', 't_parkinglot', 'placeCount', 'ALTER TABLE t_parkinglot ADD COLUMN `placeCount` int(5) NOT NULL DEFAULT 0 AFTER `tollCount`;');
CALL add_element_unless_exists('column', 't_parkinglot', 'zoomRate', 'ALTER TABLE t_parkinglot ADD COLUMN `zoomRate` tinyint(2) NOT NULL DEFAULT 1 AFTER `placeCount`;');
CALL add_element_unless_exists('column', 't_parkinglot', 'CliDate', 'ALTER TABLE t_parkinglot ADD COLUMN `CliDate` datetime NULL AFTER `zoomRate`;');
CALL add_element_unless_exists('column', 't_parkinglot', 'CliFlag', 'ALTER TABLE t_parkinglot ADD COLUMN `CliFlag` int(8) NOT NULL DEFAULT 0 AFTER `CliDate`;');
CALL add_element_unless_exists('column', 't_parkinglot', 'IsDelete', 'ALTER TABLE t_parkinglot ADD COLUMN `IsDelete` int(1) NOT NULL DEFAULT 0 AFTER `CliFlag`;');
CALL add_element_unless_exists('column', 't_parkinglot', 'address', 'ALTER TABLE t_parkinglot ADD COLUMN `address` varchar(200) NULL DEFAULT AFTER `IsDelete`;');
CALL add_element_unless_exists('column', 't_parkinglot', 'totalSpace', 'ALTER TABLE t_parkinglot ADD COLUMN `totalSpace` varchar(200) NULL DEFAULT AFTER `address`;');
CALL add_element_unless_exists('column', 't_parkinglot', 'tel', 'ALTER TABLE t_parkinglot ADD COLUMN `tel` varchar(200) NULL DEFAULT AFTER `totalSpace`;');
CALL add_element_unless_exists('column', 't_parkinglot', 'secret', 'ALTER TABLE t_parkinglot ADD COLUMN `secret` varchar(200) NULL DEFAULT AFTER `tel`;');
CALL add_element_unless_exists('index', 't_parkinglot', 'PRIMARY', 'ALTER TABLE t_parkinglot ADD UNIQUE INDEX `PRIMARY` (`lotId`) USING BTREE;');

-- 更新表 t_power_events 所有字段和索引
CALL add_element_unless_exists('column', 't_power_events', 'id', 'ALTER TABLE t_power_events ADD COLUMN `id` bigint(20) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_power_events', 'evtType', 'ALTER TABLE t_power_events ADD COLUMN `evtType` int(11) NOT NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 't_power_events', 'imgName', 'ALTER TABLE t_power_events ADD COLUMN `imgName` varchar(50) NOT NULL DEFAULT 0 AFTER `evtType`;');
CALL add_element_unless_exists('column', 't_power_events', 'dspIp', 'ALTER TABLE t_power_events ADD COLUMN `dspIp` varchar(32) NOT NULL DEFAULT 0 AFTER `imgName`;');
CALL add_element_unless_exists('column', 't_power_events', 'evtTime', 'ALTER TABLE t_power_events ADD COLUMN `evtTime` varchar(32) NOT NULL DEFAULT 0 AFTER `dspIp`;');
CALL add_element_unless_exists('column', 't_power_events', 'inAddr', 'ALTER TABLE t_power_events ADD COLUMN `inAddr` varchar(32) NOT NULL DEFAULT 0 AFTER `evtTime`;');
CALL add_element_unless_exists('column', 't_power_events', 'inTime', 'ALTER TABLE t_power_events ADD COLUMN `inTime` varchar(32) NOT NULL DEFAULT 0 AFTER `inAddr`;');
CALL add_element_unless_exists('column', 't_power_events', 'outAddr', 'ALTER TABLE t_power_events ADD COLUMN `outAddr` varchar(32) NOT NULL DEFAULT 0 AFTER `inTime`;');
CALL add_element_unless_exists('column', 't_power_events', 'outTime', 'ALTER TABLE t_power_events ADD COLUMN `outTime` varchar(32) NOT NULL DEFAULT 0 AFTER `outAddr`;');
CALL add_element_unless_exists('column', 't_power_events', 'money', 'ALTER TABLE t_power_events ADD COLUMN `money` int(11) NOT NULL DEFAULT 0 AFTER `outTime`;');
CALL add_element_unless_exists('column', 't_power_events', 'carNo', 'ALTER TABLE t_power_events ADD COLUMN `carNo` varchar(32) NOT NULL DEFAULT 0 AFTER `money`;');
CALL add_element_unless_exists('column', 't_power_events', 'carplateNum', 'ALTER TABLE t_power_events ADD COLUMN `carplateNum` varchar(45) NOT NULL DEFAULT 0 AFTER `carNo`;');
CALL add_element_unless_exists('column', 't_power_events', 'carplateType', 'ALTER TABLE t_power_events ADD COLUMN `carplateType` int(1) unsigned NOT NULL DEFAULT 0 AFTER `carplateNum`;');
CALL add_element_unless_exists('column', 't_power_events', 'carplateProty1', 'ALTER TABLE t_power_events ADD COLUMN `carplateProty1` int(3) unsigned NOT NULL DEFAULT 0 AFTER `carplateType`;');
CALL add_element_unless_exists('column', 't_power_events', 'carplateProty2', 'ALTER TABLE t_power_events ADD COLUMN `carplateProty2` int(3) unsigned NOT NULL DEFAULT 0 AFTER `carplateProty1`;');
CALL add_element_unless_exists('column', 't_power_events', 'enchargeFlag', 'ALTER TABLE t_power_events ADD COLUMN `enchargeFlag` int(1) unsigned NOT NULL DEFAULT 0 AFTER `carplateProty2`;');
CALL add_element_unless_exists('column', 't_power_events', 'serialType', 'ALTER TABLE t_power_events ADD COLUMN `serialType` int(1) unsigned NOT NULL DEFAULT 0 AFTER `enchargeFlag`;');
CALL add_element_unless_exists('column', 't_power_events', 'serialNo', 'ALTER TABLE t_power_events ADD COLUMN `serialNo` varchar(45) NOT NULL DEFAULT 0 AFTER `serialType`;');
CALL add_element_unless_exists('column', 't_power_events', 'inImgName', 'ALTER TABLE t_power_events ADD COLUMN `inImgName` varchar(50) NULL DEFAULT AFTER `serialNo`;');
CALL add_element_unless_exists('column', 't_power_events', 'CarColor', 'ALTER TABLE t_power_events ADD COLUMN `CarColor` varchar(45) NOT NULL DEFAULT AFTER `inImgName`;');
CALL add_element_unless_exists('column', 't_power_events', 'CarBrand', 'ALTER TABLE t_power_events ADD COLUMN `CarBrand` varchar(45) NOT NULL DEFAULT AFTER `CarColor`;');
CALL add_element_unless_exists('column', 't_power_events', 'RecogEnable', 'ALTER TABLE t_power_events ADD COLUMN `RecogEnable` int(8) NOT NULL DEFAULT 0 AFTER `CarBrand`;');
CALL add_element_unless_exists('column', 't_power_events', 'CarplateColor', 'ALTER TABLE t_power_events ADD COLUMN `CarplateColor` varchar(45) NOT NULL DEFAULT AFTER `RecogEnable`;');
CALL add_element_unless_exists('column', 't_power_events', 'CameraId', 'ALTER TABLE t_power_events ADD COLUMN `CameraId` int(11) NOT NULL DEFAULT 0 AFTER `CarplateColor`;');
CALL add_element_unless_exists('column', 't_power_events', 'remark', 'ALTER TABLE t_power_events ADD COLUMN `remark` varchar(50) NULL DEFAULT AFTER `CameraId`;');
CALL add_element_unless_exists('index', 't_power_events', 'PRIMARY', 'ALTER TABLE t_power_events ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');
CALL add_element_unless_exists('index', 't_power_events', 'idx_events_dspIp', 'ALTER TABLE t_power_events ADD INDEX INDEX `idx_events_dspIp` (`dspIp`) USING BTREE;');
CALL add_element_unless_exists('index', 't_power_events', 'idx_events_evtType', 'ALTER TABLE t_power_events ADD INDEX INDEX `idx_events_evtType` (`evtType`) USING BTREE;');

-- 更新表 t_service_config 所有字段和索引
CALL add_element_unless_exists('column', 't_service_config', 'id', 'ALTER TABLE t_service_config ADD COLUMN `id` int(11) NOT NULL;');
CALL add_element_unless_exists('column', 't_service_config', 'is_separate', 'ALTER TABLE t_service_config ADD COLUMN `is_separate` tinyint(1) NULL DEFAULT 0 AFTER `id`;');
CALL add_element_unless_exists('column', 't_service_config', 'is_sync_parking_data', 'ALTER TABLE t_service_config ADD COLUMN `is_sync_parking_data` tinyint(1) NULL DEFAULT 0 AFTER `is_separate`;');
CALL add_element_unless_exists('column', 't_service_config', 'is_sync_lock_instruction', 'ALTER TABLE t_service_config ADD COLUMN `is_sync_lock_instruction` tinyint(1) NULL DEFAULT 0 AFTER `is_sync_parking_data`;');
CALL add_element_unless_exists('column', 't_service_config', 'create_time', 'ALTER TABLE t_service_config ADD COLUMN `create_time` datetime NULL AFTER `is_sync_lock_instruction`;');
CALL add_element_unless_exists('column', 't_service_config', 'update_time', 'ALTER TABLE t_service_config ADD COLUMN `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP AFTER `create_time`;');
CALL add_element_unless_exists('index', 't_service_config', 'PRIMARY', 'ALTER TABLE t_service_config ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 t_toll_ip 所有字段和索引
CALL add_element_unless_exists('column', 't_toll_ip', 'id', 'ALTER TABLE t_toll_ip ADD COLUMN `id` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 't_toll_ip', 'ip', 'ALTER TABLE t_toll_ip ADD COLUMN `ip` varchar(20) NOT NULL DEFAULT AFTER `id`;');
CALL add_element_unless_exists('column', 't_toll_ip', 'createTime', 'ALTER TABLE t_toll_ip ADD COLUMN `createTime` datetime NULL AFTER `ip`;');
CALL add_element_unless_exists('column', 't_toll_ip', 'creator', 'ALTER TABLE t_toll_ip ADD COLUMN `creator` varchar(256) NULL DEFAULT AFTER `createTime`;');
CALL add_element_unless_exists('index', 't_toll_ip', 'PRIMARY', 'ALTER TABLE t_toll_ip ADD UNIQUE INDEX `PRIMARY` (`id`) USING BTREE;');

-- 更新表 temp_log_parkcount 所有字段和索引
CALL add_element_unless_exists('column', 'temp_log_parkcount', 'ID', 'ALTER TABLE temp_log_parkcount ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'temp_log_parkcount', 'AreaId', 'ALTER TABLE temp_log_parkcount ADD COLUMN `AreaId` int(11) NOT NULL DEFAULT 0 AFTER `ID`;');
CALL add_element_unless_exists('column', 'temp_log_parkcount', 'AreaName', 'ALTER TABLE temp_log_parkcount ADD COLUMN `AreaName` varchar(50) NOT NULL DEFAULT AFTER `AreaId`;');
CALL add_element_unless_exists('column', 'temp_log_parkcount', 'ParkDate', 'ALTER TABLE temp_log_parkcount ADD COLUMN `ParkDate` datetime NULL AFTER `AreaName`;');
CALL add_element_unless_exists('column', 'temp_log_parkcount', 'ParkHour', 'ALTER TABLE temp_log_parkcount ADD COLUMN `ParkHour` int(11) NOT NULL DEFAULT 0 AFTER `ParkDate`;');
CALL add_element_unless_exists('column', 'temp_log_parkcount', 'ParkCount', 'ALTER TABLE temp_log_parkcount ADD COLUMN `ParkCount` int(11) NOT NULL DEFAULT 0 AFTER `ParkHour`;');
CALL add_element_unless_exists('column', 'temp_log_parkcount', 'FlowIn', 'ALTER TABLE temp_log_parkcount ADD COLUMN `FlowIn` int(11) NOT NULL DEFAULT 0 AFTER `ParkCount`;');
CALL add_element_unless_exists('column', 'temp_log_parkcount', 'FlowOut', 'ALTER TABLE temp_log_parkcount ADD COLUMN `FlowOut` int(11) NOT NULL DEFAULT 0 AFTER `FlowIn`;');
CALL add_element_unless_exists('column', 'temp_log_parkcount', 'CliDate', 'ALTER TABLE temp_log_parkcount ADD COLUMN `CliDate` datetime NULL AFTER `FlowOut`;');
CALL add_element_unless_exists('column', 'temp_log_parkcount', 'CliFlag', 'ALTER TABLE temp_log_parkcount ADD COLUMN `CliFlag` int(8) NOT NULL DEFAULT 0 AFTER `CliDate`;');
CALL add_element_unless_exists('column', 'temp_log_parkcount', 'IsDelete', 'ALTER TABLE temp_log_parkcount ADD COLUMN `IsDelete` int(1) NOT NULL DEFAULT 0 AFTER `CliFlag`;');
CALL add_element_unless_exists('index', 'temp_log_parkcount', 'PRIMARY', 'ALTER TABLE temp_log_parkcount ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');

-- 更新表 user 所有字段和索引
CALL add_element_unless_exists('column', 'user', 'ID', 'ALTER TABLE user ADD COLUMN `ID` int(11) NOT NULL  auto_increment;');
CALL add_element_unless_exists('column', 'user', 'LoginName', 'ALTER TABLE user ADD COLUMN `LoginName` varchar(45) NOT NULL AFTER `ID`;');
CALL add_element_unless_exists('column', 'user', 'Pwd', 'ALTER TABLE user ADD COLUMN `Pwd` varchar(45) NOT NULL AFTER `LoginName`;');
CALL add_element_unless_exists('column', 'user', 'URight', 'ALTER TABLE user ADD COLUMN `URight` int(10) unsigned NOT NULL DEFAULT 0 AFTER `Pwd`;');
CALL add_element_unless_exists('column', 'user', 'lastlogintime', 'ALTER TABLE user ADD COLUMN `lastlogintime` varchar(40) NULL AFTER `URight`;');
CALL add_element_unless_exists('column', 'user', 'UserType', 'ALTER TABLE user ADD COLUMN `UserType` int(11) NULL DEFAULT 0 AFTER `lastlogintime`;');
CALL add_element_unless_exists('index', 'user', 'PRIMARY', 'ALTER TABLE user ADD UNIQUE INDEX `PRIMARY` (`ID`) USING BTREE;');


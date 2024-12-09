import re

sql_content = """
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
"""

create_table_pattern = re.compile(
        r'--.*?\n\s*CREATE TABLE.*?\(.*?\).*?;',
        re.S | re.I
    )

# 查找所有匹配的 CREATE TABLE 语句
create_table_statements = create_table_pattern.findall(sql_content)
for i in range(len(create_table_statements)):
    print(i + 1, create_table_statements[i])

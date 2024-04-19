@echo off
chcp 65001

title 随便玩
rem mode con cols=30 lines=20 & 
color 2E
:Begin
cls
rem 显示所有已连接设备
rem adb devices

rem 清除所有已知连接
adb disconnect
echo.
echo   --------------------来，这里当个首页吧！---------------------
echo.
echo   --------------本批处理由寻车引导项目组友情赞助---------------
echo.
echo 【1】连接找车机
echo.
echo 【2】退出
echo.
set "ch="
set /p ch=请输入选择数字后回车确认！
echo.
echo %ch%|findstr /i "^[1-2]$">nul||echo 请输入有效数值 && timeout -t 2 -nobreak>nul && goto Begin
if /i "%ch%"=="1" goto links
if /i "%ch%"=="2" goto exit

:links
cls
echo.
echo 小提示：如果是从其它页面跳回来的，只要不选连接其它找车机，都会默认之前的IP！
echo.
set /p machine_ip=请输入找车机IP后回车确认！注意前后不要有空格！：
if /i "%machine_ip%"=="" goto links
adb connect %machine_ip%

timeout -t 3 -nobreak>nul

:link
cls
echo.
echo   --------------------来，下一步吧！---------------------
echo.
echo   ------（提示：下载日志需要先关闭找车机远程窗口）-------
echo.
echo 【1】开启远程
echo.
echo 【2】连接其它找车机
echo.
echo 【3】下载日志——FCCC收费一体机
echo.
echo 【4】下载日志——fsfp立式人脸找车机
echo.
echo 【5】下载日志——fsfa壁挂式人脸找车机
echo.
echo 【6】下载日志——LCD显示屏（一体屏，其它有没有区别没用过）
echo.
echo 【7】重启安卓设备
echo.
echo 【8】退出
echo.
set "ch1="
set /p ch1=请输入选择数字后回车确认！
echo.
echo %ch1%|findstr /i "^[1-8]$">nul||echo 请输入有效数值 && timeout -t 2 -nobreak>nul && goto link
echo %ch1%|findstr /i "^[2-8]$">nul||goto remote
if /i "%ch1%"=="3" set cname=fccc&& goto download
if /i "%ch1%"=="4" set cname=fsfp&& goto download
if /i "%ch1%"=="5" set cname=frsa&& goto download
if /i "%ch1%"=="6" set cname=lcdgs&& goto download
if /i "%ch1%"=="7" goto rst
adb disconnect
if /i "%ch1%"=="2" goto links
if /i "%ch1%"=="8" goto exit


:remote

start cmd /K "@echo off &&echo 使用找车机窗口时，别关！！！&&scrcpy.exe 2>nul && exit"

goto link


:rst

adb reboot

goto link


:download

REM 提取年、月、日，格式跟本机不一样，用的好像是找车机的
set "yy=%date:~3,4%"
set "mm=%date:~8,2%"
set "dd=%date:~11,2%"
set "ym=%yy%%mm%"
set "td=%ym%%dd%"

echo   --------------------来，下个找车机日志吧！---------------------
echo.
echo 【1】下载当天日志
echo.
echo 【2】下载其它时间日志
echo.
echo 【3】返回上一级
echo.
echo 【4】退出
echo.
set "ch3="
set /p ch3=请输入选择的数字，并回车确认！

echo %ch3%|findstr /i "^[1-4]$">nul||echo 请输入有效数值 && timeout -t 1 -nobreak>nul && goto download
if /i "%ch3%"=="1" call :dl && goto download
if /i "%ch3%"=="2" call :dlot && goto download
if /i "%ch3%"=="3" goto link
if /i "%ch3%"=="4" goto exit



rem echo %ch2%|findstr /i ("^[012][0-9]$|^3[01]$")>nul||echo 请输入有效数值 && timeout -t 1 -nobreak>nul && goto download

:dl
rem 下载当天
adb pull /sdcard/Android/data/com.keytop.%cname%/files/log/%td%.log %~dp0

echo 没报错就是成功哈 && timeout -t 2 -nobreak>nul

goto:eof

:dlot

rem 下载其它时间
set "ch2="
set /p ch2=请输入日期后两位后回车确认！（例：2023年4月5日，输入0405）

rem echo %ch2%|findstr /r "^\d{4}$">nul||echo 请输入有效数值 && timeout -t 1 -nobreak>nul && goto download

adb pull /sdcard/Android/data/com.keytop.%cname%/files/log/%yy%%ch2%.zip %~dp0

goto:eof


exit

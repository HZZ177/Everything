import os
import time
import ctypes
import psutil
import win32gui
import win32process
from ctypes import wintypes

# 加载必要的 Windows API 函数
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
advapi32 = ctypes.WinDLL('advapi32', use_last_error=True)

# 定义常量
SECURITY_WORLD_SID_AUTHORITY = (0, 0, 0, 0, 0, 1)  # SID 标识符
SECURITY_WORLD_RID = 0  # 世界 SID 的 RID
ACL_REVISION = 2  # ACL 版本
SE_KERNEL_OBJECT = 6  # 内核对象类型
DACL_SECURITY_INFORMATION = 0x00000004  # DACL 安全信息标志
MUTEX_ALL_ACCESS = 0x1F0001  # 互斥体的完全访问权限

# 定义函数参数和返回类型
kernel32.CreateMutexW.argtypes = [wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR]
kernel32.CreateMutexW.restype = wintypes.HANDLE

advapi32.AllocateAndInitializeSid.argtypes = [
    ctypes.POINTER(ctypes.c_byte),  # SID_IDENTIFIER_AUTHORITY
    ctypes.c_byte,  # SubAuthorityCount
    ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong,
    ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong,
    ctypes.POINTER(ctypes.c_void_p)  # PSID
]
advapi32.AllocateAndInitializeSid.restype = wintypes.BOOL

advapi32.InitializeAcl.argtypes = [wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD]
advapi32.InitializeAcl.restype = wintypes.BOOL

advapi32.AddAccessDeniedAce.argtypes = [wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID]
advapi32.AddAccessDeniedAce.restype = wintypes.BOOL

advapi32.SetSecurityInfo.argtypes = [
    wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID,
    wintypes.LPVOID, wintypes.LPVOID
]
advapi32.SetSecurityInfo.restype = wintypes.DWORD

def Create_wechat_Mutex():
    # 创建一个互斥体，微信使用该互斥体确保单实例运行
    h_mutex = kernel32.CreateMutexW(None, False, "_WeChat_App_Instance_Identity_Mutex_Name")
    if not h_mutex:
        raise ctypes.WinError(ctypes.get_last_error())

    # 定义 SID_IDENTIFIER_AUTHORITY 结构
    sid_auth_world = (ctypes.c_byte * 6)(*SECURITY_WORLD_SID_AUTHORITY)

    # 为 Everyone 组分配并初始化 SID
    p_everyone_sid = ctypes.c_void_p()
    if not advapi32.AllocateAndInitializeSid(
        ctypes.cast(ctypes.byref(sid_auth_world), ctypes.POINTER(ctypes.c_byte)),  # 正确传递 SID_IDENTIFIER_AUTHORITY
        1,  # SubAuthorityCount
        SECURITY_WORLD_RID, 0, 0, 0, 0, 0, 0, 0,  # SubAuthorities
        ctypes.byref(p_everyone_sid)  # PSID
    ):
        raise ctypes.WinError(ctypes.get_last_error())

    # 初始化 ACL
    sz_buffer = (ctypes.c_byte * 4096)()
    p_acl = ctypes.cast(sz_buffer, ctypes.POINTER(ctypes.c_byte))
    if not advapi32.InitializeAcl(p_acl, ctypes.sizeof(sz_buffer), ACL_REVISION):
        raise ctypes.WinError(ctypes.get_last_error())

    # 向 ACL 添加拒绝访问的 ACE（访问控制条目）
    if not advapi32.AddAccessDeniedAce(p_acl, ACL_REVISION, MUTEX_ALL_ACCESS, p_everyone_sid):
        raise ctypes.WinError(ctypes.get_last_error())

    # 设置互斥体的安全信息，修改其 ACL
    result = advapi32.SetSecurityInfo(
        h_mutex, SE_KERNEL_OBJECT, DACL_SECURITY_INFORMATION, None, None, p_acl, None
    )
    if result != 0:
        raise ctypes.WinError(result)

# 获取进程pid
def get_pid(process_name):
    pids = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            pids.append(proc.info['pid'])
    return pids

# 根据pid获取进程路径
def get_process_path(pid):
    try:
        process = psutil.Process(pid)
        return process.exe()
    except psutil.NoSuchProcess:
        return None

# 根据pid获取窗口句柄
def get_hwnd_from_pid(pids):
    hwnds = []
    def callback(hwnd, extra):
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        window_title = win32gui.GetWindowText(hwnd)  # 获取窗口标题
        if pid in pids and win32gui.IsWindowVisible(hwnd) and window_title != "":
            hwnds.append(hwnd)
        return True
    win32gui.EnumWindows(callback, None)
    return hwnds

# 获取屏幕尺寸
def get_screen_size():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)  # SM_CXSCREEN
    screen_height = user32.GetSystemMetrics(1)  # SM_CYSCREEN
    return screen_width, screen_height

# 排列窗口
def arrange_windows(windows):
    num_windows = len(windows)
    if num_windows == 0:
        return

    # 获取屏幕尺寸
    screen_width, screen_height = get_screen_size()

    # 获取第一个窗口的大小（假设所有窗口大小相同）
    left, top, right, bottom = win32gui.GetWindowRect(windows[0])
    window_width = right - left
    window_height = bottom - top

    # 窗口间距
    spacing = 10

    # 计算行数和每行的窗口数量
    rows = 2  # 默认 2 行
    if num_windows <= 2:
        rows = 1
    elif num_windows >= 3:
        rows = 2

    # 计算每行的窗口数量
    windows_per_row = []
    if rows == 1:
        windows_per_row = [num_windows]
    else:
        # 多行
        windows_per_row = [num_windows // 2 + num_windows % 2, num_windows // 2]

    # 计算每行的起始位置
    start_y = (screen_height - rows * (window_height + spacing)) // 2

    # 移动窗口
    index = 0
    for row in range(rows):
        current_cols = windows_per_row[row]  # 当前行的窗口数量

        # 计算当前行的总宽度
        total_width = current_cols * window_width + (current_cols - 1) * spacing
        start_x = (screen_width - total_width) // 2

        # 排列当前行的窗口
        for col in range(current_cols):
            if index >= num_windows:
                break
            x = start_x + col * (window_width + spacing)
            y = start_y + row * (window_height + spacing)
            win32gui.MoveWindow(windows[index], x, y, window_width, window_height, True)
            index += 1

try:
    Create_wechat_Mutex()
except:
    pass

### 获取WeChat.exe进程路径
last_pids = get_pid("WeChat.exe")
if len(last_pids) > 0:
    path = get_process_path(last_pids[0])

### 没有打开微信手填一下,或者打开一个微信
# path = "C:\Program Files (x86)\Tencent\WeChat\WeChat.exe"

open_wx_num = 5
for i in range(open_wx_num):
    os.startfile(path)

### 获取新打开的pids
now_pids = get_pid("WeChat.exe")
pids = list(set(now_pids) - set(last_pids))

### 获取窗口句柄
wechat_windows = get_hwnd_from_pid(pids)

# 等待所有窗口打开
print("等待窗口加载...")
time.sleep(1)  # 增加等待时间

# 排列窗口
arrange_windows(wechat_windows)
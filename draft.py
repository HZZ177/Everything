import sys
import os
# 获取Python的安装目录
import os
import sys
python_path = sys.executable # 这个是python.exe的路径
python_path = os.path.dirname(python_path)
print("Python安装路径:", python_path)
# 检查Python是否在环境变量中
print(os.environ)
path_env = os.environ.get('PATH')
if python_path in path_env:
    print("Python在环境变量中")
else:
    print("Python不在环境变量中")
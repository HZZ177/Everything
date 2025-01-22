import time
import threading
import paramiko
from dash import Dash, dcc, html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output


# 定义函数，获取远程服务器性能指标
def get_server_metrics(host, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port, username=username, password=password)

        commands = {
            "CPU使用率": "top -bn1 | grep 'Cpu(s)' | awk '{print $2+$4}'",
            "内存使用情况": "free -m | awk 'NR==2{printf \"%.2f\", $3*100/$2 }'",
            "磁盘使用情况": "df -h --total | grep 'total' | awk '{print $5}'"
        }

        metrics = {}
        for metric_name, command in commands.items():
            stdin, stdout, stderr = client.exec_command(command)
            result = stdout.read().decode().strip()
            metrics[metric_name] = float(result.replace('%', ''))  # 去掉百分号并转换为浮点数

        return metrics
    except Exception as e:
        print(f"获取性能指标时发生错误: {e}")
        return {}
    finally:
        client.close()

# 初始化全局变量用于存储监控数据
data_lock = threading.Lock()
data = pd.DataFrame(columns=["时间", "CPU使用率", "内存使用情况", "磁盘使用情况"])

# 定义后台线程定时获取数据
def monitor_server(host, port, username, password, interval=5):
    global data
    while True:
        metrics = get_server_metrics(host, port, username, password)
        print(metrics)
        if metrics:
            with data_lock:
                current_time = pd.Timestamp.now()
                metrics["时间"] = current_time
                data = pd.concat([data, pd.DataFrame([metrics])]).tail(100)  # 只保留最近100条记录
        time.sleep(interval)


# 启动监控线程
host = "192.168.21.130"  # 替换为远程服务器IP
port = 22  # SSH端口
username = "root"  # 替换为用户名
password = "RootKeytop:2020#"  # 替换为密码

thread = threading.Thread(target=monitor_server, args=(host, port, username, password), daemon=True)
thread.start()

# 创建Dash应用
app = Dash(__name__)

app.layout = html.Div([
    html.H1("远程服务器性能监控"),
    dcc.Graph(id="performance-graph"),
    dcc.Interval(
        id="update-interval",
        interval=5000,  # 每5秒刷新一次
        n_intervals=0
    )
])

@app.callback(
    Output("performance-graph", "figure"),
    [Input("update-interval", "n_intervals")]  # 正确写法
)
def update_graph(n):
    global data
    with data_lock:
        if data.empty:
            return go.Figure()

        # 创建折线图
        figure = go.Figure()
        for metric in ["CPU使用率", "内存使用情况", "磁盘使用情况"]:
            figure.add_trace(
                go.Scatter(
                    x=data["时间"],
                    y=data[metric],
                    mode="lines+markers",
                    name=metric
                )
            )

        # 更新布局
        figure.update_layout(
            title="远程服务器性能监控",
            xaxis_title="时间",
            yaxis_title="使用率 (%)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, range=[0, 100]),
            legend=dict(x=0, y=1)
        )
        return figure


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)

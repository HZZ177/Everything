"""

"""
import hashlib
import time
import uuid
from urllib.parse import urlencode

appId = "22787"
appSecret = "b85e96cb109f4cd9a94c03e7bff18165"
pageNo = 1
pageSize = 10
parkId = "230025319"
parkNo = "测试01"
startTime = "2023-11-1 00:00:00"
endTime = "2023-11-2 16:00:00"
serviceCode = "getParkInOutEventList"

# Generate a request ID using UUID
reqId = str(uuid.uuid4()).replace('-', '')

# Get the current timestamp
ts = int(time.time() * 1000)

# Create a dictionary of all parameters
params = {
    "pageNo": pageNo,
    "pageSize": pageSize,
    "parkId": parkId,
    "parkNo": parkNo,
    "startTime": startTime,
    "endTime": endTime,
    "reqId": reqId,
    "serviceCode": serviceCode,
    "ts": ts
}

# Sort the parameters by key and concatenate them into a string
sorted_keys = sorted(params.keys())
result = []
for key in sorted_keys:
    value = params[key]
    result.append(f"{key}={value}")

result_string = '&'.join(result)
sign_string = f"{result_string}&{appSecret}"

# Generate the MD5 hash of the concatenated string
m = hashlib.md5()
m.update(sign_string.encode('utf-8'))
key = m.hexdigest().upper()

# Print the required values
print("The generate key is:", key)
print("The generate request id is:", reqId)

# Set all the required variables. In an actual application, you'd probably
# want to return these from a function or use them directly, not just print them.
print("=============================================================")
print(f'appId: {appId}')
print(f'key: {key}')
print(f'pageNo: {pageNo}')
print(f'pageSize: {pageSize}')
print(f'parkId: {parkId}')
print(f'parkNo: {parkNo}')
print(f'startTime: {startTime}')
print(f'endTime: {endTime}')
print(f'reqId: {reqId}')
print(f'serviceCode: {serviceCode}')
print(f'ts: {ts}')

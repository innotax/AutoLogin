import win32com.client
import json

print('*'*100)
ift = win32com.client.Dispatch('iftWinExAdapter.clsAdapter')

j = {
    "appCd": "InfotechApiDemo",
    "orgCd": "hometax",
    "svcCd": "Z0001",
    "bizNo": "1388148652,1148532166"
}

js = json.dumps(j)
res = ift.serviceCall(js)

print(js)
print(res)

# import sys
# print("*"*10)
# print(sys.version)


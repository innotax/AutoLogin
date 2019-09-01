# 32bit only
import json
import win32com.client

iftCertdll = win32com.client.Dispatch("iftCoreEngine.iftGate")
iftServicedll = win32com.client.Dispatch("iftWinExAdapter.clsAdapter")

req_js_str = ""

res_js_str = iftCertdll.getUserCert(req_js_str)

cert_dict = json.loads(res_js_str)

print(cert_dict['cert_nm'], cert_dict['cert_pw'])
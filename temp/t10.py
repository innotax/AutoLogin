import json
import win32com.client

iftCertdll = win32com.client.Dispatch("iftCoreEngine.iftGate")
iftServicedll = win32com.client.Dispatch("iftWinExAdapter.clsAdapter")


def cert_nm_pw():
    # return 공인인증서 명칭 비밀번호
    iftCertdll = win32com.client.Dispatch("iftCoreEngine.iftGate")
    req_js_str = ""
    js_str = iftCertdll.getUserCert(req_js_str)
    dic = json.loads(js_str)

    cert_nm = dic["cert_nm"]
    cert_pw = dic["cert_pw"]

    return (str(cert_nm), str(cert_pw))

js_str = cert_nm_pw()
print(js_str)

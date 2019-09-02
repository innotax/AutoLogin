import json
import win32com.client

def cert_nm_pw():
    iftCertdll = win32com.client.Dispatch("iftCoreEngine.iftGate")
    req_js_str = ""
    js_str = iftCertdll.getUserCert(req_js_str)
    dic = json.loads(js_str)

    cert_nm = dic["cert_nm"]
    cert_pw = dic["cert_pw"]

    return (cert_nm, cert_pw)

# a = cert_nm_pw()
cert_nm, cert_pw = cert_nm_pw()

print(cert_nm, cert_pw)
if not cert_nm:
    print('empt')
    print(cert_nm)

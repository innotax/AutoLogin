import json
import pandas as pd
from pprint import pprint

#============== 1. json to dic
fulljs = r'C:\Ataxtech\ATT\Ver1.0\json\web.json'

with open(fulljs, encoding='utf-8') as fn:
    dic = json.load(fn)                      # dic : dic_dic_lst_dic
idpw_dic_lst_dic = dic['idpw']               # idpw_dic_lst_dic : dic_lst_dic

#============== 2. dic_lst_dic to Dataframe
columns = ['website', 'id', 'pw']      # website : dic_lst_dic.keys() 컬럼
web_id_pw = []
empty_site_lst = []                             # id,pw 없는 사이트 json file 관리 위해 2
for website in idpw_dic_lst_dic.keys():    
    idpw_lst_dic = idpw_dic_lst_dic[website]
    if idpw_lst_dic:
        for d in idpw_lst_dic:
            _id = d['id']
            _pw = d['pw']
            web_id_pw.append([website, _id, _pw])
            continue
        continue
    # web_id_pw.append([website, "", ""])        # id,pw 없는 사이트 json file 관리 위해 1
    empty_site_lst.append(website)               # id,pw 없는 사이트 json file 관리 위해 2
            
df = pd.DataFrame(web_id_pw, columns=columns)

print("  2. >> type(df) : ", type(df), "="*100)
pprint(df)

#============= 3. Dataframe to original dic_lst_dic : https://hoy.kr/dXq62
# 1. 값 있는 것
df_to_dict = df.to_dict('split')                    
_data_lst_lst = df_to_dict['data']
pprint(_data_lst_lst)
# 2. 값 없는 것
empty_site_lst_lst = [[website, "", ""] for website in empty_site_lst]
pprint(empty_site_lst_lst)
# 3. 1+2
data_lst_lst = _data_lst_lst + empty_site_lst_lst
pprint(data_lst_lst)


web_dic_lst_dic = dict()

for web, id, pw in data_lst_lst:
    inner_dic = dict()

    inner_dic['id'] = id
    inner_dic['pw'] = pw

    if inner_dic['id'] != "":    
        if web in web_dic_lst_dic.keys():
            web_dic_lst_dic[web].append(inner_dic)    # nd2 id/pw 이후
            continue
        web_dic_lst_dic[web] = [inner_dic]            # first id/pw
        continue
    web_dic_lst_dic[web] = []                         # id/pw 가 없는 경우
           
print("  3. >> type(web_dic_lst_dic) : ", type(web_dic_lst_dic), "="*100)
pprint(web_dic_lst_dic)

#============ 4. dict to json
fulljs = r'C:\Ataxtech\ATT\Ver1.0\json\web.json'
dic['idpw'] = web_dic_lst_dic
with open(fulljs, 'w', encoding='utf-8') as fn:
    json.dump(dic, fn, ensure_ascii=False, indent=4)


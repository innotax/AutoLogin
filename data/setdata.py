import os, sys, time, json, zipfile

# 상위폴더 내 파일 import  https://brownbears.tistory.com/296
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from data import data
from utils import Util

# 처음시작시 경로설정
root_path = "C:\\"
ift_dir = "Infotech"                  # 스크래핑 모듈
ift_path = os.path.join(root_path, ift_dir)
att_dir = "Ataxtech"
att_path = os.path.join(root_path, att_dir)
main_dir = "AutoLogin"
main_path = os.path.join(att_path, main_dir)          # APP 저장경로
st1_app_dir = ['loginAPP', 'data']
st1_app_path = os.path.join(main_path, st1_app_dir[0]) # 첫번째앱 저장경로
driver_path = os.path.join(st1_app_path, "driver")    # 크롬드라이버 저장경로
data_path = os.path.join(st1_app_path, "data")        # json 파일 등 저장경로
json_fn = "data.json"                                 # 
full_json_fn = os.path.join(data_path, json_fn)       # json 파일 full 경로

def set_path_make_json_return_dic():   
    """ 앱 경로설정
    """
    """ 인포텍 모쥴 설치
    if not os.path.isdir(ift_path):
        import subprocess
        ''' atmui.py 와 동일한 경로에 iftNxService_setup_20190304.exe 저장
        '''
        full_ift_setup_path = os.path.join(os.getcwd(), 'iftNxService_setup_20190304.exe') 
        PIPE = subprocess.PIPE
        subprocess.Popen(full_ift_setup_path, stdin=PIPE, stdout=PIPE)
    """
    # json 파일이 있으면 dic 변환후 리턴
    if os.path.isfile(full_json_fn):
        # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
        with open(full_json_fn, encoding='utf-8') as fn:
            nts_dict = json.load(fn) 
        return nts_dict
        
    else:
        try:
            if not os.path.isdir(att_path):
                Util.make_sub_dirs(root_path, att_dir)
        except:
            pass

        try:
            if not os.path.isdir(main_path):
                Util.make_sub_dirs(att_path, main_dir)
        except:
            pass

        # 앱 경로에 하위 경로 설정하고 json 파일 생성후 생성된 json 파일에서 변수로 활용할 파이썬 객체 (nts_dict) 생성
        try:
            if not os.path.isdir(st1_app_path):
                # 1. 하위 APP 디렉토리 없으면 만들고
                Util.make_sub_dirs(main_path, *st1_app_dir)
                Util.make_sub_dirs(st1_app_path, "driver") 

                # 1.1 크롬드라이버, 인포텍 모쥴 설치(exe 파일과 zip 파일을 같은 경로에...)
                try:
                    with zipfile.ZipFile(os.path.join(os.getcwd(), "driver_iftsetup.zip")) as zf:
                        zf.extractall(driver_path)
                except:
                    pass

                # 2. 딕셔너리를 json 파일로 만들어 저장
                nts_dict = data.get_nts_dict()
                nts_dict['secret']['크롬경로'] = driver_path      
                with open(full_json_fn, 'w', encoding='utf-8') as fn:
                    json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
                    # json_data = json.dumps(_dict_data, ensure_ascii=False, indent=4)

                # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
                with open(full_json_fn, encoding='utf-8') as fn:
                    nts_dict = json.load(fn)

            elif os.path.isdir(st1_app_path):
                if not os.path.isfile(full_json_fn):
                # 2. 딕셔너리를 json 파일로 만들어 저장
                    nts_dict = data.get_nts_dict()        
                    with open(full_json_fn, 'w', encoding='utf-8') as fn:
                        json.dump(nts_dict, fn, ensure_ascii=False, indent=4)
                        # json_data = json.dumps(_dict_data, ensure_ascii=False, indent=4)

                    # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
                    with open(full_json_fn, encoding='utf-8') as fn:
                        nts_dict = json.load(fn) 

                elif os.path.isfile(full_json_fn):
                    # 3. 저장된 json 파일을 파이썬 객체(딕셔너리)로...
                    with open(full_json_fn, encoding='utf-8') as fn:
                        nts_dict = json.load(fn) 
        except:
            pass
        finally:
            return nts_dict

def get_nts_dict():

    nts_dict = dict()
    nts_dict['메인영역'] = "txppIframe"

    secret = dict()

    elem_id = dict()
    login = dict()
    menu = dict()
    minone = dict()
    semudaeli = dict()
    singodaeli = dict()

    # nts_dict > secret
    secret['딜레이타임'] = "0.7"
    secret['부서아이디'] = "innotax154"
    secret['부서비번'] = "dlshxortm14!"
    secret['세무사관리번호'] = "W15960"
    secret['세무사비번'] = "1234"
    secret['공인인증서명칭'] = "세무법인이노택스테헤(BizBank)008802520131101188000459"
    secret['공인인증서비번'] = "innotax1260!"
    secret['크롬경로'] = "/zz/NTS/driver/"
    secret['크롬드라이버'] = "chromedriver.exe"
    secret['수퍼아이디'] = "innotax14"

    # nts_dict > elem_id > login
    login['최상단로그인'] = "group1544" 
    login['인증서로그인'] = "trigger38"
    login['부서아이디'] = "iptUserId" 
    login['부서비번'] = "iptUserPw"
    login['부서아이디로그인'] = "trigger46"
    login['세무사관리번호'] = "input1"
    login['세무사비번'] = "input2"
    login['최종로그인'] = "trigger41"

    login['공인인증서영역'] = "dscert"
    login['공인인증서명칭'] = f"{secret['공인인증서명칭']}"  ######################
    login['공인인증서비번'] = "input_cert_pw"
    login['공인인증서확인'] = "btn_confirm_iframe"

    # nts_dict > elem_id > menu
    menu['홈택스로고'] = "hdGroup814"  # h1 메뉴내 좌상로고
    ### 첫화면 메인메뉴
    # menu['메인영역'] = "txppIframe"   ### 최상위(nts_dict)로 이동
    menu['조회발급'] = "group1300"
    menu['민원증명'] = "group1302"
    menu['신청제출'] = "group1304"
    menu['신고납부'] = "group1314"
    menu['상담제보'] = "group1316"
    menu['세무대리인'] = "group1410"

    ### 상단 메뉴
    menu['조회발급_s'] = "hdGroup913"
    menu['민원증명_s'] = "hdGroup915"
    menu['신청제출_s'] = "hdGroup917"
    menu['신고납부_s'] = "hdGroup919"
    menu['상담제보_s'] = "hdGroup921"
    menu['세무대리인_s'] = "hdGrp921"

    # 민원증명 nts_dict > elem_id > minone
    minone['납세사실증명'] = "a_0206060000"
    minone['주민번호앞'] = "inputCvaAplnBscClntResRgtNo1"
    minone['주민번호뒤'] = "inputCvaAplnBscClntResRgtNo2"
    minone['주민번호확인'] = "btnCvaAplnBscClntFnmTnm"
    minone['수임여부'] = "rbChkClntAfaYn_input_0"
    minone['주민번호공개여부'] = "rbCvaAplnRecptResNoOpYn_input_0"
    minone['발급수량'] = "cmbCvaAplnRecptIsnHopeQty"
    minone['세목'] = "itrfCd"
    minone['수납시작년'] = "cerStrtYr"
    minone['수납시작월'] = "cerStrtMm"
    minone['수납종료년'] = "cerEndYr"
    minone['수납종료월'] = "cerEndMm"
    minone['사용용도'] = "fctCerTypeCd"
    minone['제출처'] = "cmbCvaDcumSbmsOrgnClCd"
    minone['신청하기'] = "btnApln"

    minone['민원사무명'] = "grdCvaAlfaBrkdInqr_cell_0_4"
    minone['발급수량'] = "grdCvaAlfaBrkdInqr_cell_0_11"
    minone['증명접수일시'] = "grdCvaAlfaBrkdInqr_cell_0_8"
    minone['증명발급번호'] = "grdCvaAlfaBrkdInqr_cell_0_12"

    ### 세무대리 > 수임납세자 정보조회 nts_dict > elem_id > semudaeli
    semudaeli['수임납세자조회'] = "a_0601050000"

    semudaeli['사업자기본사항'] = "a_0601010100"
    semudaeli['사업용계좌신고현황'] = "a_0601010200"
    semudaeli['고지내역'] = "a_0601010300"
    semudaeli['체납내역'] = "a_0601010400"
    semudaeli['환급금'] = "a_0601010500"
    semudaeli['부가세신고도움'] = "a_0601012900"
    semudaeli['부가세예정고지세액'] = "a_0601010600"
    semudaeli['화물운전복지카드누계'] = "a_0601011000"
    semudaeli['부가세성실신고안내'] = "a_0601012700"
    semudaeli['사업장현황신고도움'] = "a_0601013000"
    semudaeli['종합소득세신고도움'] = "a_0601011100"
    semudaeli['법인세중간예납세액'] = "a_0601011400"
    semudaeli['연금건강고용산재보험료'] = "a_0601012800"
    semudaeli['현지기업고유번호'] = "a_0601011600"
    semudaeli['부가세신고용합계표'] = "a_0601012000"
    semudaeli['신용카드매출자료'] = "a_0601012100"
    semudaeli['현금영수증매출총액'] = "a_0601012200"
    semudaeli['사업용신용카드누계'] = "a_0601012300"
    semudaeli['전자(세금)계산서'] = "a_0601012400"
    semudaeli['전자(세금)계산서합계표'] = "a_0601012500"
    semudaeli['부가세매입자납부특례'] = "a_0601013100"
    semudaeli['납부서출력'] = "a_0601013200"
    
    ### 세무대리 > 신고대리 정보조회  nts_dict > elem_id > singodaeli
    singodaeli['부가세신고도움_신고대리'] = "a_0602041200"
    singodaeli['부가세예정고지세액_신고대리'] = "a_0602040100"
    singodaeli['신용카드매출자료_신고대리'] = "a_0602040200"
    singodaeli['현금영수증매출총액_신고대리'] = "a_0602040300"
    singodaeli['사업용신용카드누계_신고대리'] = "a_0602040400"
    singodaeli['화물운전복지카드누계_신고대리'] = "a_0602040500"
    singodaeli['종합소득세신고도움_신고대리'] = "a_0602040600"
    singodaeli['연금건강고용산재보험료_신고대리'] = "a_0602041000"
    singodaeli['전자(세금)계산서_신고대리'] = "a_0602040700"
    singodaeli['전자(세금)계산서합계표_신고대리'] = "a_0602040800"
    singodaeli['부가세신고용합계표_신고대리'] = "a_0602040900"
    singodaeli['증여세결정정보'] = "a_0602041100"
    singodaeli['부가세매입자납부특례_신고대리'] = "'a_0602041300"

    
    nts_dict['secret'] = secret

    elem_id['login'] = login
    elem_id['menu'] = menu
    elem_id['minone'] = minone
    elem_id['semudaeli'] = semudaeli
    elem_id['singodaeli'] = singodaeli

    nts_dict['elem_id'] = elem_id

    return nts_dict
    
# nts_dict = set_path_make_json_return_dic() 

# 브라우저 높이에 따른 크롬 실행환경 변경 flag
flag_window_height = True

# 셀레니움 Xpath element 반환함수

if __name__ == '__main__':
    
    nts_dic = set_path_make_json_return_dic()
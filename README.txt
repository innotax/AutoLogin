'''배포판 실행파일(exe) 만들기 https://wikidocs.net/21952  https://winterj.me/pyinstaller/
pyinstaller 디코딩에러 수정 https://stackoverflow.com/questions/47692960/error-when-using-pyinstaller-unicodedecodeerror-utf-8-codec-cant-decode-byt
I found an answer on another forum. I change the line number 427 in the Python\Lib\site-packages\Pyinstaller\compat.py file
'''
# 상위폴더 내 파일 import  https://brownbears.tistory.com/296
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
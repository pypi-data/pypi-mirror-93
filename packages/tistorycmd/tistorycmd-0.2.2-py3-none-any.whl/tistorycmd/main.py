from .auth import *
from .server import *
from .blog import *
import mistune

USAGE = """USAGE:
    # 블로그 정보 보기
    tistorycmd info

    # 카테고리 목록 보기
    tistorycmd category

    # 글쓰기
    tistorycmd post <제목> <내용|파일경로> <category_id> <태그>
    """


def main():
    if len(sys.argv) < 2:
        print(USAGE, file=sys.stderr)
        return

    auth = Auth()  # 로그인, oauth, 토큰 관련 클래스
    blog = Blog()  # 글쓰기, 블로그 관련 클래스
    command = sys.argv[1]  # 메뉴
    if command == 'info':
        blog.info()
    elif command == 'category':
        blog.category_list()
    elif command == 'post':
        if len(sys.argv) < 4:
            print(USAGE, file=sys.stderr)
            return

        cont_path = os.path.abspath(sys.argv[3])  # 내용 파일 경로
        history_file = os.path.dirname(cont_path) + '\\.tistory'  # 기존 등록내역파일

        title = sys.argv[2]  # 제목
        category = (len(sys.argv) > 4) and sys.argv[4] or ''  # 카테고리 (필수 x)
        tags = (len(sys.argv) > 5) and sys.argv[5] or ''  # 태그 (필수 x)
        content_md = ""  # 업로드할 파일내용 마크다운 형태
        overwrite_md = ""  # 덮어 쓸 내용 (이미지 계속 업로드 되는거 방지)

        # 이미지 있을 경우 파일 업로드
        with open(cont_path, 'r', encoding='UTF8') as fp:
            for line in fp:
                name_grp = re.search('(\!\[\s*)(\w+)(\s*\])(\(\s*)([^http:\/\/].*)(\s*\))', line)  # 이미지 형태 있는지 검사
                if (name_grp):
                    content_md += blog.file_upload(line, os.path.dirname(cont_path))
                    overwrite_md += blog.file_upload(line, os.path.dirname(cont_path))
                else:
                    content_md += line
                    overwrite_md += line

        # 파일내용 덮어쓰기 (이미지 계속 업로드 되는거 방지)
        if os.path.exists(cont_path):
            with open(cont_path, 'w', encoding='utf-8') as make_file:
                make_file.write(overwrite_md)

        content_html = mistune.markdown(content_md)  # 업로드 할 파일 내용 html 형태
        if (os.path.isfile(history_file)):
            # 글수정
            blog.post_edit(history_file, title, content_html, category, tags)
        else:
            # 글쓰기
            blog.post_write(history_file, title, content_html, category, tags)
    else:
        print(USAGE, file=sys.stderr)
        return
# 뭐입지? (Django 기반 웹 프로젝트)

사용자의 날씨와 스타일 고민을 덜어주는 커뮤니티 기반 서비스입니다.  
기온과 체감정보, 민감도를 고려해 의견을 공유하고, 다른 사용자의 팁을 참고할 수 있습니다.

## 📁 주요 기능

- 기상청 API를 활용한 날씨 기반 홈화면
- 게시판 (글 작성, 수정, 삭제, 검색)
- 댓글, 추천, 스크랩 기능
- 마이페이지, 회원가입 및 로그인
- 미니게임: 가위바위보, 로또

## 🧱 기술 스택

- **Backend**: Django, Python
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **API**: 기상청 단기예보 API


## 🔧 프로젝트 실행 방법

    1. 프로젝트 클론  
        ```
        git clone https://github.com/sua-repo/django_psa_weatherboard.git
        ```

    2. 가상환경 생성 및 활성화 (Windows 기준)

    3. 의존성 설치
        ```
        pip install -r requirements.txt
        ```

    4. 환경 변수 설정 (.env 파일 생성)
        ```
        # 네이버 지도
        NAVER_API_CLIENT_ID=
        NAVER_API_CLIENT_SECRET=

        # 단기예보 (초단기예보 포함)
        KMA_SHORT_ENDPOINT=
        KMA_SHORT_ENCODED_KEY=
        KMA_SHORT_DECODED_KEY=

        # 중기예보
        KMA_MID_ENDPOINT=
        KMA_MID_ENCODED_KEY=
        KMA_MID_DECODED_KEY=

        # 구글 지도
        GOOGLE_API_KEY=
        ```

    5. 마이그레이션 및 서버 실행
        ```
        python manage.py makemiigrations
        python manage.py migrate
        python manage.py runserver
        ```

    6. 웹 브라우저 접속
        http://127.0.0.1:8000/

## 🌐 URL-View 매핑표
| URL 경로                                    | View 함수          | 앱        | name             | 설명                |
| ----------------------------------------- | ---------------- | -------- | ---------------- | ----------------- |
| `/`                                       | `index`          | main     | `index`          | 홈 화면              |
| `/get-address/`                           | `get_address`    | main     | `get_address`    | 위도·경도 → 주소 변환 API |
| `/get-weather/`                           | `get_weather`    | main     | `get_weather`    | 날씨 데이터 가져오기 API   |
| `/board/`                                 | `post_list`      | board    | `post_list`      | 게시글 목록            |
| `/board/create/`                          | `post_create`    | board    | `post_create`    | 게시글 작성            |
| `/board/<int:post_id>/`                   | `post_detail`    | board    | `post_detail`    | 게시글 상세 보기         |
| `/board/update/<int:post_id>/`            | `post_update`    | board    | `post_update`    | 게시글 수정            |
| `/board/delete/<int:post_id>/`            | `post_delete`    | board    | `post_delete`    | 게시글 삭제            |
| `/board/comment/<int:post_id>/`           | `comment_create` | board    | `comment_create` | 댓글 작성             |
| `/board/comment/update/<int:comment_id>/` | `comment_update` | board    | `comment_update` | 댓글 수정             |
| `/board/comment/delete/<int:comment_id>/` | `comment_delete` | board    | `comment_delete` | 댓글 삭제             |
| `/board/post/<int:post_id>/like/`         | `post_like`      | board    | `post_like`      | 게시글 추천            |
| `/board/post/<int:post_id>/scrap/`        | `post_scrap`     | board    | `post_scrap`     | 게시글 스크랩           |
| `/accounts/login/`                        | `login_user`     | accounts | `login_user`     | 로그인               |
| `/accounts/logout/`                       | `logout_user`    | accounts | `logout_user`    | 로그아웃              |
| `/accounts/signup/`                       | `signup_user`    | accounts | `signup_user`    | 회원가입              |
| `/accounts/mypage/`                       | `mypage`         | accounts | `mypage`         | 마이페이지             |
| `/accounts/edit/`                         | `edit_user`      | accounts | `edit_user`      | 마이페이지 정보 수정       |
| `/game/rsp/`                              | `rsp`            | game     | `rsp`            | 가위바위보 게임          |
| `/game/lotto/`                            | `lotto`          | game     | `lotto`          | 로또 번호 추첨          |

## 📚 자세한 설명

👉 [노션 문서에서 확인하기](https://www.notion.so/Weather-Board-242f8c4af472804c9739f337016609d0)

import streamlit as st

st.set_page_config(
    page_title="재현이네 연차 관리 매니저",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 메인 페이지
st.title("📅 (WIP) 재현이네 연차 관리 매니저")
st.markdown("---")

st.header("미구현 부분")
st.write("**개인정보(주민번호, 입사일, 퇴사일, 부서, 직위 등) 표기**")
st.write("**직원 DB 추가/삭제/업데이트**")
st.write("**그 외 고객님 추가 요구사항**")

st.markdown("---")

st.info("""
### 💡 연차 업데이트 테스트 방법
1. [재현이네(마스터) 샘플 파일](https://raw.githubusercontent.com/Jootingstar/WorkLifeBalance/main/samples/%EC%9E%AC%ED%98%84%EC%9D%B4%EB%84%A4.xlsx) 파일을 다운로드 하세요.
2. [테니스부 2월 시트파일](https://raw.githubusercontent.com/Jootingstar/WorkLifeBalance/main/samples/%ED%85%8C%EB%8B%88%EC%8A%A4%EB%B6%80_26_2.xlsx) 파일을 다운로드 하세요.
3. 좌측의 update 메뉴를 클릭
4. 다운로드한 마스터파일, 팀별 시트 파일을 선택하세요.
5. 업데이트 된 내용을 확인 후 시트 업데이트 및 적용된 마스터 파일을 다운로드 하세요.

### 💡 직원별 사용 이력 조회 테스트 방법
1. 좌측의 inquiry 메뉴를 클릭
2. 재현이네(마스터) 파일을 선택
""")


st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 연차 업데이트")

with col2:
    st.subheader("🔍 직원별 사용 이력 조회")

st.markdown("---")

st.caption("ℹ️ GitHub https://github.com/Jootingstar/WorkLifeBalance")

# 자동으로 업데이트 페이지로 리다이렉트
# st.switch_page("pages/1_update.py")

import streamlit as st

st.set_page_config(
    page_title="WIP 재현이네 연차 관리 매니저",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 메인 페이지
st.title("📅 재현이네 연차 관리 매니저")
st.markdown("---")

st.header("미구현 부분")
st.write("**개인정보(주민번호, 입사일, 퇴사일, 부서, 직위 등) 표기**")
st.write("**그 외 고객님 추가 요구사항**")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 연차 업데이트")

with col2:
    st.subheader("🔍 직원별 사용 이력 조회")

st.markdown("---")

# st.info("""
# ### 💡 사용 방법
# """)

# 자동으로 업데이트 페이지로 리다이렉트
# st.switch_page("pages/1_update.py")

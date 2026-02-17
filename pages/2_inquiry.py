import streamlit as st
import pandas as pd
import os
import sys
import tempfile

# 상위 디렉토리의 business_logic 모듈 import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from business_logic import load_teamSheet

st.set_page_config(page_title="멤버별 조회", page_icon="🔍", layout="wide")

st.title("🔍 멤버별 일정 조회")
st.markdown("---")

st.header("📂 전체 일정 시트 파일")
st.caption("ℹ️ PC의 어느 폴더에서든 파일을 선택할 수 있습니다")
target_file = st.file_uploader("전체 일정 시트 파일을 선택하세요", type=['xlsx'], key="member_query_file")

if target_file:
    st.markdown("---")
    
    # 업로드된 파일을 임시 폴더에 저장
    temp_dir = tempfile.mkdtemp()
    target_path = os.path.join(temp_dir, target_file.name)
    with open(target_path, 'wb') as f:
        f.write(target_file.getbuffer())
    
    st.success(f"✅ 파일이 로드되었습니다: `{target_file.name}`")
    
    try:
        # Excel 파일 읽기
        excel_file = pd.ExcelFile(target_path)
        sheet_names = excel_file.sheet_names
        
        # 시트 선택
        selected_sheet = st.selectbox("조회할 시트를 선택하세요:", sheet_names)
        
        if selected_sheet:
            # Team 시트 읽기
            df_team, has_data = load_teamSheet(target_path, selected_sheet)
            
            if not has_data or df_team.empty:
                st.warning("⚠️ 선택한 시트에 데이터가 없습니다.")
            else:
                # 멤버별 총 일수 계산
                member_summary = df_team.groupby('name')['days'].agg([
                    ('총_일수', 'sum'),
                    ('일정_간수', 'count')
                ]).reset_index()
                
                member_summary = member_summary.sort_values('총_일수', ascending=False)
                
                st.subheader(f"📊 멤버별 총 사용일수 (총 {len(member_summary)}명)")
                
                # 순위 통계
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("총 멤버 수", f"{len(member_summary)}명")
                with col2:
                    st.metric("전체 일정 간수", f"{member_summary['일정_간수'].sum()}건")
                with col3:
                    st.metric("전체 사용 일수", f"{member_summary['총_일수'].sum()}일")
                
                st.markdown("---")
                
                # 멤버별 통계 테이블
                st.dataframe(member_summary, use_container_width=True)
                
                st.markdown("---")
                
                # 특정 멤버 상세 조회
                st.subheader("🔍 멤버 상세 조회")
                member_names = sorted(df_team['name'].unique())
                selected_member = st.selectbox("멤버를 선택하세요:", member_names)
                
                if selected_member:
                    member_data = df_team[df_team['name'] == selected_member].copy()
                    member_data = member_data.sort_values('start_date', ascending=False)
                    
                    # 날짜를 date 형식으로 변환하여 표시
                    member_data_display = member_data.copy()
                    member_data_display['start_date'] = member_data_display['start_date'].dt.date
                    member_data_display['end_date'] = member_data_display['end_date'].dt.date
                    
                    total_days = member_data['days'].sum()
                    
                    st.markdown(f"### {selected_member}의 일정 (총 {total_days}일, {len(member_data)}건)")
                    st.dataframe(member_data_display, use_container_width=True)
    
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

else:
    st.info("ℹ️ Excel 파일을 선택해주세요.")

st.markdown("---")
st.caption("ℹ️ 서버별: 1) 진행 일정 시트 파일 선택 → 2) 조회할 시트 선택 → 3) 멤버별 통계 확인")

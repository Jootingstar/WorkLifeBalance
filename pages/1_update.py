import streamlit as st
import pandas as pd
import os
import sys
import tempfile

st.set_page_config(page_title="일정 업데이트", page_icon="📝", layout="wide")

st.title("📝 일정 관리 시스템")
st.markdown("---")

# 상위 디렉토리의 business_logic 모듈 import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from business_logic import (
    process_source_data,
    load_teamSheet,
    find_new_data,
    merge_and_sort_data,
    save_to_excel,
    create_yearly_summary
)

col1, col2 = st.columns(2)

with col1:
    st.header("1️⃣ 진행 일정 시트 파일")
    target_file = st.file_uploader("진행 일정 시트 파일을 선택하세요 (마스터 파일)", type=['xlsx'], key="target")

with col2:
    st.header("2️⃣ 추가 일정 시트 파일")
    source_file = st.file_uploader("추가 일정 시트 파일을 선택하세요 (신규 데이터)", type=['xlsx'], key="source")

if target_file and source_file:
    st.markdown("---")
    
    # 업로드된 파일을 임시 폴더에 저장
    temp_dir = tempfile.mkdtemp()

    # 전체 일정 시트 파일 임시 저장
    target_path = os.path.join(temp_dir, target_file.name)
    with open(target_path, 'wb') as f:
        f.write(target_file.getbuffer())
    
    # 추가 일정 시트 파일 임시 저장
    source_path = os.path.join(temp_dir, source_file.name)
    with open(source_path, 'wb') as f:
        f.write(source_file.getbuffer())
    
    st.success(f"✅ 파일이 로드되었습니다!")
    st.info(f"📂 진행 일정: `{target_file.name}`\n\n📂 추가 일정: `{source_file.name}`")
    
    st.markdown("---")
    
    try:
        # 1. 데이터 파일에서 데이터 읽기
        excel_source = pd.ExcelFile(source_path)

        # 시트 선택
        sheet_names = excel_source.sheet_names
        sheet_name = excel_source.sheet_names[0]
        
        df_source, source_data = process_source_data(source_path, sheet_name)
        
        if source_data is None:
            st.error("⚠️ 시트 포멧이 맞지 않습니다. 최소 4개의 컬럼(이름, 시작일, 종료일, 일수)이 필요합니다.")
            st.stop()
        
        # 2. Team 시트 읽기 (실제 파일 시스템에서 읽기)
        df_team, has_data = load_teamSheet(target_path, sheet_name)
        
        if not has_data:
            st.info("ℹ️ Team 시트가 비어있습니다. 새로 생성합니다.")
        
        # 3. 중복 체크
        new_data = find_new_data(source_data, df_team)
        
        st.subheader(f"📊 추가할 새 데이터 ({len(new_data)}건)")
        if not new_data.empty:
            new_data_display = new_data.copy()
            new_data_display['start_date'] = new_data_display['start_date'].dt.date
            new_data_display['end_date'] = new_data_display['end_date'].dt.date
            st.dataframe(new_data_display, use_container_width=True)
        else:
            st.success("✅ 추가할 새 데이터가 없습니다. (이미 추가 되어 있음)")
        
        # 4. 업데이트 미리보기
        df_team_updated = merge_and_sort_data(df_team, new_data)
        
        df_team_updated_display = df_team_updated.copy()
        df_team_updated_display['start_date'] = df_team_updated_display['start_date'].dt.date
        df_team_updated_display['end_date'] = df_team_updated_display['end_date'].dt.date
        
        # st.subheader(f"📋 업데이트 후 Team 데이터 ({len(df_team_updated)}건)")
        # st.dataframe(df_team_updated_display, use_container_width=True)
        
        st.markdown("---")
        
        # 5. 업데이트 버튼
        if st.button("✅ Team 시트 업데이트 및 다운로드", type="primary", use_container_width=True):
            try:
                save_to_excel(target_path, df_team_updated, sheet_name)
                
                # 연도별 집계 생성
                with st.spinner("'폴상사' 시트를 업데이트 중..."):
                    create_yearly_summary(target_path)
                    st.success("✅ 업데이트 완료!")
                
                # 업데이트된 파일을 다운로드 버튼으로 제공
                with open(target_path, 'rb') as f:
                    st.download_button(
                        label="📥 업데이트된 파일 다운로드",
                        data=f.read(),
                        file_name=target_file.name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                st.info("ℹ️ 다운로드 버튼을 클릭하여 업데이트된 파일을 저장하세요.")
            
            except Exception as e:
                st.error(f"❌ 파일 저장 중 오류 발생: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
    
    except Exception as e:
        st.error(f"❌ 오류 발생: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

else:
    st.info("ℹ️ 두 개의 Excel 파일을 선택해주세요.")

st.markdown("---")
st.caption("ℹ️ 서버별: 1) 진행 일정 시트 파일 선택 → 2) 추가 일정 시트 파일 선택 → 3) 멤버별 통계 확인")

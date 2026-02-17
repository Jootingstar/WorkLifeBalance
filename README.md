# WorkLifeBalance
Work &amp; Life Balance

🌿 WorkLifeBalance — 재현이네 연차 관리 시스템

> 직원들의 연차 일정을 Excel 기반으로 손쉽게 관리하고 집계하는 웹 애플리케이션입니다.

## 📌 주요 기능

| 기능 | 설명 |
|------|------|
| 📥 연차 사용 내역 업데이트 | 기존 전체 일정 파일에 새 일정 시트를 병합 |
| 🔍 직원별 연차 사용 이력 조회 | 팀원별 연차 사용 현황 및 상세 일정 확인 |

## 📂 프로젝트 구조

```
WorkLifeBalance/
├── app.py                  # 메인 페이지
├── business_logic.py       # 비즈니스 로직
├── console.py              # 콘솔 유틸리티 (console 테스트용)
├── pages/
│   ├── 1_update.py         # 일정 업데이트 페이지
│   └── 2_inquiry.py        # 멤버별 조회 페이지
├── samples/
│   └── 재현이네.xlsx        # 샘플 데이터 파일
└── README.md
```

## ⚙️ 설치 및 실행

### 요구사항

- Python 3.8 이상
- pip

🙌 만든 사람
jootingstar — 테니스 실력 향상을 위해 일과 삶의 균형을 유지하자.

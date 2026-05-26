import streamlit as str

# 1. 앱 제목 설정
str.title("💖 나의 연애 성공 확률 계산기")
str.subheader("재미로 보는 나의 연애 점수는 몇 점일까?")

str.write("---")

# 2. 사용자 입력 받기
name = str.text_input("당신의 이름을 입력해주세요:", placeholder="예: 홍길동")
crush_name = str.text_input("상대방의 이름을 입력해주세요:", placeholder="예: 성춘향")

# 3. 선택지 (라디오 버튼)
vibe = str.radio(
    "요즘 두 사람의 분위기는 어떤가요?",
    ("매일 연락하고 밤새 통화한다 📞", "가끔 연락하지만 만나면 즐겁다 ☕", "아직은 눈인사만 하는 사이 😳")
)

str.write("---")

# 4. 결과 출력 버튼
if str.button("❤️ 확률 확인하기"):
    if name and crush_name:
        str.success(f"**{name}** 님과 **{crush_name}** 님의 분석이 완료되었습니다!")
        
        # 선택지에 따른 결과 분기
        if "매일 연락" in vibe:
            str.balloons() # 화면에 풍선 애니메이션 효과
            str.metric(label="고백 성공 확률", value="99%", delta="그냥 오늘 고백하세요!")
        elif "가끔 연락" in vibe:
            str.metric(label="고백 성공 확률", value="65%", delta="조금만 더 용기를 내보세요.")
        else:
            str.metric(label="고백 성공 확률", value="20%", delta="우선 친해지는 것부터 시작!")
    else:
        str.warning("⚠️ 두 사람의 이름을 모두 입력해야 정확한 분석이 가능합니다.")

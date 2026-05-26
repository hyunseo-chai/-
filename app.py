import streamlit as st
from datetime import date

# 페이지 설정
st.set_page_config(page_title="우리만의 연애 앱", page_icon="💖")

st.title("💖 올인원 연애 앱")
st.write("확률 계산부터 디데이, 게임까지 한 번에 즐겨보세요!")

# 탭 생성 (메뉴 나누기)
tab1, tab2, tab3 = st.tabs(["❤️ 확률 계산기", "📅 디데이 계산기", "🎮 밸런스 게임"])

# --- 탭 1: 연애 성공 확률 계산기 ---
with tab1:
    st.header("고백 성공 확률 분석")
    name = st.text_input("당신의 이름:", placeholder="이름 입력")
    crush = st.text_input("상대방 이름:", placeholder="이름 입력")
    vibe = st.select_slider(
        "두 분의 현재 분위기는?",
        options=["어색함", "눈인사", "카톡중", "썸타는중", "거의커플"],
        value="카톡중"
    )
    
    if st.button("결과 확인 💘"):
        if name and crush:
            probs = {"어색함": "5%", "눈인사": "20%", "카톡중": "50%", "썸타는중": "85%", "거의커플": "99%"}
            st.success(f"**{name}**님과 **{crush}**님의 성공 확률은 **{probs[vibe]}**입니다!")
            if vibe in ["썸타는중", "거의커플"]:
                st.balloons()
        else:
            st.warning("이름을 입력해주세요!")

# --- 탭 2: 연애 디데이 계산기 ---
with tab2:
    st.header("우리의 소중한 시간")
    start_date = st.date_input("처음 만난(사귄) 날짜를 선택하세요:", value=date.today())
    today = date.today()
    
    passed_days = (today - start_date).days + 1
    
    if passed_days > 0:
        st.metric(label="함께한 시간", value=f"{passed_days}일째")
        st.write(f"💕 앞으로도 예쁜 사랑 하세요!")
    else:
        st.write("미래의 날짜를 선택하셨네요! 설레는 시작을 기다려봐요.")

# --- 탭 3: 커플 밸런스 게임 ---
with tab3:
    st.header("커플 밸런스 게임 🎮")
    st.subheader("Q. 더 용서할 수 없는 상황은?")
    choice = st.radio(
        "정답은 없습니다. 서로의 생각을 공유해보세요!",
        ["말없이 잠수타기 (잠수 이별)", "다른 사람과 환승하기 (환승 이별)"]
    )
    
    if st.button("결정 완료! ✅"):
        st.info(f"선택하신 답변: **{choice}**")
        st.write("상대방의 생각은 어떤지 물어보고 대화를 나눠보세요!")

import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(
    page_title="GlowUp - 맞춤형 외모 관리 가이드",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS로 감성적이고 깔끔한 UI 디자인 적용
st.markdown("""
    <style>
    .main {
        background-color: #FAFAFA;
    }
    .stButton>button {
        background-color: #FF8A8A;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        color: white;
    }
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    .routine-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border-left: 5px solid #FF8A8A;
    }
    .tip-title {
        color: #FF6B6B;
        font-weight: bold;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 데이터 정의 (안정성을 위해 내부 데이터셋 활용 및 에러 방지)
SKIN_CARE_DATA = {
    "지성 (기름기가 많고 모공이 넓음)": {
        "morning": ["약산성 폼클렌저로 과도한 유분 세안", "가벼운 워터 타입 토너로 수분 공급", "유분기 없는 오일프리 수분크림 수딩젤", "가볍고 산뜻한 플루이드 유기자차 자외선 차단제"],
        "night": ["클렌징 워터로 메이크업 및 노폐물 1차 세정", "약산성 클렌징 폼으로 2차 세안", "모공 케어 및 진정 성분(티트리, 바하) 앰플", "유수분 밸런스를 맞추는 젤 크림"],
        "tip": "기름이 많이 돈다고 수분 공급을 건너뛰면 피지가 더 많이 분비됩니다. 수분 위주의 레이어링을 해주세요."
    },
    "건성 (푸석하고 당김이 심함)": {
        "morning": ["물세안 또는 아주 부드러운 밀크 클렌저 사용", "콧물 제형의 고보습 스킨/토너 2회 레이어링", "세라마이드 성분이 함유된 보습 에센스", "촉촉한 크림 타입의 무기/혼합자차 자외선 차단제"],
        "night": ["클렌징 오일 또는 밤으로 부드럽게 메이크업 녹이기", "약산성 보습 클렌징 폼으로 세안", "피부 장벽을 강화하는 페이셜 오일 한 두 방울 또는 리치한 영양 크림", "주 1~2회 슬리핑 팩 활용"],
        "tip": "세안 후 물기가 마르기 전 3초 이내에 토너를 발라 수분 증발을 막아주는 것이 핵심입니다."
    },
    "복합성 (T존은 번들거리고 U존은 건조함)": {
        "morning": ["T존 위주로 가볍게 클렌징 폼 세안", "토너 패드로 T존은 닦아내고 U존은 흡수시키기", "부위별로 양을 조절하여 가벼운 로션 도포", "산뜻한 로션 제형의 자외선 차단제"],
        "night": ["립앤아이 리무버 후 클렌징 워터/젤로 세안", "수분 앰플을 얼굴 전체에 도포", "T존에는 젤 크림을 얇게, U존에는 보습 크림을 도톰하게 나누어 바르기"],
        "tip": "얼굴 부위별로 피부 상태가 다르므로 화장품을 바르는 양과 제형을 다르게 가져가는 지혜가 필요합니다."
    }
}

MAKEUP_DATA = {
    "데일리/출근 퀵 메이크업 (5분 완성)": [
        "1단계: 기초 케어 후 톤업 선크림을 얼굴 전체에 골고루 펴 발라 안색을 밝힙니다.",
        "2단계: 잡티나 다크서클 부위에만 컨실러를 살짝 찍어 바른 뒤 스펀지로 두드려 커버합니다.",
        "3단계: 스크류 브러쉬로 눈썹 결을 정리한 뒤, 빈 곳만 아이브로우 펜슬로 자연스럽게 채웁니다.",
        "4단계: 혈색을 주는 립밤이나 촉촉한 틴트를 입술 중앙부터 물들이듯 발라 마무리합니다."
    ],
    "면접/미팅 신뢰감을 주는 메이크업": [
        "1단계: 지속력을 위해 매트하거나 세미매트한 쿠션/파운데이션을 얇게 레이어링하여 밀착시킵니다.",
        "2단계: 차분한 브라운 계열의 음영 섀도우를 눈두덩이에 넓게 발라 깊이감 있는 눈매를 만듭니다.",
        "3단계: 깔끔한 인상을 위해 눈썹 산을 살짝 살려 깔끔하고 대칭이 맞게 눈썹을 그립니다.",
        "4단계: 아이라인은 과하게 빼지 않고 속눈썹 사이만 채우며, 립은 튀지 않는 말린장미(MLBB)나 차분한 코랄 컬러를 선택합니다."
    ],
    "특별한 날 화사한 꾸안꾸 메이크업": [
        "1단계: 은은한 광채를 주는 글로우 베이스나 쿠션을 사용하여 피부 바탕을 맑고 투명하게 표현합니다.",
        "2단계: 맑은 핑크나 피치 톤의 블러셔를 볼 중앙에 둥글게 굴려 생기와 귀여운 느낌을 더합니다.",
        "3단계: 펄이 미세하게 들어간 글리터 섀도우를 눈동자 위와 애교살에 살짝 얹어 눈가에 포인트를 줍니다.",
        "4단계: 앵두 같은 입술을 연출해 주는 탕후루 광택의 글래스 립 틴트를 발라 화사함을 극대화합니다."
    ]
}

MOTIVATION_QUOTES = [
    "오늘의 작은 관리가 1년 뒤 눈부신 차이를 만듭니다. ✨",
    "나를 아끼고 가꾸는 시간은 결코 낭비가 아닙니다. 🤍",
    "가장 아름다운 모습은 나다운 모습을 당당하게 드러낼 때 찾아옵니다. 🌿",
    "피부와 외모는 내가 보낸 시간과 정성을 속이지 않습니다. 💪",
    "오늘 밤 스킨케어 5분이 내일 아침 거울 앞의 미소를 만듭니다. 🥰"
]

# --- 사이드바 구성 ---
st.sidebar.title("✨ GlowUp 케어 룸")
st.sidebar.write("나를 가꾸는 가장 쉬운 자기관리 루틴")

menu = st.sidebar.radio(
    "원하는 관리 메뉴를 선택하세요:",
    ["🏠 홈 (오늘의 다짐)", "🧴 맞춤형 피부 케어", "💄 맞춤형 메이크업", "📅 나의 가꾸기 체크리스트"]
)

st.sidebar.markdown("---")
st.sidebar.caption("GlowUp v1.0.0 | 안전하고 직관적인 뷰티 매니저")


# --- 각 메뉴별 화면 구현 ---

# 1. 홈 화면
if menu == "🏠 홈 (오늘의 다짐)":
    st.title("✨ GlowUp 자기관리")
    st.subheader("매일 조금씩 예뻐지는 나를 위한 공간")
    
    st.image("https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&q=80&w=800", 
             caption="나를 돌보는 온전한 시간에 집중해 보세요.")
    
    st.write("")
    st.markdown("#### 💌 오늘의 뷰티 동기부여 메시지")
    
    # 세션 상태를 활용해 새로고침 전까지 문구 유지 및 랜덤 버튼 구현
    if 'quote' not in st.session_state:
        st.session_state.quote = random.choice(MOTIVATION_QUOTES)
        
    st.info(st.session_state.quote)
    
    if st.button("다른 응원 문구 보기"):
        st.session_state.quote = random.choice(MOTIVATION_QUOTES)
        st.rerun()

# 2. 피부 케어 화면
elif menu == "🧴 맞춤형 피부 케어":
    st.title("🧴 맞춤형 피부 케어 가이드")
    st.write("자신의 피부 타입을 선택하면 아침/저녁에 꼭 해야 할 핵심 케어 방법을 알려드립니다.")
    
    skin_type = st.selectbox(
        "당신의 피부 타입은 무엇인가요?",
        list(SKIN_CARE_DATA.keys())
    )
    
    try:
        data = SKIN_CARE_DATA[skin_type]
        
        st.markdown(f"### ☀️ 아침 루틴 ({skin_type.split()[0]})")
        for i, step in enumerate(data["morning"], 1):
            st.markdown(f"<div class='routine-box'><b>Step {i}.</b> {step}</div>", unsafe_allow_html=True)
            
        st.markdown(f"### 🌙 저녁 루틴 ({skin_type.split()[0]})")
        for i, step in enumerate(data["night"], 1):
            st.markdown(f"<div class='routine-box'><b>Step {i}.</b> {step}</div>", unsafe_allow_html=True)
            
        st.markdown("### 💡 전문가의 한 줄 꿀팁")
        st.warning(data["tip"])
        
    except Exception as e:
        st.error("데이터를 불러오는 중 문제가 발생했습니다. 관리자에게 문의하세요.")

# 3. 메이크업 화면
elif menu == "💄 맞춤형 메이크업":
    st.title("💄 맞춤형 메이크업 가이드")
    st.write("상황과 목적에 꼭 맞는 메이크업 연출법을 단계별로 쉽게 따라 해 보세요.")
    
    makeup_style = st.selectbox(
        "오늘 어떤 스타일의 메이크업이 필요하신가요?",
        list(MAKEUP_DATA.keys())
    )
    
    try:
        steps = MAKEUP_DATA[makeup_style]
        st.markdown(f"### 📌 {makeup_style} 프로세스")
        
        for step in steps:
            st.write(step)
            
        st.write("")
        st.success("💡 Tip: 메이크업 전 기초를 탄탄히 다져야 화장이 들뜨지 않고 오래 유지됩니다!")
        
    except Exception as e:
        st.error("메이크업 가이드를 불러오는 중 오류가 발생했습니다.")

# 4. 체크리스트 화면 (사용자 반응형 기능)
elif menu == "📅 나의 가꾸기 체크리스트":
    st.title("📅 나의 가꾸기 체크리스트")
    st.write("오늘 실천한 외모 관리 행동들을 체크하며 성취감을 느껴보세요!")
    
    tasks = ["물 1.5L 이상 마시기", "외출 전 자외선 차단제 바르기", "얼굴 손으로 만지지 않기", "저녁에 꼼꼼히 세안하기", "가벼운 스트레칭 또는 림프 마사지"]
    
    completed_count = 0
    st.markdown("### 📝 오늘의 체크 목록")
    for task in tasks:
        if st.checkbox(task, key=f"check_{task}"):
            completed_count += 1
            
    # 성취도 계산 및 시각화
    total_tasks = len(tasks)
    progress = completed_count / total_tasks
    
    st.markdown("### 📊 오늘의 가꾸기 성취도")
    st.progress(progress)
    
    if completed_count == total_tasks:
        st.balloons()
        st.success("🎉 대단해요! 오늘 정한 자신과의 외모 관리 약속을 완벽하게 지키셨습니다!")
    elif completed_count > 0:
        st.info(f"총 {total_tasks}개 중 {completed_count}개 완료! 잘하고 계십니다. 조금만 더 힘내세요! 🔥")
    else:
        st.write("아직 체크된 항목이 없습니다. 하나씩 실천해 볼까요?")

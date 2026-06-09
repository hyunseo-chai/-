import streamlit as st
import google.generativeai as genai
import random

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="GlowAI - 약속 맞춤형 AI 외모 관리",
    page_icon="✨",
    layout="centered"
)

# 2. 동기부여 문구 데이터
MOTIVATION_QUOTES = [
    "오늘의 정성스러운 관리는 내일의 눈부신 자신감이 됩니다. ✨",
    "나를 가꾸고 아끼는 시간은 삶을 사랑하는 가장 아름다운 방법입니다. 🤍",
    "가장 완벽한 메이크업은 당당하게 미소 짓는 당신의 얼굴입니다. 🥰",
    "피부는 거짓말을 하지 않습니다. 오늘 밤 5분의 케어가 내일의 차이를 만듭니다. 🌿"
]

# 3. 안전한 API 키 로드 (에러 방지 가드)
api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    # 로컬 환경 등 secrets 파일이 아예 없을 때 에러 크래시 방지
    pass

# --- 메인 화면 레이아웃 ---
st.title("✨ GlowAI : 약속 맞춤형 자기관리")
st.markdown("##### 나의 약속과 얼굴 특징에 딱 맞는 메이크업 & 케어 비법을 AI 뷰티 매니저가 설계해 드립니다.")

# 사이드바 구성
st.sidebar.title("🌿 My Care Room")
if "quote" not in st.session_state:
    st.session_state.quote = random.choice(MOTIVATION_QUOTES)

st.sidebar.info(f"💡 **오늘의 다짐**\n\n{st.session_state.quote}")
if st.sidebar.button("다른 문구 보기"):
    st.session_state.quote = random.choice(MOTIVATION_QUOTES)
    st.rerun() # 안전한 최신 리프레시 방식 적용

st.sidebar.markdown("---")
st.sidebar.caption("GlowAI v1.2.0 | Powered by gemini-2.5-flash-lite")

# 탭 레이아웃 분리
tab1, tab2 = st.tabs(["🔮 AI 맞춤 뷰티 컨설팅", "📅 데일리 가꾸기 체크리스트"])

# --- Tab 1: AI 컨설팅 기능 ---
with tab1:
    st.markdown("### 📝 나의 상황 입력하기")
    
    col1, col2 = st.columns(2)
    with col1:
        appointment = st.selectbox(
            "1. 어떤 종류의 약속인가요?",
            ["중요한 면접 및 비즈니스 미팅", "설레는 소개팅 및 데이트", "트렌디하고 힙한 파티/클럽 모임", "편안한 친구들과의 캐주얼 모임", "결혼식 하객 참석", "증명/프로필 사진 촬영"]
        )
        skin_type = st.selectbox(
            "2. 현재 내 피부 타입은?",
            ["지성 (유분이 많고 화장이 잘 지워짐)", "건성 (푸석하고 각질이 잘 뜨며 당김)", "복합성 (T존은 번들, U존은 건조)", "민감성 (쉽게 붉어지고 트러블 발생)"]
        )
    with col2:
        face_shape = st.selectbox(
            "3. 나의 얼굴형과 고민은?",
            ["둥근형 (부어 보이고 턱선 음영 필요)", "각진형/각진턱 (부드러운 인상 연출 필요)", "계란형 (장점을 살리는 입체감 필요)", "긴 얼굴형 (중안부를 짧아 보이게 연출 필요)"]
        )

    st.markdown("---")
    
    # 비상용 API Key 수동 입력창 가드
    if not api_key:
        st.warning("⚠️ Streamlit Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
        user_key = st.text_input("테스트를 위해 본인의 Gemini API Key를 입력하시면 즉시 실행 가능합니다:", type="password")
        if user_key:
            api_key = user_key

    # 가이드 생성 버튼
    if st.button("✨ 나만을 위한 AI 맞춤 가이드 가져오기"):
        if not api_key or not api_key.strip():
            st.error("🔒 API Key가 누락되었습니다. 아래 설정 방법을 참고하여 Secrets를 등록하거나 위 입력창에 넣어주세요.")
        else:
            with st.spinner("AI 뷰티 매니저가 최적의 관리법을 분석하고 있습니다..."):
                try:
                    # 공식 Google Generative AI 설정 및 호출
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-2.5-flash-lite")
                    
                    prompt = f"""
                    당신은 전문 퍼스널 쇼퍼이자 뷰티 컨설턴트입니다. 아래 조건에 맞는 맞춤형 외모 관리 가이드를 작성해주세요.
                    
                    [사용자 조건]
                    - 예정된 약속: {appointment}
                    - 피부 타입: {skin_type}
                    - 얼굴형 및 특징: {face_shape}
                    
                    [작성 규칙]
                    - 반드시 한국어로 친절하고 따뜻한 어조로 작성하세요.
                    - 아래 3가지 섹션을 명확히 구분하여 마크다운 문법과 이모지를 곁들여 설명해주세요.
                      1. 🧴 [내 피부에 맞는 사전/사후 케어 방법] (약속 전날이나 화장 전 무너지지 않는 수분/진정 케어법)
                      2. 💄 [약속과 얼굴형에 어울리는 추천 메이크업 가이드] (색조 분위기, 얼굴형 보완 기법 포함)
                      3. 💡 [오늘의 핵심 원포인트 외모 꿀팁]
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.markdown("### 💝 AI가 설계한 맞춤 가이드 리포트")
                    # 안전하게 일반 마크다운 형태로 렌더링하여 HTML 충돌 에러 원천 차단
                    st.info(response.text)
                    
                except Exception as e:
                    st.error(f"❌ AI 호출 중 에러가 발생했습니다: {str(e)}")
                    st.info("💡 해결 방법: 발급받은 API 키가 유효한지 확인하거나 Secrets 등록 형식을 점검해 주세요.")

# --- Tab 2: 루틴 체크리스트 기능 ---
with tab2:
    st.markdown("### 📅 오늘 하루 외모 가꾸기 약속")
    st.write("기초가 튼튼해야 메이크업도 빛납니다. 오늘 실천한 루틴들을 체크해 보세요!")
    
    routines = [
        "💧 하루 물 1.5L 이상 섭취하기",
        "☀️ 외출 전 자외선 차단제(선크림) 꼼꼼히 바르기",
        "🚫 습관적으로 얼굴 손으로 만지지 않기",
        "🧼 저녁 퇴근 후 귀찮아도 꼼꼼하게 이중 세안하기",
        "🧴 수분 크림 충분히 발라 피부 장벽 지키기"
    ]
    
    score = 0
    for i, routine in enumerate(routines):
        if st.checkbox(routine, key=f"routine_{i}"):
            score += 1
            
    total = len(routines)
    progress = score / total
    
    st.write("")
    st.markdown(f"**현재 나의 실천도 : {score} / {total}**")
    st.progress(progress)
    
    if score == total:
        st.balloons()
        st.success("🎉 대단해요! 오늘 정한 자신과의 외모 관리 약속을 완벽하게 지키셨습니다!")
    elif score > 0:
        st.info("정말 잘하고 계시네요! 조금만 더 채워볼까요? 🔥")

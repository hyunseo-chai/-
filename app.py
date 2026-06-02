import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 설정
st.set_page_config(page_title="달콤살벌 연애상담소", page_icon="💖", layout="centered")
st.title("💖 달콤살벌 연애상담소")
st.write("연애 때문에 고민이신가요? 속 시원하게 털어놓으세요. 당신의 연애 코치가 되어드릴게요!")

# Streamlit Secrets에서 API 키 불러오기
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("⚠️ Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 설정 후 다시 시도해주세요.")
    st.stop()

# GenAI 클라이언트 초기화
@st.cache_resource
def get_genai_client(api_key):
    return genai.Client(api_key=api_key)

client = get_genai_client(gemini_api_key)

# 챗봇의 페르소나(역할) 설정
SYSTEM_INSTRUCTION = """
당신은 공감 능력이 뛰어나면서도 때로는 뼈를 때리는 현실적인 조언을 해주는 전문 연애 상담사입니다.
사용자의 연애 고민(짝사랑, 이별, 권태기, 썸 등)을 듣고 친구처럼 다정하게 공감해주되, 
상황을 객관적으로 파악할 수 있도록 솔직하고 현명한 해결책을 제시해주세요.
답변은 친근한 반말이나 존댓말을 적절히 섞어 따뜻하고 위트 있는 톤앤매너를 유지하세요.
"""

# 세션 상태(Session State)로 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 채팅 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if user_input := st.chat_input("연애 고민을 입력하세요... (예: 썸남이 선톡을 안 해요)"):
    # 사용자 메시지 화면에 표시 및 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 챗봇 답변 생성 및 표시
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            with st.spinner("연애 코치가 고민을 분석 중입니다... 💭"):
                # gemini-2.5-flash-lite 모델 호출
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7, # 적절한 창의성과 공감 능력 유지
                    )
                )
                
                ai_response = response.text
                message_placeholder.markdown(ai_response)
                
                # AI 메시지 기록 저장
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
        except APIError as e:
            # Gemini API 관련 오류 처리
            error_msg = f"❌ Gemini API 오류가 발생했습니다: {e.message}"
            message_placeholder.error(error_msg)
        except Exception as e:
            # 기타 일반 오류 처리
            error_msg = f"⚠️ 예기치 못한 오류가 발생했습니다: {str(e)}"
            message_placeholder.error(error_msg)

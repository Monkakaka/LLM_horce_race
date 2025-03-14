import streamlit as st
from streamlit_chat import message
import openai_api
import random

st.title("🏇🏇경마 시뮬레이션🏇🏇")

def generate_horses():
    horses = [
        "특별한 한주", "동해 제왕", "황금 배", "벚꽃 박진왕", "금빛 도시",
        "푸른 하늘", "화창한 봄", "눈의 미인", "쌀 목욕"
    ]
    random.shuffle(horses)  # 인기 순위 랜덤 설정
    return horses

# 우승 확률 계산 (기본 확률 + 랜덤 변동)
def calculate_win_probabilities(horses):
    base_probabilities = [30, 28, 25, 23, 20, 16, 13, 10, 8]  # 기본 확률
    probability_variation = [random.uniform(-8, 15) for _ in range(len(horses))]  # -8% ~ +15% 변동

    # 변동된 확률 계산
    adjusted_probabilities = [
        max(base_probabilities[i] + probability_variation[i], 1)  # 최소 1% 보장
        for i in range(len(horses))
    ]

    total = sum(adjusted_probabilities)  # 정규화
    probabilities = {horse: adjusted_probabilities[i] / total for i, horse in enumerate(horses)}
    return probabilities

# 전체 순위 결정 함수
def calculate_rankings(probabilities):
    horses = list(probabilities.keys())
    probs = list(probabilities.values())
    
    # 각 말에 대한 우승 확률을 기준으로 내림차순으로 정렬하여 순위 매기기
    ranking = sorted(horses, key=lambda horse: probabilities[horse], reverse=True)
    
    return ranking


# 메시지 리스트 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "race_bot", "content": "안녕하세요 경마장은 처음 이신가요?"}]

if "race_number" not in st.session_state:
    st.session_state.race_number = 0

if "race" not in st.session_state:
    st.session_state.race = "아직 경기 정보가 없습니다."

# 이전 채팅 메시지 출력
for chat in st.session_state.messages:
    is_user = chat["role"] == "user"  # 사용자인지 여부 확인
    message(chat["content"], is_user=is_user)  # 메시지 출력

input_message = st.chat_input(placeholder="메세지를 입력하세요")

st.sidebar.title("🏇 새 경기 시작하기")
if st.sidebar.button("경기 시작"):
    st.session_state.race_number +=1
    horses = generate_horses()
    probabilities = calculate_win_probabilities(horses)
    ranking = calculate_rankings(probabilities)
    race_info = f"{st.session_state.race_number}번째 경기 정보입니다. 인기 순위:{horses}, 레이스 랭킹:{ranking}"
    st.session_state.race = race_info
    # input_message = "새 경기 시작!"   # 왜튕김?왜튕김?왜튕김?왜튕김?왜튕김?왜튕김?
    print(race_info)

st.sidebar.write(f"{st.session_state.race_number}번째 경기 진행 중")

if input_message:
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": input_message})
    message(input_message, is_user=True)

    conversation_history = st.session_state.messages[-10:]

    combined_message = f"이전 대화내용:\n{conversation_history}\n이번 사용자 입력: {input_message}"

    # GPT 응답 생성
    output_message = openai_api.ask_gpt(combined_message)

    # 챗봇 응답 저장
    st.session_state.messages.append({"role": "race_bot", "content": output_message})
    message(output_message, is_user=False)





# 사이드바에 메시지 지우기 버튼 추가
st.sidebar.title("🗑️ 대화 내역 초기화")
if st.sidebar.button("초기화"):
    st.session_state.messages = []  # 메시지 내역 초기화
    st.session_state.race = []
    st.session_state.race_number = 0
    st.sidebar.success("초기화 되었습니다.")  # 메시지 지워졌다는 알림 표시


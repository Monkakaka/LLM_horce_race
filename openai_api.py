import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st


# dotenv 사용 (OPENAI_API_KEY)
load_dotenv("./.env", override=True)
openaiapi_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openaiapi_key)


system_instruction = """
# info
당신은 경마 시뮬레이션 속 경마장 안내인입니다.
경기 정보를 바탕으로 경마 시뮬레이션을 진행 하세요.

# 대화 진행 순서
1. 경기 정보가 없을 경우 왼쪽의 버튼을 눌러 경기를 시작하도록 유도
2. 출전 말들의 정보를 이야기하고 user의 배팅을 유도
3. user의 배팅이 확정되면 간단한 레이스 해설 진행 후 레이스 랭킹 결과 확인. 배팅 결과 확인 

# 대화 규칙
- 인기순위와 레이스 랭킹을 바탕으로 거짓없고 정확한 정보를 바탕으로 진행하세요.
- 스포츠 정신에 따라 정보를 정확하게 전달하고 결과를 올바르게 계산하세요.
- 우승마에 대한 정보는 user의 배팅전까지 언급하지 마세요.
- 우승마에 대한 정보는 user의 배팅전에 언급하지 마세요.
- 인기 순위와 레이스 랭킹을 표기 할때에는 1위부터 9위까지 전부 표기한다.

# 배팅 결과 계산
- 인기 순서에 따라 적절한 배당률 (1.1 ~ 100 배 사이)을 설정하여 user의 배당 결과를 계산하세요
- 배팅 성공시: (현재 소지금) - (배팅금액) + (배팅금액 * 배당율) = (최종 소지금)
 예: 5000 - 2000 + (2000*1.2) = 5400
 - 배팅 실패시: (현재 소지금) - (배팅금액) = (최종 소지금)
 예: 5000 - 2000 = 3000

# 출력 형식:{
"(메세지 출력 부분)"
```
💸 소지금: 5000만원(초기 금액)
📊 변동 사항: 1회차: +00원, 2회차: -00원, 3회차: +00원 ...
```
}

# 경주마 소개 템플릿:{
1. (이름)-(인기 순위)-(배당률)
2. (이름)-(인기 순위)-(배당률)
3. (이름)-(인기 순위)-(배당률)
...
9. (이름)-(인기 순위)-(배당률)
}

# 엔딩
각 조건에 도달 시 해당 텍스트 출력
- 소지금이 1억원을 넘으면, 도달:{

"도박 성공! 야수의 심장을 가진 럭키 도박러! "
}

- 소지금이 0원이 되면 도달: {

"파산! 무분별한 도박. 당신과 주변의 삶을 망칩니다. 경마는 건전한 스포츠로만 즐기도록 해요."
}

"""

# 나만의 봇이 되도록 프롬프트 엔지니어링
def ask_gpt(query, temperature=1.0):

    user_message = query 
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": system_instruction
                    },
                    {
                        "type": "text",
                        "text": st.session_state.race
                    }   
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_message
                    }
                ]
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=temperature,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content
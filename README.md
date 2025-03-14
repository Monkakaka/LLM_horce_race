# 🏇 LLM 기반 경마 시뮬레이션 게임

<br>

## 00. 뭐 하는 프로젝트인가?
SKN AI캠프 9기 LLM 기반 미니게임 만들기 프로젝트로 제작된 경마 시뮬레이션
LLM 기반 챗봇을 통해 5천만원의 자본금을 경마로 2배로 늘리는 것이 목표입니다.

## 01. How to use

- .env
  시작 전 .env파일을 생성하여 openai api key를 입력하세요.
```
OPENAI_API_KEY = sk-xxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
- 콘솔에서 실행하세요
  
```
streamlit run app.py
```

## 02. How to play
![Image](https://github.com/user-attachments/assets/71cafb90-9b23-481d-9fe7-85118132e354)

- 챗봇 형식의 대화창을 통해 진행 됩니다.
- 새 레이스 시작시 좌측 상단의 버튼을 누른 후 대화를 진행하세요.
- 초기화 버튼으로 대화내용을 지울 수 있습니다.
- 경기 정보를 받아온 후 대화를 진행하면 챗봇이 경기 정보를 안내 해줍니다.
- 인기순위에 따라 우승 확률이 높고 인기순위가 낮을수록 배당이 높습니다. 우승마를 추측해서 맞춰 보세요!

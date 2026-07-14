from dotenv import load_dotenv
import os
import anthropic
import streamlit as st

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.title("나의 챗봇")

# 이전 대화 기록을 저장할 공간 (새로고침하기 전까지 유지됨)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 지금까지의 대화 내용을 화면에 그리기
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 하단에 입력창 표시
question = st.chat_input("질문을 입력하세요")

if question:
    # 사용자 메시지 저장 + 화면에 표시
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    # AI 응답 요청
    with st.chat_message("assistant"):
        with st.spinner("답변 생성 중..."):
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            answer = response.content[0].text
            st.write(answer)

    # AI 응답도 기록에 저장
    st.session_state.messages.append({"role": "assistant", "content": answer})
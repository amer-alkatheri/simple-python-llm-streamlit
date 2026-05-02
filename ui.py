import streamlit as st
from main import main_ui

icons = {"assistant": "🤖", "user": "👤"}

st.set_page_config(page_title="AI Chat Demo", page_icon="🤖")
st.title("Chat Demo", text_alignment="center")

# 1. Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. When you need to use a tool, use the built-in tool-calling feature. Do not write the function call yourself in text."
        }
    ]


# 2. Display existing chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]): 
            st.markdown(message["content"])

# 3. Handle User Input
if prompt := st.chat_input():
    # Show user message
    st.chat_message("user").markdown(prompt)

    # Update History
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # 4. CALL THE EXTERNAL FUNCTION
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            answer = main_ui(st.session_state.messages)
            st.markdown(answer)

            # Update History with Assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })
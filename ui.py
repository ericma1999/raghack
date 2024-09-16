import streamlit as st
from ai import get_response

st.set_page_config(page_title="LLM Chat App", page_icon="🤖")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


def get_model_response(user_input):
    model_response = get_response(user_input, st.session_state["chat_history"])
    # return f"AI: I received your message: {user_input} and my response is {model_response.choices[0].message.content}"
    return f"AI: {model_response.choices[0].message.content}"

def send_message():
    user_input = st.session_state["user_input"]

    if user_input:
        st.session_state["chat_history"].append(f"User: {user_input}")

        model_response = get_model_response(user_input)
        st.session_state["chat_history"].append(model_response)

        st.session_state["user_input"] = ""


st.title("🏠 Property-LLM Application")

st.write("A simple chat LLM for searching properties in London")

container = st.container(height=500)
for message in st.session_state["chat_history"]:
    container.write(message)

st.text_input("Enter your message:", key="user_input", on_change=send_message)

if st.button("Clear Chat History"):
    st.session_state["chat_history"] = []
    st.rerun()  # Refresh the app to show cleared chat

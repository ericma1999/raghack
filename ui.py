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


col1, col2 = st.columns([8, 2])


with col1:

    container = st.container(height=500)
    for message in st.session_state["chat_history"]:
        container.write(message)

    st.text_input("Enter your message:", key="user_input",
                  on_change=send_message)

    if st.button("Clear Chat History"):
        st.session_state["chat_history"] = []
        st.rerun()  # Refresh the app to show cleared chat

with col2:
    option = st.selectbox(
        "RAG options", ("Basic", "AI Search", "AI Vector Search"))

    content = {
        "Basic": "Basic option loads the csv file and insert the content into the context of the user input.",
        "AI Search": "Uses the Azure AI Search on the content that is stored in the blob storage of the Azure service. This does not perform the embeddings.",
        "AI Vector Search": "Uses the Azure AI Search and the embedder from the Azure Open AI service, that performs the vector embeddings of the properties information content.",
    }

    st.write(content[option])

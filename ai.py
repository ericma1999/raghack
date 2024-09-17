from auth import model_chat
from rag_client import CSVRagClient, AISearchRagClient
from const import SYSTEM_MESSAGE




def format_history(chat_history):
    output = []
    counter = 0
    # print(type(chat_history[0]))
    for chat in chat_history:
        chat_content = " ".join(chat.split(" ")[1::])
        format_chat = None
        if counter % 2 == 0:
            format_chat = {"role": "user", "content": chat_content}
        else:
            format_chat = {"role": "assistant", "content": chat_content}
        output.append(format_chat)
    return output


def get_response(user_input, history):
    rag_client = AISearchRagClient()
    rag_response = rag_client.get_rag(user_input)
    current_history = format_history(history)
    print(rag_response)

    current_history[-1]["content"] = (
        current_history[-1]["content"] + "\nSources: " + rag_response
    )

    response = model_chat(
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
        ]
        + current_history,
    )

    return response

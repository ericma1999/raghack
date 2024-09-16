from auth import model_chat
from rag_client import CSVRagClient, AISearchRagClient

# print(f"Found {len(matches)} matches:")
# print(matches_table)
PROPERTY_FORMAT = """
Overview: [x] bedrooms, [x] bathrooms, [x] tenants, [location] 
Description: [summarised description]
Price and Bills: [x] deposit, [x] rent per month and bills [included / not included]
Tenant Preference: The property is [student friendly / student only] [families allowed or not allowed] [smokers allowed / not allowed]
Availability: [from date] and [minimum tenancy]
Features: [summary of other property features]
URL: [url (must only be from dataset openrent url)]
"""


SYSTEM_MESSAGE = f"""
You are a helpful assistant that answers questions about rental properties.
You must use the data set to answer the questions, you should not provide any info that is not in the provided sources.
Make sure the response include the exact property title, rent, deposit and the factual requirements are the same as the source.
Use the following template: {PROPERTY_FORMAT}
"""


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
            # {"role": "user", "content": user_input + "\nSources: " + rag_response},
        ]
        + current_history,
    )

    return response

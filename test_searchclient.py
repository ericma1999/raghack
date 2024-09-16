from auth import search_client

results = search_client.search(search_text="a studio in E1")


def generate_markdown(keys, result=None):
    if result is None:
        return " | ".join(keys)

    return "| ".join(["" if result[key] is None else result[key] for key in keys])


def format_retrieval_content(results):

    keys = None
    output = ""
    for index, result in enumerate(results):
        if index == 5:
            break
        if keys is None:
            keys = [*result]
            keys = [item for item in keys if not "@" in item]
            output += generate_markdown(keys)
            output += "\n"

        output += generate_markdown(keys, result)
        output += "\n"

    return output


output = format_retrieval_content(results)


print(output)

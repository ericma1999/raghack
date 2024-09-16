import csv
from abc import ABC, abstractmethod

from auth import search_client


class RagClient(ABC):

    @abstractmethod
    def get_rag(self, user_input):
        """RAG implementation"""


class CSVRagClient(RagClient):

    def open_file(self):
        with open("properties_info_full_with_id.csv") as file:
            reader = csv.reader(file)
            rows = list(reader)
            return rows

    def get_rag(self, user_input):
        rows = self.open_file()

        normalized_message = (
            user_input.lower().replace("?", "").replace("(", " ").replace(")", " ")
        )

        words = normalized_message.split()
        matches = []
        limit = 3
        counter = 1
        for row in rows[1:]:
            if counter == limit:
                break
            if any(word in row[0].lower().split() for word in words) or any(
                word in row[5].lower().split() for word in words
            ):
                matches.append(row)
                counter += 1

            matches_table = (
                " | ".join(rows[0])
                + "\n"
                + " | ".join(" --- " for _ in range(len(rows[0])))
                + "\n"
            )
            matches_table += "\n".join(" | ".join(row) for row in matches)

        return matches_table


class AISearchRagClient(RagClient):

    def generate_markdown(self, keys, result=None):
        if result is None:
            return " | ".join(keys)

        return "| ".join(["" if result[key] is None else result[key] for key in keys])

    def format_retrieval_content(self, results):
        """Format the content in markdown separated by bar"""

        keys = None
        output = ""
        for index, result in enumerate(results):
            if index == 5:
                break
            if keys is None:
                keys = [*result]
                keys = [item for item in keys if not "@" in item]
                output += self.generate_markdown(keys)
                output += "\n"

            output += self.generate_markdown(keys, result)
            output += "\n"

        return output

    def get_rag(self, user_input):
        results = search_client.search(search_text=user_input)

        return self.format_retrieval_content(results)


class VectorAISearchRagClient(RagClient):

    def get_rag(self, user_input):
        return "something"

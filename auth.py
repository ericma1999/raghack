import os
from functools import partial

import azure.identity
import openai
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from dotenv import load_dotenv

load_dotenv(override=True)


# Models
model_client = None
API_HOST = os.getenv("API_HOST")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    model_client = openai.AzureOpenAI(
        api_version=os.getenv("AZURE_OPENAI_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_ad_token_provider=token_provider,
    )
    MODEL_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

elif API_HOST == "ollama":
    model_client = openai.OpenAI(
        base_url=os.getenv("OLLAMA_ENDPOINT"),
        api_key="nokeyneeded",
    )
    MODEL_NAME = os.getenv("OLLAMA_MODEL")

elif API_HOST == "github":
    model_client = openai.OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN"),
    )
    MODEL_NAME = os.getenv("GITHUB_MODEL")

else:
    model_client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))
    MODEL_NAME = os.getenv("OPENAI_MODEL")


model_chat = partial(
    model_client.chat.completions.create, model=MODEL_NAME, temperature=0.3
)


# SearchClient


service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
key = os.environ["AZURE_SEARCH_API_KEY"]

search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))


# VectorSearch
### Model is the azure openai deployment name

def generate_embedding(text, model):

    embeddings = model_client.embeddings.create(model=model, input=text)

    return embeddings.data[0].embedding


def generate_vector_query(query, model):

    vector_query = VectorizedQuery(
        vector=generate_embedding(query, model),
        k_nearest_neighbors=5,
        fields="content_vector",
    )
    return vector_query

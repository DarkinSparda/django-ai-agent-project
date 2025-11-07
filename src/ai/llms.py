from django.conf import settings
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_perplexity import ChatPerplexity
###
api = settings.PPLX_API_KEY
###
def get_ai_api_key():

    return api


def get_ai_model(model="sonar-pro"):

    return ChatPerplexity(
        model=model,
        temperature=0,
        max_retries=2,
        api_key=api,

    )

# def get_ai_model(model="gpt-5-mini"):

#     return ChatOpenAI(
#         model=model,
#         temperature=0,
#         max_retries=2,
#         api_key=settings.OPENAI_API_KEY,

#     )
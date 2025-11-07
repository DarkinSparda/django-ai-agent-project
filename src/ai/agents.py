from langchain.agents import create_agent

from ai.tools import document_tools, movie_tools
from ai.llms import get_ai_model

def get_document_agent(checkpointer=None):
    model=get_ai_model()

    agent = create_agent(
        name="document-agent",
        model=model,
        tools=document_tools,
        system_prompt=
        """You are a helpful AI assistant. You can help with:
        1. Managing user's documents (list, create, view documents)
        2. Answering general knowledge questions about movies, science, history, etc.
        3. Providing summaries, explanations, and information on any topic
        
        Use your knowledge to answer questions when they don't require document access.
        Use the document tools when the user asks about their documents.
        if you had to update or query database then do so""",
        checkpointer=checkpointer
    )
    
    return agent

def get_movies_agent(checkpointer=None):
    model = get_ai_model()

    agent = create_agent(
        name="movies-agent",
        model=model,
        tools=movie_tools,
        system_prompt=
        """You are a specialized movie assistant AI. You can help with:
        1. Searching for movies by title, genre, year, or other criteria
        2. Getting detailed movie information (plot, cast, ratings, reviews)
        3. Providing movie recommendations based on preferences
        4. Comparing movies and providing analysis
        
        Use the movie tools to access up-to-date movie database information.
        Provide accurate, helpful responses about films and entertainment.""",
        checkpointer=checkpointer
    )

    return agent
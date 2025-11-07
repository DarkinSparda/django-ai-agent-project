from langgraph_supervisor import create_supervisor
from .agents import get_document_agent, get_movies_agent, get_ai_model

def get_supervisor(checkpointer=None):
    # Initialize agents with checkpointer
    agents = [
        get_document_agent(checkpointer),
        get_movies_agent(checkpointer)
    ]
    model = get_ai_model()
    
    return create_supervisor(
        agents=agents,
        model=model,
        prompt="""You are a supervisor AI that coordinates between specialized agents to help users.

Available agents:
- document-agent: Handles document management (list, create, view documents) and database operations
- movies-agent: Provides movie information, searches, recommendations, and entertainment analysis

Your role:
1. Analyze user requests to determine which agent(s) can best help
2. Route requests to the appropriate agent based on the task
3. If a request involves documents/files, use the document-agent
4. If a request involves movies/entertainment, use the movies-agent
5. For general questions that don't require specialized tools, you can handle them directly
6. Coordinate between agents if a task requires multiple specialties

Always choose the most appropriate agent for the user's specific needs."""    
    ).compile(checkpointer=checkpointer)
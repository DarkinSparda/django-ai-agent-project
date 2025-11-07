"""
AI Output Prettifier Package
Simple, human-friendly output formatting for AI responses
"""

from IPython.display import display, Markdown, HTML


def pretty_print(text_or_response):
    """
    Display text/response with nice markdown formatting
    
    Args:
        text_or_response: Either a dict with 'messages' or plain text
    """
    if isinstance(text_or_response, dict) and 'messages' in text_or_response:
        text = text_or_response['messages'][-1].content
    else:
        text = text_or_response
    
    display(Markdown(text))


def print_json(data):
    """Pretty print JSON data"""
    import json
    text = json.dumps(data, indent=2)
    display(Markdown(f"```json\n{text}\n```"))


def print_code(code, language="python"):
    """Pretty print code with syntax highlighting"""
    display(Markdown(f"```{language}\n{code}\n```"))

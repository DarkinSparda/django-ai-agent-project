import json
import ast
import re
from IPython.display import display, HTML

def _serialize(obj):
    """Convert non-JSON-serializable objects to dict representation"""
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return str(obj)

def _colorize_json(json_str):
    """Apply syntax highlighting to JSON string with typical JSON colors"""
    lines = json_str.split('\n')
    colored_lines = []

    for line in lines:
        # booleans/null → orange
        line = re.sub(r'\b(true|false|null)\b', r'<span style="color:#FF8C00;">\1</span>', line)
        # keys → blue
        line = re.sub(r'"([^"]+)"\s*:', lambda m: f'<span style="color:#0066cc;">{m.group(0)}</span>', line)
        # string values → green
        line = re.sub(r':\s*"([^"\\]|\\.)*"', lambda m: f': <span style="color:#228B22;">{m.group(0)[2:].lstrip()}</span>', line)
        # numbers → red
        line = re.sub(r':\s*(-?\d+\.?\d*)', lambda m: f': <span style="color:#D32F2F;">{m.group(1)}</span>', line)
        colored_lines.append(line)

    return '\n'.join(colored_lines)

def pprint(data):
    """
    Jupyter-friendly prettifier:
    - Pretty JSON/dict formatting with color
    - Converts escaped \\n or literal newlines into real ones
    - Handles text safely for HTML
    """
    def _escape_html(s: str) -> str:
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # Try to pretty print as JSON first
    try:
        formatted = json.dumps(data, indent=2, ensure_ascii=False, default=_serialize)
        formatted = _escape_html(formatted)
        formatted = _colorize_json(formatted)
        display(HTML(f"<pre style='font-size:13px;line-height:1.4;font-family:Courier,monospace;overflow-x:auto;margin:0;'>{formatted}</pre>"))
        return
    except Exception:
        pass

    # Handle string input
    if isinstance(data, str):
        # Attempt to interpret it as JSON or Python literal
        try:
            parsed = json.loads(data)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False, default=_serialize)
            formatted = _escape_html(formatted)
            formatted = _colorize_json(formatted)
            display(HTML(f"<pre style='font-size:13px;line-height:1.4;font-family:Courier,monospace;overflow-x:auto;margin:0;'>{formatted}</pre>"))
            return
        except Exception:
            pass
        try:
            parsed = ast.literal_eval(data)
            if isinstance(parsed, (dict, list)):
                formatted = json.dumps(parsed, indent=2, ensure_ascii=False, default=_serialize)
                formatted = _escape_html(formatted)
                formatted = _colorize_json(formatted)
                display(HTML(f"<pre style='font-size:13px;line-height:1.4;font-family:Courier,monospace;overflow-x:auto;margin:0;'>{formatted}</pre>"))
                return
        except Exception:
            pass

        # ---- core fix: handle both escaped and literal \n ----
        text = data.encode('utf-8').decode('unicode_escape')  # converts \\n to real \n
        text = text.replace('\r', '').strip()
        text = _escape_html(text)

        display(HTML(
            f"<pre style='font-size:13px;line-height:1.4;font-family:Courier,monospace;white-space:pre-wrap;overflow-x:auto;margin:0;'>{text}</pre>"
        ))
        return

    # Default fallback for other data types
    text = _escape_html(str(data))
    display(HTML(
        f"<pre style='font-size:13px;line-height:1.4;font-family:Courier,monospace;white-space:pre-wrap;overflow-x:auto;margin:0;'>{text}</pre>"
    ))

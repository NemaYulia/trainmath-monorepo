from django import template
import re

register = template.Library()


def _prettify_expression(text: str) -> str:
    """Convert raw LaTeX-ish or sympy string to a concise, user-friendly form.

    Examples:
    - "\\left(2 a - 3 b\\right)^{2}" -> "(2a - 3b)^2"
    - "a * b + 2 * a^2" -> "a·b + 2a^2"
    """
    if not text:
        return ""

    s = str(text)
    # Remove LaTeX left/right wrappers
    s = s.replace("\\left", "").replace("\\right", "")
    # Replace LaTeX power ^{k} with ^k
    s = re.sub(r"\^\{([^}]+)\}", r"^\1", s)
    # Remove spaces around single-letter variables like "2 a" -> "2a"
    s = re.sub(r"(\d)\s+([a-zA-Z])", r"\1\2", s)
    s = re.sub(r"([a-zA-Z])\s+([a-zA-Z])", r"\1\2", s)
    # Multiplication: replace " * " with middle dot
    s = s.replace(" * ", "·")
    # Clean multiple spaces
    s = re.sub(r"\s+", " ", s).strip()
    return s


@register.filter(name="pretty_expr")
def pretty_expr(value: str) -> str:
    return _prettify_expression(value)


@register.filter(name="minutes")
def minutes(ms_value) -> str:
    try:
        ms = float(ms_value)
        total_seconds = ms / 1000.0
        mins = int(total_seconds // 60)
        secs = int(round(total_seconds % 60))
        if mins > 0:
            return f"{mins}m {secs}s"
        return f"{secs}s"
    except Exception:
        return str(ms_value)



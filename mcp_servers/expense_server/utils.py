from functools import wraps


def validate_positive(value: float, field_name: str):
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative.")


def safe_tool(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return {
                "success": True,
                "data": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    return wrapper

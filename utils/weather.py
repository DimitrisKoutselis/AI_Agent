def get_current_weather(location: str, unit: str = "celsius") -> str:
    # This is a mock function. In a real scenario, you'd call an actual weather API.
    return f"The current weather in {location} is 22°{'C' if unit == 'celsius' else 'F'}"
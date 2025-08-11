import google.generativeai as genai

def gemini_generate(prompt: str, model_name: str = 'gemini-pro') -> str:
    """
    Utility to call Gemini LLM for text generation.
    """
    genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Replace with your Gemini API key or load from env
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else str(response)

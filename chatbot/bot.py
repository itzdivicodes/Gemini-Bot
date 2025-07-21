# Required dependencies:
# pip install google-genai python-dotenv

import os
import base64
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from a .env file
load_dotenv()

def generate_gemini_response(user_input: str):
    """
    Generates a Gemini model response to a given user input.

    Args:
        user_input (str): The prompt/text input to send to the model.

    Returns:
        str: Combined response from the model.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    client = genai.Client(api_key=api_key)

    model = "gemini-2.5-pro"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)],
        ),
    ]

    tools = [types.Tool(googleSearch=types.GoogleSearch())]

    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        tools=tools,
        response_mime_type="text/plain",
    )

    response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response += chunk.text
    return response

# Test the module when run standalone
if __name__ == "__main__":
    print("🤖 Gemini AI Chatbot - CLI Mode")
    print("Type 'quit', 'exit', or 'bye' to end the conversation.\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Thanks for chatting!")
                break
            
            if not user_input:
                print("Please enter a message.")
                continue
            
            print("🤖 Thinking...")
            response = generate_gemini_response(user_input)
            print(f"Bot: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    if len(sys.argv) != 2:
        print('Please provide a prompt in the form of "Text ..." for the AI model')
        sys.exit(1)
    else:
        user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-001"

    response = client.models.generate_content(model=model, contents=messages)

    print(response.text)

    usage = response.usage_metadata

    print("Prompt tokens:", usage.prompt_token_count)
    print("Response tokens:", usage.candidates_token_count)


if __name__ == "__main__":
    main()

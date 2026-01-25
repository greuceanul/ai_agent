import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API Key could not be found")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=messages
    )

    usage = response.usage_metadata

    if usage is None:
        raise RuntimeError("Failed API request on usage metadata")
    if args.verbose is True:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", usage.prompt_token_count)
        print("Response tokens:", usage.candidates_token_count)

    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()

""" if len(sys.argv) != 2:
        print('Please provide a prompt in the form of "Text ..." for the AI model')
        sys.exit(1)
    else:
        user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]"""
